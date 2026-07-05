"""Mahu agent skill router."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mahu")
except PackageNotFoundError:  # pragma: no cover - source tree without install metadata
    __version__ = "0.0.0"

