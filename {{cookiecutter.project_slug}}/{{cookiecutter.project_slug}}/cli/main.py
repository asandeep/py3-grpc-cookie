import traceback

from cement import App, TestApp
from cement.core.exc import CaughtSignal

from {{ cookiecutter.project_slug }}.cli import exc
from {{ cookiecutter.project_slug }}.cli.controllers import base, client, server


class {{ cookiecutter.cement_app_name }}(App):
    """{{ cookiecutter.project_name }} main application."""

    class Meta:  # pylint: disable=missing-class-docstring
        label = "{{ cookiecutter.project_slug }}"

        # call sys.exit() on close
        exit_on_close = True

        # register handlers
        handlers = [base.Base, client.HelloworldClient, server.HelloworldServer]


class {{ cookiecutter.cement_app_name }}Test(TestApp, {{ cookiecutter.cement_app_name }}):
    """A sub-class of {{ cookiecutter.cement_app_name }} that is better suited for testing."""

    class Meta:  # pylint: disable=missing-class-docstring
        label = "{{ cookiecutter.project_slug }}"


def main():  # pylint: disable=missing-function-docstring
    with {{ cookiecutter.cement_app_name }}() as app:
        try:
            app.run()

        except AssertionError as assertion_error:
            print("AssertionError > %s" % assertion_error.args[0])
            app.exit_code = 1

            if app.debug is True:
                traceback.print_exc()

        except exc.{{ cookiecutter.cement_app_name }}Error as app_error:
            print("{{ cookiecutter.cement_app_name }}Error > %s" % app_error.args[0])
            app.exit_code = 1

            if app.debug is True:
                traceback.print_exc()

        except CaughtSignal as caught_signal:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % caught_signal)
            app.exit_code = 0


if __name__ == "__main__":
    main()
