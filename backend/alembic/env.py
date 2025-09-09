from dotenv import load_dotenv
import os

load_dotenv()  # loads DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

from models.base import Base
from models import user, problem, testcase, submission

target_metadata = Base.metadata  # ← important: your models' metadata

from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    url = DATABASE_URL  # use env variable
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)  # ← use env variable

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
