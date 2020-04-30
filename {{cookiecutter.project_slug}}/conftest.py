{% if cookiecutter.database != "NA" %}
import uuid

import pytest
from sqlalchemy import orm

from {{ cookiecutter.project_slug }}.app.py import models


@pytest.fixture(autouse=True)
def mock_session_factory():
    """
    A function scoped fixture that mocks models._SESSION_FACTORY to return a
    scoped session instead of plain session instance. This is to make sure that
    same session is used during lifetime of a single test function.

    This extends the recipe mentioned at below link:
    https://docs.sqlalchemy.org/en/13/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    engine = models.get_db_engine()
    connection = engine.connect()

    # Begin a non-ORM transaction
    transaction = connection.begin()

    session_factory = orm.sessionmaker(expire_on_commit=False)

    # By default scoped_session stores newly created session as thread local
    # data, which means the sessions are not accessible across threads. To
    # prevent this, we pass a scope function which always returns same ID to
    # hash the session instance.
    session_id = uuid.uuid1()
    scoped_session_factory = orm.scoped_session(
        session_factory, scopefunc=lambda: session_id
    )

    # Explicitly create a session and bind it to connection. This call will
    # create a new session instance and save in session registry and any further
    # requests for session will return the same session.
    _ = scoped_session_factory(bind=connection)

    # pylint: disable=protected-access
    models.SessionFactory._SESSION_FACTORY = scoped_session_factory

    # This will yield control to the test function.
    yield

    # Rollback any changes made to the database.
    transaction.rollback()
    connection.close()
    scoped_session_factory.remove()
{% endif %}
