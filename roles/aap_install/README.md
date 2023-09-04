# aap_install role

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Please see the collection main page for a higher level description.

## Configuration

Below are the role default values from defaults/main.yml:

<pre>
---
# Ansible Automation Platform version
aap_install_version: "2.4"

# Hostnames for status checks of components
# In demo setup these will be used as hosts,
# only the controller is required for demo.
aap_install_controller_fqdn:
aap_install_hub_fqdn:
aap_install_eda_controller_fqdn:


# Directory where AAP setup.sh is, if missing
# installer RPM will be installed using sudo.
# Defaults to RPM created installer directory
# Bundle installer will need rsync on bastion
aap_install_installer_dir: /opt/ansible-automation-platform/installer

# Full path to installer inventory on bastion
aap_install_inventory_path: /root/inventory

# Directory to store installer setup log(s)
aap_install_setup_log_dir: "{{ aap_install_installer_dir }}"

# Custom parameters for setup.sh (string)
aap_install_script_custom_parameters:

# Optional ansible.cfg to use with the installer
# If not set the default (if any) will be used
aap_install_installer_config:

# Force running installer, skip status checks
aap_install_installer_run_always: false

# Always try install latest installer RPM
aap_install_installer_update: false

# Register AAP nodes to Red Hat Insights
aap_install_insights_enable: false


# Local custom installer inventory template to use
# If defined no other variables below will be used
# Must differ from aap_install_inventory_path when
# the bastion host is the same system ie localhost
aap_install_inventory_custom:


# Demo setup of controller+db and optional hub/eda
# If true all the other node variables are ignored
aap_install_demo_setup: true


# Trusted container registry used by hub
aap_install_registry_url: registry.redhat.io
# These should come from vault
#aap_install_registry_username:
#aap_install_registry_password:

# Enable hub api log and hub analytics
aap_install_hub_api_log_analytics: true


#
# Node definitions for multi-node installation
#
aap_install_controller_nodes:
#  - fqdn: ctrl-1.example.com
#    vars: node_type=control
#  - fqdn: ctrl-2.example.com
#    vars: node_type=control peers=execution_nodes
#  - fqdn: ctrl-3.example.com
#    vars: node_type=control peers=execution_nodes

aap_install_database_node:
#  fqdn: db.example.com

# Following variables are optional
aap_install_execution_nodes:
#  - fqdn: exec-1.example.com
#    vars: node_type=execution peers=exec-2.example.com
#  - fqdn: exec-2.example.com
#    vars: node_type=execution peers=exec-3.example.com
#  - fqdn: exec-3.example.com
#    vars: node_type=execution

# These must be defined together
aap_install_hub_node:
#  fqdn: hub.example.com
aap_install_hub_database_node:
#  fqdn: db.example.com

# These must be defined together
aap_install_eda_controller_node:
#  fqdn: eda.example.com
aap_install_eda_controller_database_node:
#  fqdn: db.example.com

# Optional SSO instance to use
aap_install_sso_node:
#  fqdn: sso.example.com

# Lines to be added to end of template
aap_install_template_additional_lines: |
  # Inventory custom part starts here
</pre>

## License

GPLv3+
