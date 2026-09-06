"""Robust launcher for Nuitka with Antivirus retry tolerance for Windows resource updates.

Complies with SOLID principles by isolating Windows filesystem lock resilience.
"""
from __future__ import annotations

import os
import sys

try:
    import nuitka.utils.Utils as utils

    _orig_decorator = utils.decoratorRetries

    def _robust_decoratorRetries(
        logger,
        purpose,
        consequence,
        extra_recommendation=None,
        attempts=5,
        sleep_time=1,
        exception_type=OSError,
    ):
        # Extend attempts to 35 with 2s delay to outlast antivirus file scanning on large binaries
        return _orig_decorator(
            logger=logger,
            purpose=purpose,
            consequence=consequence,
            extra_recommendation=extra_recommendation,
            attempts=35,
            sleep_time=2,
            exception_type=exception_type,
        )

    utils.decoratorRetries = _robust_decoratorRetries
except Exception:
    pass

from nuitka import __main__

if __name__ == "__main__":
    __main__.main()
