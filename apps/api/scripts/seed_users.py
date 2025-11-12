"""
Seed script to create initial users for testing.
Run with: python -m scripts.seed_users
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.database import Base, db_manager
from app.db.models.user import User, UserRole


async def seed_users() -> None:
    """Create seed users for testing."""
    print("[*] Starting user seed...")

    # Create tables if they don't exist
    async with db_manager.write_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] Tables created/verified")

    # Users to create
    seed_users_data = [
        # Admins
        {
            "email": "admin@contabil.com",
            "password": "admin123",
            "name": "Administrador Sistema",
            "role": UserRole.ADMIN,
            "is_verified": True,
        },
        {
            "email": "admin2@contabil.com",
            "password": "admin123",
            "name": "Maria Santos - Admin",
            "role": UserRole.ADMIN,
            "is_verified": True,
        },
        # Funcionários
        {
            "email": "func@contabil.com",
            "password": "func123",
            "name": "João Silva - Contador",
            "role": UserRole.FUNC,
            "is_verified": True,
        },
        {
            "email": "func2@contabil.com",
            "password": "func123",
            "name": "Ana Paula Costa - Assistente",
            "role": UserRole.FUNC,
            "is_verified": True,
        },
        {
            "email": "func3@contabil.com",
            "password": "func123",
            "name": "Pedro Henrique Oliveira - Analista Fiscal",
            "role": UserRole.FUNC,
            "is_verified": True,
        },
        # Clientes (serão vinculados aos clientes reais)
        {
            "email": "contato@techsolutions.com",
            "password": "cliente123",
            "name": "Roberto Costa - Tech Solutions",
            "role": UserRole.CLIENTE,
            "is_verified": False,
        },
        {
            "email": "comercial@supermercadoboa.com",
            "password": "cliente123",
            "name": "Sandra Ferreira - Supermercado Boa Esperança",
            "role": UserRole.CLIENTE,
            "is_verified": False,
        },
        {
            "email": "admin@restaurantegirassol.com",
            "password": "cliente123",
            "name": "José Antonio Lima - Restaurante Girassol",
            "role": UserRole.CLIENTE,
            "is_verified": True,
        },
        {
            "email": "financeiro@construtoranovavida.com",
            "password": "cliente123",
            "name": "Marcos Pereira - Construtora Nova Vida",
            "role": UserRole.CLIENTE,
            "is_verified": True,
        },
        {
            "email": "contato@belezaecia.com",
            "password": "cliente123",
            "name": "Juliana Martins - Beleza & Cia",
            "role": UserRole.CLIENTE,
            "is_verified": False,
        },
    ]

    # Insert users
    async with db_manager.session_factory() as session:
        for user_data in seed_users_data:
            # Check if user already exists
            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"[SKIP] User {user_data['email']} already exists, skipping...")
                continue

            # Create new user
            user = User(
                email=user_data["email"],
                name=user_data["name"],
                role=user_data["role"],
                is_active=True,
                is_verified=user_data["is_verified"],
            )
            user.set_password(user_data["password"])
            session.add(user)
            print(f"[OK] Created user: {user_data['email']} (role: {user_data['role'].value})")

        await session.commit()

    print("\n[SUCCESS] Seed completed successfully!")
    print("\n[INFO] Test Users Created:")
    print("=" * 70)
    for user_data in seed_users_data:
        print(f"Email: {user_data['email']:<30} | Password: {user_data['password']:<15} | Role: {user_data['role'].value}")
    print("=" * 70)


async def main() -> None:
    """Main function."""
    try:
        await seed_users()
    except Exception as e:
        print(f"\n[ERROR] Error during seed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        # Close database connections
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
