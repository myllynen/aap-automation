# Ansible Automation Platform Automation

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Ansible collection of playbooks and roles to install and upgrade
Ansible Automation Platform using RPMs.

## Contents

* [vars_aap.yml](vars_aap.yml)
  * Example vars file for installation and configuration
* [vault_aap.yml](vault_aap.yml)
  * Unencrypted example vault file
* [inventory](inventory)
  * Example inventory where to run the installer
* [aap_install.yml](aap_install.yml)
  * Playbook to install Ansible Automation Platform
* [aap_manifest](aap_manifest.yml)
  * Playbook to download and install required manifest
* [aap_upgrade.yml](aap_upgrade.yml)
  * Playbook to upgrade Ansible Automation Platform

These playbooks and roles allow for fully automating Ansible Automation
Platform installation, manifest handling, and upgrades. The playbooks
use supported RPMs from Red Hat repositories and download the required
manifest file from Red Hat Customer Portal removing the need to download
or provide any installation related files manually. For more information
about the manifest, see
[Subscription Allocations page](https://access.redhat.com/management/subscription_allocations)
and
[creating a new subscription allocation](https://docs.ansible.com/automation-controller/latest/html/userguide/import_license.html#obtaining-a-subscriptions-manifest).

The installation playbook and role provide three different alternatives:

1. Simple demo setup with single-node Automation Controller and an
   optional Automation Hub node. Only the hostname(s) need to be
   provided and the playbook will take care of the rest. See below for a
   basic example and also [vars_aap.yml](vars_aap.yml) and
   [vault_aap.yml](vault_aap.yml).
1. Template based setup which requires specifying different hosts
   for installation (see
   [roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
   for details.
1. Customized setup using a manually crafted installer inventory file,
   see
   [roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
   for additional details.

The only requirements prior installation and upgrades are:

1. The target RHEL installation nodes have been properly subscribed so
   that the standard RHEL repositories are enabled and Ansible
   Automation Platform subscription is available to allow the installer
   to enable the Ansible Automation Platform repositories when needed.
1. DNS, networking, SSH, and timesync have been setup properly.
1. Root access on all nodes (including the installer node, for now).

The [inventory](inventory) file in this directory specifies the bastion
host, i.e., where to run the actual installer. Especially in the demo
setup it can well be the same node as the Automation Contoller node.

A basic demo setup with a controller node only would be like, please see
[vars_aap.yml](vars_aap.yml) for a slightly more complete example and
[roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
for all the supported variables. By default all the passwords are set to
_foobar123_, see [vault_aap.yml](vault_aap.yml).

```
# AAP repository version
aap_install_version: "2.2"
aap_install_demo_setup: true
aap_install_controller_fqdn: ctrl.example.com
```

These playbooks have been tested most recently with Ansible Automation
Platform 2.2.1 on RHEL 8.6.

## Quick Usage Example

To install this collection:

```
ansible-galaxy collection install git+https://github.com/myllynen/aap-automation,master
```

To install Ansible Automation Platform, automatically download manifest
from Red Hat Customer Portal and upload it to the Automation Controller:

```
# Edit settings and credentials to suite local environment
vi vars_aap.yml vault_aap.yml
# Set the hostname where to run the actual installer
vi inventory
# Install Ansible Automation Platform
ansible-playbook -i inventory myllynen.aap_automation.aap_install.yml
# Download and install manifest
ansible-playbook -i inventory myllynen.aap_automation.aap_manifest.yml
# Upgrade Ansible Automation Platform
ansible-playbook -i inventory myllynen.aap_automation.aap_upgrade.yml
```

## See Also

See also
[https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform](https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles).

See also
[https://github.com/myllynen/rhel-ansible-roles](https://github.com/myllynen/rhel-ansible-roles).

See also
[https://github.com/redhat-cop](https://github.com/redhat-cop).

## License

GPLv3+
