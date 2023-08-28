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
  * Example inventory for where to run the installer
* [playbooks/aap_install.yml](playbooks/aap_install.yml)
  * Playbook to install Ansible Automation Platform
* [playbooks/aap_manifest](playbooks/aap_manifest.yml)
  * Playbook to download and install required manifest
* [playbooks/aap_upgrade.yml](playbooks/aap_upgrade.yml)
  * Playbook to upgrade Ansible Automation Platform

These playbooks and roles allow for fully automating Ansible Automation
Platform installation,
[subscription manifest handling](https://docs.ansible.com/automation-controller/latest/html/userguide/import_license.html#import-a-subscription),
and upgrades. The playbooks use supported RPMs from Red Hat repositories
and download the required manifest file from Red Hat Customer Portal
removing the need to download or provide any installation related files
manually. For more information about the manifest, see
[Red Hat Subscription Allocations tool](https://access.redhat.com/management/subscription_allocations)
and
[obtaining a subscription manifest](https://docs.ansible.com/automation-controller/latest/html/userguide/import_license.html#obtaining-a-subscriptions-manifest).

The installation playbook and role support three different installation
variants:

1. Simple demo setup with a single-node Automation Controller and optional
   Automation Hub and/or EDA Controller nodes. Only the hostname(s) need to
   be provided and the playbook will take care of the rest. See below for a
   basic example and also see [vars_aap.yml](vars_aap.yml) and
   [vault_aap.yml](vault_aap.yml).
1. Template based setup which requires specifying different hosts
   for installation (see
   [roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
   for details).
1. Customized setup using a manually crafted installer inventory file,
   see
   [roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
   for details and
   [roles/aap_install/templates/inventory.j2](roles/aap_install/templates/inventory.j2)
   for an example.

The only requirements prior installation and upgrades are:

1. The target RHEL installation nodes have been properly subscribed so
   that the standard
   [RHEL repositories](https://github.com/linux-system-roles/rhc)
   are enabled and Ansible Automation Platform subscription is available
   to allow the installer to enable the Ansible Automation Platform
   repositories when needed.
1. DNS, networking, SSH, and timesync have been setup properly. The
   installer will open the needed firewall ports if the _firewalld_
   service was enabled during installation.
1. Passwordless sudo rights on all nodes, including the installer host.
   If the installer RPM was already installed on the installer host then
   sudo rights on the installer host are needed only due to AAP-14991
   (hopefully to be fixed in a future release).

The [inventory](inventory) file in this directory specifies the
installer (bastion) host, i.e., where to run the actual installer.
Especially in a demo setup this can well be the same host as the
as the local system and the Automation Controller node.

The most minimal configuration for a basic demo setup with the
controller node only could be like this:

```
# AAP repository version
aap_install_version: "2.4"
aap_install_demo_setup: true
aap_install_controller_fqdn: ctrl.example.com
```

See [vars_aap.yml](vars_aap.yml) for a more complete example and
[roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
for all the supported variables.

All the credentials used are listed in [vault_aap.yml](vault_aap.yml).

These playbooks have been tested most recently using Ansible 2.14 to
install Ansible Automation Platform 2.4 on RHEL 8.8.

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
ansible-playbook -i inventory -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_install.yml
# Download and install manifest
ansible-playbook -i inventory -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_manifest.yml
# Upgrade Ansible Automation Platform
ansible-playbook -i inventory -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_upgrade.yml
```

## See Also

See also
[https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform](https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles).

See also
[https://github.com/myllynen/aap-troubleshooting-guide](https://github.com/myllynen/aap-troubleshooting-guide).

See also
[https://github.com/myllynen/rhel-ansible-roles](https://github.com/myllynen/rhel-ansible-roles).

See also
[https://github.com/redhat-cop](https://github.com/redhat-cop).

## License

GPLv3+
