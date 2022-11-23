"""Set git SHA value for displaying in footer."""

import environ


def get_git_sha():
    """Return git SHA value for displaying in footer.

    Returns:
        String value to display.
    """
    env = environ.Env()
    return env("GIT_SHA", default=None) or "local development"
