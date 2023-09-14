from pathlib import Path


def validate_environment_settings(
    SECRET_KEY: str, CLIENT_PRIVATE_KEY: Path, SERVER_PUBLIC_KEY: Path, AUTH_SERVER: str
):
    """
    Validate the environment settings.

    Args, Returns, Raises: (as before)
    """

    if not SECRET_KEY:
        raise ValueError(
            "SECRET_KEY is not set. Please set the SECRET_KEY environment variable."
        )

    error_msg_template = "The specified {} file {} does not exist or is a directory."

    if not CLIENT_PRIVATE_KEY.exists() or CLIENT_PRIVATE_KEY.is_dir():
        raise ValueError(
            error_msg_template.format("client private key", CLIENT_PRIVATE_KEY)
        )

    if not SERVER_PUBLIC_KEY.exists() or SERVER_PUBLIC_KEY.is_dir():
        raise ValueError(
            error_msg_template.format("server public key", SERVER_PUBLIC_KEY)
        )

    if not AUTH_SERVER:
        raise ValueError("AUTH_SERVER is not set.")

    return True
