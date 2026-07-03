from datetime import UTC, datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.provider import ProviderCreateDTO
from app.db.models import Provider
from app.plugins.parsers.registry import parser_registry


class ProviderService:
    async def create_provider(self, session: AsyncSession, payload: ProviderCreateDTO) -> Provider:
        provider = Provider(**payload.model_dump(), url=str(payload.url))
        session.add(provider)
        await session.commit()
        await session.refresh(provider)
        return provider

    async def list_providers(self, session: AsyncSession) -> list[Provider]:
        result = await session.execute(select(Provider).order_by(Provider.scoring_total.desc(), Provider.priority.desc()))
        return list(result.scalars().all())

    async def refresh_provider(self, session: AsyncSession, provider: Provider) -> dict[str, int]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(provider.url)
            response.raise_for_status()
            payload = response.text

        nodes = parser_registry.detect_and_parse(payload)
        total = len(nodes)
        healthy = int(total * 0.9)
        dead = max(total - healthy, 0)

        provider.status = "healthy" if healthy else "degraded"
        provider.last_update_at = datetime.now(UTC)

        provider.scoring_speed = min(100.0, 10000.0 / max(provider.update_interval_seconds, 1))
        provider.scoring_healthy_nodes = float(healthy)
        provider.scoring_dead_ratio = (dead / total * 100.0) if total else 100.0
        provider.scoring_response_time = 100.0
        provider.scoring_error_rate = 0.0
        provider.scoring_total = (
            provider.scoring_speed * 0.15
            + provider.scoring_healthy_nodes * 0.35
            + (100.0 - provider.scoring_dead_ratio) * 0.2
            + provider.scoring_response_time * 0.2
            + (100.0 - provider.scoring_error_rate) * 0.1
        )

        await session.commit()
        return {"total": total, "healthy": healthy, "dead": dead}


provider_service = ProviderService()
