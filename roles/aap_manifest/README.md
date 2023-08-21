# aap_manifest role

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0)

Please see the collection main page for a higher level description.

## Configuration

Below are the role default values from defaults/main.yml:

<pre>
---
# Either copy a manifest file from the local system
# or download directly from Red Hat Customer Portal
aap_manifest_download: false

# Manifest path to use on the target host
aap_manifest_path: /root/aap_manifest.zip

#
# Required when copying manifest
#
# Local manifest file to copy to the target host
aap_manifest_file: aap_manifest.zip

#
# Required when downloading manifest
#
# Manifest UUID to download
aap_manifest_uuid:

# Red Hat Customer Portal credentials for downloading
# These should come from vault
#aap_rhsm_username:
#aap_rhsm_password:
</pre>

## License

GPLv3+
