"""
License expiration background task.
Runs daily to check for expiring licenses and send alerts.
"""

import asyncio
import logging
from datetime import datetime

from app.core.database import db_manager
from app.services.license import ExpirationAlertService

logger = logging.getLogger(__name__)


async def check_license_expirations_task() -> None:
    """
    Background task to check for expiring licenses.
    Runs daily (scheduled via lifespan in main.py).
    """
    logger.info("Starting license expiration check task...")

    try:
        # Get database session
        async for session in db_manager.get_session():
            try:
                alert_service = ExpirationAlertService(session)

                # Check and get summary
                summary = await alert_service.check_and_notify()

                logger.info(
                    f"License expiration check completed. "
                    f"Found: {summary['alerts_30_days']} (30d), "
                    f"{summary['alerts_15_days']} (15d), "
                    f"{summary['alerts_7_days']} (7d), "
                    f"{summary['alerts_1_day']} (1d), "
                    f"{summary['expired']} expired"
                )

                # TODO: Integrate with NotificationService to send actual notifications
                # For now, just log the results
                if summary['alerts_1_day'] > 0 or summary['expired'] > 0:
                    logger.warning(
                        f"URGENT: {summary['alerts_1_day']} licenses expiring in 1 day, "
                        f"{summary['expired']} licenses already expired"
                    )

            except Exception as e:
                logger.error(f"Error in license expiration check: {e}", exc_info=True)
            finally:
                break  # Only use first session from generator

    except Exception as e:
        logger.error(f"Failed to get database session for expiration check: {e}", exc_info=True)


async def run_check_license_expirations() -> dict:
    """
    Manual trigger for license expiration check.
    Returns summary dict.
    """
    logger.info("Manual license expiration check triggered")

    try:
        async for session in db_manager.get_session():
            try:
                alert_service = ExpirationAlertService(session)
                summary = await alert_service.check_and_notify()
                return summary
            except Exception as e:
                logger.error(f"Error in manual expiration check: {e}", exc_info=True)
                raise
            finally:
                break
    except Exception as e:
        logger.error(f"Failed to get database session: {e}", exc_info=True)
        raise

