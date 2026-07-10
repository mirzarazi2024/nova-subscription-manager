from collections import Counter
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.subscription import (
    SubscriptionCreateDTO,
    SubscriptionPreviewRequest,
    SubscriptionPreviewResponse,
)
from app.db.models import Provider, Subscription, User
from app.domain.services.merge_engine import NormalizedNode, merge_engine
from app.infrastructure.clients.hiddify_client import hiddify_client


class SubscriptionService:
    async def list_subscriptions(self, session: AsyncSession) -> list[Subscription]:
        result = await session.execute(select(Subscription).order_by(Subscription.created_at.desc()))
        return list(result.scalars().all())

    async def create_subscription(self, session: AsyncSession, payload: SubscriptionCreateDTO) -> Subscription:
        user = await session.get(User, payload.user_id)
        if user is None:
            raise ValueError("User not found")

        existing_result = await session.execute(select(Subscription).where(Subscription.user_id == user.id))
        existing = existing_result.scalar_one_or_none()
        if existing:
            return existing

        sub_uuid = str(uuid4())
        source_url: str | None = None
        try:
            source_url = await hiddify_client.get_user_subscription(user.hiddify_user_id)
        except Exception:
            source_url = None

        subscription = Subscription(
            user_id=user.id,
            uuid=sub_uuid,
            source_hiddify_url=source_url,
            nova_url=f"https://sub.novavpn.com/{sub_uuid}",
            format=payload.format,
            is_active=True,
            preview_summary={},
        )
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)
        return subscription

    async def preview_subscription(
        self, session: AsyncSession, payload: SubscriptionPreviewRequest
    ) -> SubscriptionPreviewResponse:
        providers_result = await session.execute(select(Provider).where(Provider.id.in_(payload.provider_ids)))
        providers = list(providers_result.scalars().all())

        hiddify_nodes = [
            NormalizedNode(
                protocol="vless",
                server="hiddify.example.com",
                port=443,
                uuid=payload.user_id,
                public_key="pk",
                sni="hiddify.example.com",
                transport="tcp",
                source="hiddify",
            )
        ]

        provider_nodes: list[NormalizedNode] = []
        provider_count = Counter()
        for provider in providers:
            node = NormalizedNode(
                protocol="vless",
                server=f"{provider.name.lower()}.provider.net",
                port=443,
                uuid=payload.user_id,
                public_key="pk2",
                sni="provider.net",
                transport="ws",
                source=provider.id,
            )
            provider_nodes.append(node)
            provider_count[provider.name] += 1

        merged, duplicates = merge_engine.merge(hiddify_nodes, provider_nodes)
        rules_removed = 0
        final_nodes = max(len(merged) - rules_removed, 0)

        return SubscriptionPreviewResponse(
            hiddify_nodes=len(hiddify_nodes),
            provider_nodes=dict(provider_count),
            duplicates_removed=duplicates,
            rules_removed=rules_removed,
            final_nodes=final_nodes,
        )


subscription_service = SubscriptionService()
