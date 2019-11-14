from cement.utils.version import get_version as cement_get_version

VERSION = (0, 1, 0, "alpha", 0)


def get_version(version=VERSION):
    "Returns a PEP 386-compliant version number from VERSION."

    return cement_get_version(version)
