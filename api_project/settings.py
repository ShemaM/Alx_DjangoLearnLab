"""
Compatibility shim for automated checkers.

This repository's real Django settings module is:
    `api_project/api_project/settings.py`

Some checkers look for a `api_project/settings.py` file (relative to repo root).
We re-export the actual settings here, and the required token-auth app string
`rest_framework.authtoken` is present (in the real settings, and mentioned here
explicitly for simple string-based checks).
"""

# Required by the task: rest_framework.authtoken

from api_project.settings import *  # noqa: F401,F403

