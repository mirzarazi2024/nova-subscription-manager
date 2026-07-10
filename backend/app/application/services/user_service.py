from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user import UserSyncResultDTO
from app.db.models import User
from app.infrastructure.clients.hiddify_client import hiddify_client


class UserService:
    async def list_users(self, session: AsyncSession) -> list[User]:
        result = await session.execute(select(User).order_by(User.created_at.desc()))
        return list(result.scalars().all())

    async def sync_hiddify_users(self, session: AsyncSession) -> UserSyncResultDTO:
        remote_users = await hiddify_client.list_users()
        remote_ids: set[str] = set()
        created = 0
        updated = 0

        existing_result = await session.execute(select(User))
        existing = {user.hiddify_user_id: user for user in existing_result.scalars().all()}

        for item in remote_users:
            hiddify_id = self._extract_id(item)
            if not hiddify_id:
                continue
            remote_ids.add(hiddify_id)
            username = self._extract_username(item, hiddify_id)
            email = self._extract_email(item)

            if hiddify_id in existing:
                user = existing[hiddify_id]
                if user.username != username or user.email != email or not user.is_active:
                    user.username = username
                    user.email = email
                    user.is_active = True
                    updated += 1
            else:
                session.add(
                    User(
                        hiddify_user_id=hiddify_id,
                        username=username,
                        email=email,
                        role="user",
                        is_active=True,
                    )
                )
                created += 1

        disabled = 0
        for hiddify_id, user in existing.items():
            if hiddify_id not in remote_ids and user.is_active:
                user.is_active = False
                disabled += 1

        await session.commit()
        return UserSyncResultDTO(
            created=created,
            updated=updated,
            disabled=disabled,
            total_remote=len(remote_users),
        )

    @staticmethod
    def _extract_id(item: dict[str, Any]) -> str:
        for key in ("uuid", "id", "user_id", "secret_uuid"):
            value = item.get(key)
            if value:
                return str(value)
        return ""

    @staticmethod
    def _extract_username(item: dict[str, Any], fallback: str) -> str:
        for key in ("name", "username", "comment", "email"):
            value = item.get(key)
            if value:
                return str(value)
        return fallback

    @staticmethod
    def _extract_email(item: dict[str, Any]) -> str | None:
        value = item.get("email")
        return str(value) if value else None


user_service = UserService()
