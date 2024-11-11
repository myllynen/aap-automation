# Ansible Automation Platform Automation Examples

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Examples how to automate the automation when using Ansible Automation
Platform (AAP).

## Contents

* [aap_host_prepare.yml](aap_host_prepare.yml)
  * Example playbook to prepare RHEL 9 systems for AAP 2.5 installation
* [ansible.cfg.install](ansible.cfg.install)
  * Enhanced ansible.cfg to use with the containerized installer
* [inventory.lab](inventory.lab)
  * Example containerized inventory to install AAP 2.5 in a small lab
  * Can be easily adjusted for bundle and non-bundle installations
* [examples](examples)
  * Example playbooks and configuration for further AAP setup automation

To create the required AAP manifest, see
[Red Hat Subscription Allocations tool](https://access.redhat.com/management/subscription_allocations)
and
[obtaining a manifest file](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/access_management_and_authentication/assembly-gateway-licensing#assembly-aap-obtain-manifest-files).

## AAP Host Preparation

Before installing AAP on RHEL (not OCP) it is a good idea to ensure a
known-good baseline configuration on the target hosts.

[aap_host_prepare.yml](aap_host_prepare.yml) is an example playbook
that could be used for this. It should be adjusted for the local
environment and it uses the
[https://github.com/myllynen/rhel-ansible-roles](https://github.com/myllynen/rhel-ansible-roles)
collection.

## Quick Usage Example

To install Ansible Automation Platform,
[download the preferred installer](https://access.redhat.com/downloads/content/480/),
[obtain a manifest file](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/access_management_and_authentication/assembly-gateway-licensing#assembly-aap-obtain-manifest-files),
then unpack the installer, cd to the extracted directory, and adjust the inventory:

```
# Install supported ansible-core version and other tools
sudo dnf install --enablerepo=ansible-automation-platform-2.5-for-rhel-9-x86_64-rpms \
  ansible-core ansible-builder ansible-lint ansible-navigator ansible-sign
# Update the inventory for the local environment
vi inventory
# Run the AAP containerized installer
ansible-playbook -i inventory ansible.containerized_installer.install
```

## Next Steps

See [examples](examples).

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
