#!/usr/bin/env python3
#
# pylint: disable=line-too-long,too-few-public-methods

"""Filters to normalize AAP CaC data"""

from ansible.utils.unsafe_proxy import wrap_var

# May be used in infra.aap_configuration CaC but not exported
KEYS_TO_IGNORE = {'lookup_organization', 'password', 'roles', 'slug', 'token'}

class FilterModule():
    """Filters module"""
    def filters(self):
        """Filters method"""
        return {
            'normalize_brackets': normalize_brackets,
            'normalize_lists': normalize_lists
        }

# Handle infra.aap_configuration credential types injector syntax
def normalize_brackets(data, in_injectors=False):
    """Normalize brackets in AAP CaC"""
    if isinstance(data, dict):
        return {
            k: normalize_brackets(v, in_injectors=(in_injectors or k == 'injectors'))
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [normalize_brackets(item, in_injectors=in_injectors) for item in data]
    if isinstance(data, str):
        if not in_injectors:
            return data
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
            identity_key = next((k for k in ['identifier', 'name', 'username'] if k in data[0]), None)
            if identity_key:
                return {
                    str(item.get(identity_key, f"__missing_identity_index_{idx}__")): normalize_lists(item)
                    for idx, item in enumerate(data)
                }
        return [normalize_lists(item) for item in data]
    return data
