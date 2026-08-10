"""Filters to normalize and compare AAP configuration"""

# pylint: disable=line-too-long,too-few-public-methods

from ansible.utils.unsafe_proxy import wrap_var

# May be used in infra.aap_configuration CaC but not exported or compared
KEYS_TO_IGNORE = {'lookup_organization', 'password', 'slug', 'token'}

# Default values to ignore to prevent noise in output
DEFAULTS_TO_IGNORE = (False, "", 0, "0", [], {}, None)

class FilterModule():
    """Filters module"""
    def filters(self):
        """Filter methods"""
        return {
            'merge_configs': merge_configs,
            'normalize_brackets': normalize_brackets,
            'normalize_lists': normalize_lists,
            'omit_deletions': omit_deletions,
            'omit_ignored': omit_ignored
        }


def merge_configs(repo, live):
    """Merge live config to repo config while pruning unmanaged entities"""
    if not repo or not isinstance(repo, dict) or not isinstance(live, dict):
        return wrap_var(repo)

    # Merge only entities present in repo
    if all(isinstance(v, dict) for v in repo.values()):
        return wrap_var({
            k: merge_configs(v, live[k]) if k in live else v
            for k, v in repo.items()
        })

    # Retain live operational defaults, overlay repo values
    merged = dict(repo)
    for k, v in repo.items():
        if k in live and isinstance(v, dict) and isinstance(live[k], dict):
            merged[k] = merge_configs(v, live[k])
        else:
            merged[k] = v

    # Reduce diff noise by ignoring specified defaults
    for k, live_val in live.items():
        if k not in repo and live_val in DEFAULTS_TO_IGNORE:
            merged[k] = live_val

    return wrap_var(merged)

# Handle infra.aap_configuration credential types injector syntax
def normalize_brackets(data, in_injectors=False):
    """Normalize brackets in AAP CaC"""
    if not in_injectors:
        if isinstance(data, dict):
            return wrap_var({k: normalize_brackets(v, k == 'injectors') for k, v in data.items()})
        return wrap_var(data)

    if isinstance(data, dict):
        return wrap_var({k: normalize_brackets(v, True) for k, v in data.items()})

    if isinstance(data, str) and '{' in data:
        fixed = data.replace('{  {', '{{').replace('{  %', '{%')
        return wrap_var(fixed)

    return wrap_var(data)

def normalize_lists(data):
    """Normalize lists in AAP CaC"""
    if isinstance(data, dict):
        return wrap_var({k: normalize_lists(v) for k, v in data.items() if k not in KEYS_TO_IGNORE})

    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            id_key = None
            for k in ('identifier', 'name', 'username'):
                if k in data[0]:
                    id_key = k
                    break
            if id_key:
                return wrap_var({
                    str(item[id_key]) if id_key in item else f"__missing_identity_index_{idx}__": normalize_lists(item)
                    for idx, item in enumerate(data)
                })
        return wrap_var([normalize_lists(item) for item in data])

    return wrap_var(data)

def omit_deletions(data, is_root=True):
    """Remove AAP CaC items with absent state"""
    if not isinstance(data, dict):
        return wrap_var(data)

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

    return wrap_var(cleaned)

def omit_ignored(data, ignore_map):
    """Remove ignored entities from data"""
    if not isinstance(data, dict) or not ignore_map:
        return wrap_var(data)

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

                if item_v or not isinstance(item_v, dict):
                    sub_dict[item_k] = item_v

            if sub_dict:
                cleaned[key] = sub_dict

    return wrap_var(cleaned)
