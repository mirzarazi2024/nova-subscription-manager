from collections import Counter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.subscription import SubscriptionPreviewRequest, SubscriptionPreviewResponse
from app.db.models import Provider
from app.domain.services.merge_engine import NormalizedNode, merge_engine


class SubscriptionService:
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
