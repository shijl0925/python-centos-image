import os
import ssl

import subprocess

if __name__ == '__main__':

    openssl = subprocess.run(
        [f"/usr/local/openssl/bin/openssl", "version"],
        capture_output=True,
        text=True
    ).stdout
    assert ssl.OPENSSL_VERSION in openssl
