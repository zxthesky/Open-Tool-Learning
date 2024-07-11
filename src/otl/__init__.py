
from src.otl._version import __version__
from src.otl.utils._log import setup_logging as _setup_logging
logger = _setup_logging()

__all__ = [
    "__version__",
]



logger.info("Open Tool Learning (otl) initialization is completed.")