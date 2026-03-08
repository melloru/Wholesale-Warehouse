from auth.domain.entities import UserSessionEntity
from auth.infrastructure.database.models import UserSession


class SessionMapper:
    @staticmethod
    def from_orm_to_entity(orm: UserSession) -> UserSessionEntity:
        return UserSessionEntity(
            id=orm.id,
            user_id=orm.user_id,
            refresh_token=orm.refresh_token,
            current_jti=orm.current_jti,
            exp=orm.exp,
            revoked=orm.revoked,
            revoked_at=orm.revoked_at,
            revoke_reason=orm.revoke_reason,
        )
