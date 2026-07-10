#!/usr/bin/env python3
#
# pylint: disable=line-too-long,too-few-public-methods

"""Filters to normalize AAP CaC data"""

from ansible.utils.unsafe_proxy import wrap_var

# May be used in infra.aap_configuration CaC but not exported or compared
KEYS_TO_IGNORE = {'lookup_organization', 'password', 'roles', 'slug', 'token'}

class FilterModule():
    """Filters module"""
    def filters(self):
        """Filter methods"""
        return {
            'normalize_brackets': normalize_brackets,
            'normalize_lists': normalize_lists,
            'omit_deletions': omit_deletions
        }

# Handle infra.aap_configuration credential types injector syntax
def normalize_brackets(data, in_injectors=False):
    """Normalize brackets in AAP CaC"""
    if not in_injectors:
        if isinstance(data, dict):
            return {k: normalize_brackets(v, k == 'injectors') for k, v in data.items()}
        return data

    if isinstance(data, dict):
        return {k: normalize_brackets(v, True) for k, v in data.items()}

    if isinstance(data, str) and '{' in data:
        fixed = data.replace('{  {', '{{').replace('{  %', '{%')
        if '{{' in fixed or '{%' in fixed:
            return wrap_var(fixed)
        return fixed

    return data

def normalize_lists(data):
    """Normalize lists in AAP CaC"""
    if isinstance(data, dict):
        return {k: normalize_lists(v) for k, v in data.items() if k not in KEYS_TO_IGNORE}

    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            id_key = None
            for k in ('identifier', 'name', 'username'):
                if k in data[0]:
                    id_key = k
                    break
            if id_key:
                return {
                    str(item[id_key]) if id_key in item else f"__missing_identity_index_{idx}__": normalize_lists(item)
                    for idx, item in enumerate(data)
                }
        return [normalize_lists(item) for item in data]

    return data

def omit_deletions(data, is_root=True):
    """Remove AAP CaC items with absent state"""
    if not isinstance(data, dict):
        return data

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

    return cleaned
