import logging

from . import health, orders

logger = logging.getLogger(__name__)
logger.info("API module initialized with routes: health, orders")

__all__ = ["health", "orders"]
