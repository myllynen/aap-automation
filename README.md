# Ansible Automation Platform Automation Examples

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Examples how to automate the automation when using AAP
(Ansible Automation Platform).

## Contents

* [ansible.cfg](ansible.cfg)
  * Enhanced example ansible.cfg to use with the containerized installer
* [inventory.lab](inventory.lab)
  * Example containerized inventory to install AAP 2.5 in a small lab env
  * Can be easily adjusted for bundle and non-bundle installations
* [examples](examples)
  * Example playbooks and configuration for further AAP setup automation

To create the required AAP manifest, see
[Red Hat Subscription Allocations tool](https://access.redhat.com/management/subscription_allocations)
and
[obtaining a manifest file](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/access_management_and_authentication/assembly-gateway-licensing#assembly-aap-obtain-manifest-files).

## Quick Usage Example

To install this collection from GitHub:

```
ansible-galaxy collection install git+https://github.com/myllynen/aap-automation,master
```

To install Ansible Automation Platform, automatically download manifest
from Red Hat Customer Portal and upload it to the Automation Controller:

```
# Set the hostname where to run the actual installer
vi inventory
# Edit settings and credentials to suite local environment
vi vars_aap.yml vault_aap.yml
# Install Ansible Automation Platform
ansible-playbook -i bastion -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_install.yml
# Download and install manifest
ansible-playbook -i bastion -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_manifest.yml
# Upgrade Ansible Automation Platform
ansible-playbook -i bastion -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_upgrade.yml
```

## Next Steps



## See Also

See also
[https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform](https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform).

See also
[https://console.redhat.com/ansible/automation-hub/namespaces/ansible](https://console.redhat.com/ansible/automation-hub/namespaces/ansible).

See also
[https://console.redhat.com/ansible/automation-hub/namespaces/infra](https://console.redhat.com/ansible/automation-hub/namespaces/infra).

See also
[https://github.com/myllynen/aap-troubleshooting-guide](https://github.com/myllynen/aap-troubleshooting-guide).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles).

See also
[https://github.com/myllynen/rhel-ansible-roles](https://github.com/myllynen/rhel-ansible-roles).

See also
[https://github.com/myllynen/windows-ansible-roles](https://github.com/myllynen/windows-ansible-roles).

See also
[https://github.com/redhat-cop](https://github.com/redhat-cop).

## License

GPLv3+
