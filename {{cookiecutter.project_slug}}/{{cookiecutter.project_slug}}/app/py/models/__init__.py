from contextlib import contextmanager

from dynaconf import settings
from sqlalchemy import create_engine, orm
from sqlalchemy.engine import url as engine_url

# Import models here.


def get_db_url():
    """Returns the SQLAlchemy URL object for DB connection."""

    return engine_url.URL(
        drivername=settings.DB_DIALECT,
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT or None,
        database=settings.DB_NAME,
    )


def get_db_engine(**kwargs):
    """Initializes and returns a new engine to interact with backend DB."""

    return create_engine(
        get_db_url(), echo=settings.DEBUG, echo_pool=settings.DEBUG, **kwargs
    )


class SessionFactory:
    """A convenience wrapper over SQLAlchemy orm.sessionmaker instance"""

    _SESSION_FACTORY: orm.session.Session = None

    @classmethod
    def _session_factory(cls):
        """Returns an instance of SQLAlchemy `orm.sessionmaker`.

        A new `orm.sessionmaker` instance will be initialized on first call. The
        instance will be cached for subsequent calls.
        """
        if not cls._SESSION_FACTORY:
            db_engine = get_db_engine()
            cls._SESSION_FACTORY = orm.sessionmaker(
                bind=db_engine, expire_on_commit=False
            )

        return cls._SESSION_FACTORY

    @classmethod
    @contextmanager
    def get_session(cls):
        """Returns a SQLAlchemy session context manager."""

        session = cls._session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
