from loguru import logger
from sqlalchemy import select

from app.application.services.provider_service import provider_service
from app.db.models import Provider
from app.db.session import AsyncSessionFactory


async def provider_refresh_job() -> None:
    logger.info("Running provider refresh job")
    async with AsyncSessionFactory() as session:
        result = await session.execute(select(Provider).where(Provider.enabled.is_(True)))
        providers = list(result.scalars().all())
        for provider in providers:
            try:
                await provider_service.refresh_provider(session, provider)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Provider refresh failed for {}: {}", provider.name, exc)
