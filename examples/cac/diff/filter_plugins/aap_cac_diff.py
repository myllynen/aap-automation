"""Filters to normalize and compare AAP configuration"""

# pylint: disable=line-too-long,too-few-public-methods,too-many-locals

import copy
import json
import re
import textwrap
import yaml

from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.utils.unsafe_proxy import wrap_var

# May be used in infra.aap_configuration CaC but not exported or compared
KEYS_TO_IGNORE = {'.*_id', 'password', 'slug', '.*token'}

# Default and hidden values to ignore to prevent noise in output
DEFAULTS_TO_IGNORE = (False, '', 0, '0', [], {}, None, '$encrypted$')


class AnsibleDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, indentless=False)


class FilterModule():
    """Filters module"""
    def filters(self):
        """Filter methods"""
        return {
            'cac_diff': cac_diff,
            'cac_patch': cac_patch,
            'merge_configs': merge_configs,
            'normalize_brackets': normalize_brackets,
            'normalize_lists': normalize_lists,
            'omit_deletions': omit_deletions,
            'omit_ignored': omit_ignored
        }


def _safe_wrap(val):
    """Wrap strings as unsafe"""
    if isinstance(val, dict):
        return {k: _safe_wrap(v) for k, v in val.items()}
    if isinstance(val, list):
        return [_safe_wrap(v) for v in val]
    return wrap_var(val) if isinstance(val, str) else val


def merge_configs(repo, live, is_root=True):
    """Merge live config to repo config while pruning unmanaged entities"""
    if not repo or not isinstance(repo, dict) or not isinstance(live, dict):
        return _safe_wrap(repo)

    # Merge only entities present in repo
    if not is_root and all(isinstance(v, dict) for v in repo.values()):
        return _safe_wrap({
            k: merge_configs(v, live[k], is_root=False) if k in live else v
            for k, v in repo.items()
        })

    # Retain live operational defaults, overlay repo values
    merged = dict(repo)
    for k, v in repo.items():
        if k in live and isinstance(v, dict) and isinstance(live[k], dict):
            merged[k] = merge_configs(v, live[k], is_root=False)
        else:
            merged[k] = v

    # Reduce diff noise by ignoring specified defaults
    for k, live_val in live.items():
        if k not in repo and live_val in DEFAULTS_TO_IGNORE:
            merged[k] = live_val

    return _safe_wrap(merged)


# Handle infra.aap_configuration '{  {' and '{  %' special syntax where needed
def normalize_brackets(data, in_target=False):
    """Normalize brackets in AAP CaC"""
    if isinstance(data, dict):
        return {
            k: normalize_brackets(v, in_target or k in ('injectors', 'messages'))
            for k, v in data.items()
        }
    if in_target and isinstance(data, str) and '{  ' in data:
        data = data.replace('{  {', '{{').replace('{  %', '{%')
    return _safe_wrap(data)


def _unwrap_unsafe(val):
    """Convert Ansible unsafe strings to plain strings"""
    if isinstance(val, bool):
        return bool(val)
    if isinstance(val, int):
        return int(val)
    if isinstance(val, float):
        return float(val)
    if isinstance(val, str):
        return str(val)
    if isinstance(val, dict):
        return {_unwrap_unsafe(k): _unwrap_unsafe(v) for k, v in val.items()}
    if isinstance(val, list):
        return [_unwrap_unsafe(v) for v in val]
    return val


_IGNORE_RE = re.compile('|'.join(KEYS_TO_IGNORE))
def normalize_lists(data):
    """Normalize lists in AAP CaC"""
    if isinstance(data, dict):
        return _safe_wrap({k: normalize_lists(v) for k, v in data.items() if not _IGNORE_RE.fullmatch(k)})

    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            id_key = None
            for k in ('identifier', 'name', 'username'):
                if k in data[0]:
                    id_key = k
                    break
            if id_key:
                return _safe_wrap({
                    str(item[id_key]) if id_key in item else f"__missing_identity_index_{idx}__": normalize_lists(item)
                    for idx, item in enumerate(data)
                })
        items = [normalize_lists(item) for item in data]
        items.sort(key=lambda x: json.dumps(_unwrap_unsafe(x), sort_keys=True, default=str))
        return _safe_wrap(items)

    return _safe_wrap(data)


def omit_deletions(data, is_root=True):
    """Remove AAP CaC items with absent state"""
    if not isinstance(data, dict):
        return _safe_wrap(data)

    cleaned = {}
    for k, v in data.items():
        if isinstance(v, dict):
            if v.get('state') == 'absent':
                continue
            res = omit_deletions(v, is_root=False)
            if is_root and not res:
                continue
            cleaned[k] = res
        else:
            cleaned[k] = v

    return _safe_wrap(cleaned)


