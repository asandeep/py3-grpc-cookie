from cement import Controller
from cement.utils.version import get_version_banner

from {{ cookiecutter.project_slug }}.cli import version

VERSION_BANNER = f"""
{{ cookiecutter.project_short_description }} {version.get_version()}
{get_version_banner()}
"""


# pylint: disable=too-many-ancestors,missing-class-docstring
class Base(Controller):
    class Meta:  # pylint: disable=missing-class-docstring
        label = "base"

        # text displayed at the top of --help output
        description = "{{ cookiecutter.project_short_description }}"

        # text displayed at the bottom of --help output
        epilog = "Usage: {{ cookiecutter.project_slug }} command1 --foo bar"

        # controller level arguments. ex: '{{ cookiecutter.project_slug }} --version'
        arguments = [
            ### add a version banner
            (
                ["-v", "--version"],
                {"action": "version", "version": VERSION_BANNER},
            )
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()
