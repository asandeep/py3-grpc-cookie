import pytest

from {{ cookiecutter.project_slug }}.cli.main import {{ cookiecutter.cement_app_name }}Test


@pytest.mark.no_cover
def test_sentieoozone():
    # test {{ cookiecutter.project_slug }} without any subcommands or arguments
    with {{ cookiecutter.cement_app_name }}Test() as app:
        app.run()
        assert app.exit_code == 0


@pytest.mark.no_cover
def test_sentieoozone_debug():
    # test that debug mode is functional
    argv = ["--debug"]
    with {{ cookiecutter.cement_app_name }}Test(argv=argv) as app:
        app.run()
        assert app.debug is True