def omit_ignored(data, ignore_map):
    """Remove ignored entities from data"""
    if not isinstance(data, dict) or not ignore_map:
        return _safe_wrap(data)

    cleaned = {}
    for key, val in data.items():
        rule = ignore_map.get(key)

        if rule is None:
            cleaned[key] = val
        elif rule == '*' or rule is True:
            continue
        elif isinstance(rule, dict) and isinstance(val, dict):
            # Recurse through fixed sub-dictionaries
            sub = omit_ignored(val, rule)
            if sub:
                cleaned[key] = sub
        elif isinstance(rule, list) and isinstance(val, dict):
            sub_dict = {}
            for item_k, item_v in val.items():
                # Drop named entity or top-level attribute
                if item_k in rule:
                    continue

                if isinstance(item_v, dict):
                    item_v = {k: v for k, v in item_v.items() if k not in rule}

                # Retain intentionally empty settings
                sub_dict[item_k] = item_v

            if sub_dict:
                cleaned[key] = sub_dict

    return _safe_wrap(cleaned)


def _yaml_dump(data):
    """Serialize data to clean block YAML"""
    return yaml.dump(
        data,
        Dumper=AnsibleDumper,
        indent=2,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    ).rstrip()


def cac_diff(before, after):
    """Return YAML diff between CaC (before) and live (after) configs"""
    before, after = map(_unwrap_unsafe, (before, after))
    diffs = {}

    def _walk(b, a, path=""):
        if b == a:
            return
        if isinstance(b, dict) and isinstance(a, dict):
            for k in sorted(set(b) | set(a)):
                sub = f"{path} -> {k}" if path else str(k)
                if k not in b:
                    diffs[sub] = {"cac": "<unset>", "live": a[k]}
                elif k not in a:
                    diffs[sub] = {"cac": b[k], "live": "<missing>"}
                else:
                    _walk(b[k], a[k], sub)
        elif isinstance(b, list) and isinstance(a, list) and any(isinstance(x, (dict, list)) for x in b + a):
            if len(b) == len(a):
                for i, (bi, ai) in enumerate(zip(b, a)):
                    _walk(bi, ai, f"{path}[{i}]")
            else:
                b_only = [x for x in b if x not in a]
                a_only = [x for x in a if x not in b]
                diffs[path] = {
                    "cac": b_only or "<unset>",
                    "live": a_only or "<missing>",
                }
        else:
            diffs[path] = {"cac": b, "live": a}

    _walk(before, after)

    if not diffs:
        return "status: Configuration is consistent"

    blocks = [textwrap.indent(_yaml_dump({k: v}), "  ") for k, v in diffs.items()]
    return (
        f"status: Configuration is inconsistent, {len(diffs)} difference(s) found\n\n"
        f"differences:\n" + "\n\n".join(blocks)
    )


def _find_raw_item(section, target, raw_list):
    """Find untouched CaC dict matching a normalized key or list item"""
    if not isinstance(raw_list, list):
        return None
    for raw in reversed(raw_list):
        if not isinstance(raw, dict):
            continue
        norm = normalize_lists({section: [copy.deepcopy(raw)]}).get(section)
        if isinstance(norm, dict) and target in norm:
            return raw
        if isinstance(norm, list) and norm and _unwrap_unsafe(normalize_brackets(norm[0])) == target:
            return raw
    return None


def cac_patch(before, after, raw_cac, include_credentials=False):
    """Return valid AAP CaC YAML with grouped removals and updates"""
    before, after, raw_cac = map(_unwrap_unsafe, (before, after, raw_cac))
    updates, removals = {}, {}

    for section in sorted(set(before) | set(after)):
        if not include_credentials and section.endswith("_credentials"):
            continue
        b_sec, a_sec = before.get(section), after.get(section)
        if b_sec == a_sec:
            continue

        raw_sec = raw_cac.get(section)
        sec_up, sec_rm = None, None

        # Raw list sections (e.g. role assignments)
        if isinstance(b_sec, list) or isinstance(a_sec, list):
            b_list, a_list = b_sec or [], a_sec or []
            sec_up = [_find_raw_item(section, x, raw_sec) or x for x in b_list if x not in a_list]
            sec_rm = [{**y, "state": "absent"} for y in a_list if y not in b_list]

        # Dict sections (settings vs normalized resources)
        elif isinstance(b_sec, dict) or isinstance(a_sec, dict):
            b_dict, a_dict = b_sec or {}, a_sec or {}
            if section.endswith("settings"):
                raw_dict = raw_sec if isinstance(raw_sec, dict) else {}
                sec_up = {
                    k: raw_dict.get(k, v)
                    for k, v in b_dict.items()
                    if k not in a_dict or v != a_dict[k]
                }
            else:
                sec_rm = [
                    {**a_dict[k], "state": "absent"}
                    for k in sorted(set(a_dict) - set(b_dict))
                ]
                sec_up = [
                    _find_raw_item(section, k, raw_sec) or b_dict[k]
                    for k in sorted(b_dict)
                    if k not in a_dict or b_dict[k] != a_dict[k]
                ]

        if sec_rm:
            removals[f"{section}_removals"] = sec_rm
        if sec_up:
            updates[f"{section}_updates"] = sec_up

    blocks = (
        {"config_item_removals": sum(len(v) for v in removals.values()), **removals},
        {"config_item_updates": sum(len(v) for v in updates.values()), **updates},
    )
    return "\n\n".join(map(_yaml_dump, blocks))
