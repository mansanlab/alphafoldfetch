from importlib.metadata import PackageNotFoundError, version

__version__: str

try:
    __version__ = version("affetch")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

__all__ = ["__version__"]
