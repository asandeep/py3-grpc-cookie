from sqlalchemy import schema
from sqlalchemy.ext import declarative

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult.
# See: http://alembic.zzzcomputing.com/en/latest/naming.html &
#      https://docs.sqlalchemy.org/en/13/core/constraints.html#constraint-naming-conventions  #pylint: disable=line-too-long
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

METADATA = schema.MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative.declarative_base(  # pylint: disable=invalid-name
    metadata=METADATA
)
