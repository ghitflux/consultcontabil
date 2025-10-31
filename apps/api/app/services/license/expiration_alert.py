"""
License expiration alert service.
"""

from datetime import date, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.license import LicenseRepository
from app.db.repositories.client import ClientRepository
from app.schemas.license import LicenseResponse, LicenseStatus


class ExpirationAlertService:
    """Service for managing license expiration alerts."""

    def __init__(self, session: AsyncSession):
        """
        Initialize expiration alert service.

        Args:
            session: Database session
        """
        self.session = session
        self.license_repo = LicenseRepository(session)
        self.client_repo = ClientRepository(session)

    async def get_expiring_licenses(self, days: int = 30) -> list[LicenseResponse]:
        """
        Get licenses expiring within specified days.

        Args:
            days: Number of days to look ahead (default: 30)

        Returns:
            List of licenses expiring soon
        """
        licenses = await self.license_repo.get_expiring_soon(days)

        today = date.today()
        results = []

        for lic in licenses:
            days_until = None
            is_expired = False
            is_expiring_soon = False

            if lic.expiration_date:
                days_until = (lic.expiration_date - today).days
                is_expired = days_until < 0
                is_expiring_soon = 0 <= days_until <= 30

            results.append(
                LicenseResponse(
                    id=lic.id,
                    client_id=lic.client_id,
                    license_type=lic.license_type,
                    registration_number=lic.registration_number,
                    issuing_authority=lic.issuing_authority,
                    issue_date=lic.issue_date,
                    expiration_date=lic.expiration_date,
                    status=lic.status,
                    notes=lic.notes,
                    document_id=lic.document_id,
                    created_at=lic.created_at,
                    updated_at=lic.updated_at,
                    days_until_expiration=days_until,
                    is_expired=is_expired,
                    is_expiring_soon=is_expiring_soon,
                )
            )

        return results

    async def check_and_notify(self) -> dict:
        """
        Check for expiring licenses and return summary.
        This method does not send notifications directly but returns data
        that can be used to send notifications via NotificationService.

        Returns:
            Dictionary with alert summary
        """
        today = date.today()

        # Check licenses expiring at different thresholds
        alerts_30_days = await self._get_licenses_by_threshold(30)
        alerts_15_days = await self._get_licenses_by_threshold(15)
        alerts_7_days = await self._get_licenses_by_threshold(7)
        alerts_1_day = await self._get_licenses_by_threshold(1)
        expired = await self.license_repo.get_expired()

        # Build summary
        summary = {
            "checked_at": today.isoformat(),
            "alerts_30_days": len(alerts_30_days),
            "alerts_15_days": len(alerts_15_days),
            "alerts_7_days": len(alerts_7_days),
            "alerts_1_day": len(alerts_1_day),
            "expired": len(expired),
            "licenses_30_days": [self._to_alert_dict(lic) for lic in alerts_30_days],
            "licenses_15_days": [self._to_alert_dict(lic) for lic in alerts_15_days],
            "licenses_7_days": [self._to_alert_dict(lic) for lic in alerts_7_days],
            "licenses_1_day": [self._to_alert_dict(lic) for lic in alerts_1_day],
            "licenses_expired": [self._to_alert_dict(lic) for lic in expired],
        }

        return summary

    async def _get_licenses_by_threshold(self, days: int) -> list:
        """
        Get licenses expiring within exact threshold (not already checked).

        Args:
            days: Number of days

        Returns:
            List of licenses
        """
        licenses = await self.license_repo.get_expiring_soon(days)
        today = date.today()

        # Filter by exact threshold
        threshold_date = today + timedelta(days=days)
        filtered = []

        for lic in licenses:
            if lic.expiration_date and lic.expiration_date <= threshold_date:
                # Check if we should alert (not too early)
                days_until = (lic.expiration_date - today).days
                if days == 1 and days_until == 1:
                    filtered.append(lic)
                elif days == 7 and 1 < days_until <= 7:
                    filtered.append(lic)
                elif days == 15 and 7 < days_until <= 15:
                    filtered.append(lic)
                elif days == 30 and 15 < days_until <= 30:
                    filtered.append(lic)

        return filtered

    def _to_alert_dict(self, license_obj) -> dict:
        """
        Convert license to alert dictionary.

        Args:
            license_obj: License model

        Returns:
            Alert dictionary
        """
        today = date.today()
        days_until = None
        if license_obj.expiration_date:
            days_until = (license_obj.expiration_date - today).days

        # Get client name if available
        client_name = None
        try:
            # This would require eager loading in repository, simplified here
            pass
        except:
            pass

        return {
            "license_id": str(license_obj.id),
            "client_id": str(license_obj.client_id),
            "license_type": license_obj.license_type,
            "registration_number": license_obj.registration_number,
            "issuing_authority": license_obj.issuing_authority,
            "expiration_date": license_obj.expiration_date.isoformat() if license_obj.expiration_date else None,
            "days_until_expiration": days_until,
            "client_name": client_name,
        }

