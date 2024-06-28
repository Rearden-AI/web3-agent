import sys

from alembic import command
from alembic.config import Config


def make_and_apply_migrations(env_name):
    """
    Generate a new Alembic migration and apply it, based on the specified environment.

    Args:
        env_name (str): The name of the environment (e.g., 'dev', 'stage').
    """
    # Map the environment name to the Alembic configuration file
    config_files = {
        'dev': 'alembic_dev.ini',
        'stage': 'alembic_stage.ini',
        # Add more environments and their corresponding Alembic config files here
    }

    config_file = config_files.get(env_name)
    if not config_file:
        raise ValueError(f"Unknown environment: {env_name}")

    # Load the Alembic configuration and set the file path
    alembic_cfg = Config(config_file)

    # Generate a new revision with autogenerate
    command.revision(alembic_cfg, autogenerate=True, message=f"Auto-generated migration for {env_name}")

    # Apply migrations up to the latest revision
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 migration.py [env_name]")
        sys.exit(1)

    env_name = sys.argv[1]
    try:
        make_and_apply_migrations(env_name)
    except ValueError as e:
        print(e)
        sys.exit(1)
