import os
import ssl
import sys

import subprocess

if __name__ == '__main__':
    openssl_version = sys.argv[1]

    openssl = subprocess.run(
        [f"/usr/local/openssl-{openssl_version}/bin/openssl", "version"],
        capture_output=True,
        text=True
    ).stdout
    assert ssl.OPENSSL_VERSION in openssl
