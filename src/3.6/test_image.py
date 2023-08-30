import os
import ssl

import subprocess

if __name__ == '__main__':
    openssl = subprocess.run(
        ["/usr/bin/openssl", "version"],
        stdout=subprocess.PIPE
    )
    assert ssl.OPENSSL_VERSION in str(openssl.stdout)
