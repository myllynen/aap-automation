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

# Manifest path on the target host
aap_manifest_path: /root/aap_manifest.zip

#
# Required when copying manifest
#
# Manifest file to copy to target host
aap_manifest_file: files/aap_manifest.zip

#
# Required when downloading manifest
#
# Manifest download UUID
aap_manifest_uuid:
</pre>

## License

GPLv3+
