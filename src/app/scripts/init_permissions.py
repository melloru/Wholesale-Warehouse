import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.db_helper import db_helper
from core.config.permissions import PermissionEnum, RoleEnum
from users.infrastructure.database.models import (
    Permission as PermissionDb,
    Role as RoleDb,
    RolePermission as RolePermissionDb,
)


async def _create_permissions(session: AsyncSession) -> dict:
    """Создает все права в базе данных"""

    print("Создаю права доступа...")

    permissions_map = {}

    for permission in PermissionEnum.all():
        existing = await session.execute(
            select(PermissionDb).where(PermissionDb.code == permission.code)
        )

        if existing.scalar_one_or_none():
            print(f"Право '{permission.code}' уже существует, пропускаю")
            continue

        permission_db = PermissionDb(
            code=permission.code,
            description=permission.description,
        )
        session.add(permission_db)
        permissions_map[permission.code] = permission_db

    print(f"Создано {len(permissions_map)} прав")

    return permissions_map


async def _create_roles_with_permissions(
    session: AsyncSession,
    permissions_map: dict,
):
    print("👥 Создаю роли...")

    for role_enum in RoleEnum.all():
        existing = await session.execute(
            select(RoleDb).where(RoleDb.name == role_enum.role_name)
        )

        if existing.scalar_one_or_none():
            print(f"Роль '{role_enum.role_name}' уже существует, пропускаю")
            continue

        role_db = RoleDb(
            name=role_enum.role_name,
            description=role_enum.description,
        )

        session.add(role_db)
        await session.flush()

        role_permissions = role_enum.permissions()

        for permission_enum in role_permissions:
            if permission_enum.code in permissions_map:
                permission_db = permissions_map[permission_enum.code]
                role_permission = RolePermissionDb(
                    role_id=role_db.id,
                    permission_id=permission_db.id,
                )
                session.add(role_permission)

        if role_permissions:
            print(f"Роль '{role_db.name}' - {len(role_permissions)} прав")
        else:
            print(f"Роль '{role_db.name}' - без защищенных прав")


async def main():
    async for session in db_helper.get_session():
        permissions_map = await _create_permissions(session)
        await _create_roles_with_permissions(session, permissions_map)


if __name__ == "__main__":
    asyncio.run(main())
