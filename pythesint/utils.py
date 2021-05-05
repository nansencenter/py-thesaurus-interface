"""Utilities"""

import re

def set_github_version(url, version):
    """Returns a modified `url` using `version`. Only works for raw
    content URLs from github
    """
    return re.sub(
        r'(https://raw.githubusercontent.com/([^/]+/){2})[^/]+/',
        r'\g<1>{}/'.format(version),
        url)
