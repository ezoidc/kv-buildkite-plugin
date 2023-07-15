"""Environment hook."""

import os
import json
import subprocess
from urllib.request import urlopen, Request
import shlex
import sys

org = os.environ.get("BUILDKITE_PLUGIN_KV_ORG")
audience = f"https://oidc.bcj.io/{org}"
token = (
    subprocess.check_output(
        [
            "buildkite-agent",
            "oidc",
            "request-token",
            "--audience",
            audience,
            "--lifetime",
            "300",
        ]
    )
    .decode()
    .strip()
)

request = Request(
    "https://oidc.bcj.io/api/v0/variables",
    headers={"Authorization": f"Bearer {token}"},
    method="POST",
)

with urlopen(request) as response:
    response = json.loads(response.read().decode())

for var in response.get("variables", []):
    value = var.get("value")
    envvar = var.get("envvar")
    key = var.get("key")
    sensitive = var.get("sensitive")

    sys.stderr.write(
        f"Setting {envvar} to {key} (sensitive={sensitive})\n",
    )

    print(f"export {shlex.quote(f'{envvar}={value}')}")
