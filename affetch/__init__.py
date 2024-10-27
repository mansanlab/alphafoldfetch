from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('affetch')
except PackageNotFoundError:  # pragma: no cover
    __version__ = 'unknown'
finally:
    del version, PackageNotFoundError
