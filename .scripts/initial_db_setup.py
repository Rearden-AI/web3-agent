# from app.core.models import Role
from app.core.models.db_helper import db_helper


async def create_roles(session):
    ...
    # new_roles = [
    #     Role(
    #         name="admin",
    #         projects_quota=100, proofs_daily_quota=100,
    #         demos_hourly_quota=100, events_hourly_quota=1000000
    #     ),
    #     Role(
    #         name="user",
    #         projects_quota=20, proofs_daily_quota=20,
    #         demos_hourly_quota=20, events_hourly_quota=100000
    #     ),
    #     Role(
    #         name="dev",
    #         projects_quota=100, proofs_daily_quota=1000,
    #         demos_hourly_quota=1000, events_hourly_quota=1000000
    #     ),
    #     Role(
    #         name="tester",
    #         projects_quota=1000, proofs_daily_quota=1000,
    #         demos_hourly_quota=1000, events_hourly_quota=100000000
    #     ),
    # ]
    # session.add_all(new_roles)
    # await session.commit()
    #
    # print("Roles created!")


async def main():
    # Example roles
    session = db_helper.get_scoped_session()
    try:
        await create_roles(session)
    except Exception as e:
        print(e)
    await session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
