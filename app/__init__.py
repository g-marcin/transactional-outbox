import logging

__version__ = "0.1.0"

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s] %(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)

logger.info(f"Initializing transactional-outbox app v{__version__}")
