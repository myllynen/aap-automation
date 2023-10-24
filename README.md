# Ansible Automation Platform Automation

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Ansible collection of playbooks and roles to install and upgrade Ansible
Automation Platform using RPMs.

Supports also installation from the offline setup bundle.

## Contents

* [vars_aap.yml](vars_aap.yml)
  * Example vars file for installation
* [vault_aap.yml](vault_aap.yml)
  * Unencrypted example vault file
* [bastion](bastion)
  * Define the host where to run the installer
* [playbooks/aap_install.yml](playbooks/aap_install.yml)
  * Playbook to install Ansible Automation Platform
* [playbooks/aap_manifest](playbooks/aap_manifest.yml)
  * Playbook to download and install required manifest
* [playbooks/aap_upgrade.yml](playbooks/aap_upgrade.yml)
  * Playbook to upgrade Ansible Automation Platform
* [playbooks/aap_ctrl_token_get.yml](playbooks/aap_ctrl_token_get.yml)
  * Playbook to get authentication token used with later AAP configuration
* [examples](examples)
  * Example playbooks and configuration for further AAP setup automation

These playbooks and roles allow for fully automating Ansible Automation
Platform installation,
[subscription manifest handling](https://docs.ansible.com/automation-controller/latest/html/userguide/import_license.html#import-a-subscription),
and upgrades. The playbooks by default use supported RPMs from Red Hat
repositories and automatically download the required manifest file from
Red Hat Customer Portal removing the need to download or provide any
installation related files manually. However, in case the installer
directory was populated by manually provided setup files or a manifest
was made available locally those can also be used. For more information
about the manifest, see
[Red Hat Subscription Allocations tool](https://access.redhat.com/management/subscription_allocations)
and
[obtaining a subscription manifest](https://docs.ansible.com/automation-controller/latest/html/userguide/import_license.html#obtaining-a-subscriptions-manifest).

The installation playbook and role support three different installation
variants:

1. Simple demo setup with a single-node Automation Controller and
   optional Automation Hub and/or EDA Controller nodes. Only the
   hostname(s) need to be provided and the playbook will take care of
   the rest. See below for a basic example and also see
   [vars_aap.yml](vars_aap.yml) and [vault_aap.yml](vault_aap.yml).
1. Template based setup which requires specifying different hosts
   for installation (see
   [roles/aap_install/defaults/main.yml](roles/aap_install/defaults/main.yml)
   for details).
1. Customized setup using a manually crafted installer inventory template,
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
1. Passwordless sudo rights on all AAP nodes. Needed also on the
   installer host if the RPM needs to be installed. If the installer RPM
   was already installed on the installer host then sudo rights on the
   installer host are needed only, for now, due to AAP-14991 (to be
   fixed in a future release).

The [bastion](bastion) file in this directory specifies the bastion
installer host, i.e., where to run the actual installer. Especially in a
demo setup this can well be the same host as the as the local system and
the Automation Controller node.

The most minimal installation for a basic demo setup with the controller
node only could be like this:

```
aap_install_version: "2.4"
aap_install_demo_setup: true
aap_install_controller_fqdn: ctrl.example.com
aap_install_inventory_path: /tmp/inventory
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

To create and get an authentication token for Ansible Automation
Platform administrator run the helper playbook:

```
# Create and get an administrator token
ansible-playbook -c local -i localhost, -e @vars_aap.yml -e @vault_aap.yml \
  myllynen.aap_automation.aap_ctrl_token_get.yml
# Copy the token for later use and remove the token file
vi ./aap-token-admin.txt
rm ./aap-token-admin.txt
```

Configuration, project and team creation, and other follow-up tasks are
best done with
[Red Hat validated collections](https://www.redhat.com/en/blog/automate-expert-ansible-validated-content)
for Ansible Automation Platform, see especially the
_infra.controller\_configuration_, _infra.ah\_configuration_,
_infra.ee\_utilities_, and _infra.aap\_utilities_ collections at
[Red Hat Automation Hub](https://console.redhat.com/ansible/automation-hub/namespaces/infra).
An upstream example of how to utilize _infra.controller\_configuration_
for configuring automation controller is also
[available](https://github.com/redhat-cop/aap_configuration_template/blob/main/playbooks/controller_config.yml).

## See Also

See also
[https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform](https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller).

See also
[https://console.redhat.com/ansible/automation-hub/namespaces/infra](https://console.redhat.com/ansible/automation-hub/namespaces/infra).

See also
[https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles).

See also
[https://github.com/myllynen/rhel-ansible-roles](https://github.com/myllynen/rhel-ansible-roles).

See also
[https://github.com/myllynen/aap-troubleshooting-guide](https://github.com/myllynen/aap-troubleshooting-guide).

See also
[https://github.com/redhat-cop](https://github.com/redhat-cop).

## License

GPLv3+
