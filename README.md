# Ansible Automation Platform Automation Examples

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Examples how to automate the automation when using Ansible Automation
Platform (AAP).

## Contents

* [aap_host_prepare.yml](aap_host_prepare.yml)
  * Example playbook to prepare RHEL systems for AAP 2.6 installation
* [ansible.cfg.installer](ansible.cfg.installer)
  * Enhanced ansible.cfg to use with the containerized installer
* [inventory.lab](inventory.lab)
  * Example containerized inventory to install AAP 2.6 in a small lab
  * Can be easily adjusted for bundle and non-bundle installations
* [examples](examples)
  * Example playbooks and configuration for further AAP setup automation

To create the required AAP manifest, see
[Red Hat Subscription Allocations tool](https://access.redhat.com/management/subscription_allocations)
and
[obtaining a manifest file](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/containerized_installation/assembly-gateway-licensing#assembly-aap-obtain-manifest-files).

If using
[automation analytics](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/using_automation_analytics/index)
with
[Red Hat Hybrid Cloud Console](https://console.redhat.com/ansible/),
see instructions [here](https://access.redhat.com/articles/7112649).

## AAP Host Preparation

Before installing AAP on RHEL (not OCP) it is a good idea to ensure a
known-good baseline configuration on the target hosts.

[aap_host_prepare.yml](aap_host_prepare.yml) is an example playbook that
could be used for this. It should be adjusted for the local environment
and it uses the
[https://github.com/myllynen/rhel-ansible-roles](https://github.com/myllynen/rhel-ansible-roles)
collection.

## Quick Usage Example

To install Ansible Automation Platform,
[download the preferred installer](https://access.redhat.com/downloads/content/480/),
[obtain a manifest file](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/containerized_installation/assembly-gateway-licensing#assembly-aap-obtain-manifest-files),
then unpack the installer, cd to the extracted directory, and adjust the
inventory:

```
# Install ansible-core from standard RHEL repos
sudo dnf install ansible-core
# Alternatively, install ansible-core and other helpful tools from AAP repos
sudo dnf --enablerepo=ansible-automation-platform-2.6-for-rhel-10-x86_64-rpms install \
  ansible-core ansible-builder ansible-lint ansible-navigator ansible-sign
# Update the inventory for the local environment
vi inventory
# Prepare AAP hosts for installation,
# make sure to review SSH/user config before applying
vi aap_host_prepare.yml
ansible-playbook -i inventory aap_host_prepare.yml
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
[https://access.redhat.com/articles/7112649](https://access.redhat.com/articles/7112649).

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
