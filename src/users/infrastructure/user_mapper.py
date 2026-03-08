from users.domain.entities import UserEntity
from users.infrastructure.database.models import User


class UserMapper:
    """Конвертирует ORM <-> Entity"""

    @staticmethod
    def from_orm_to_entity(orm: User) -> UserEntity:
        return UserEntity(
            id=orm.id,
            role_id=orm.role_id,
            email=orm.email,
            password_hash=orm.password_hash,
            first_name=orm.first_name,
            last_name=orm.last_name,
            public_name=orm.public_name,
            phone_number=orm.phone_number,
            phone_verified=orm.phone_verified,
            email_verified=orm.email_verified,
            status=orm.status,
        )
