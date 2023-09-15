import logging
from datetime import datetime
from pathlib import Path

from decouple import config
from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware

from jwt_utils import decode_jwt, generate_jwt

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Retrieve and validate environment variables
SECRET_KEY = config("SECRET_KEY")
CLIENT_PRIVATE_KEY = Path(config("CLIENT_PRIVATE_KEY", ""))
assert (
    CLIENT_PRIVATE_KEY.exists() and not CLIENT_PRIVATE_KEY.is_dir()
), "Invalid CLIENT_PRIVATE_KEY path"
SERVER_PUBLIC_KEY = Path(config("SERVER_PUBLIC_KEY", ""))
assert (
    SERVER_PUBLIC_KEY.exists() and not SERVER_PUBLIC_KEY.is_dir()
), "Invalid SERVER_PUBLIC_KEY path"
AUTH_SERVER = config("AUTH_SERVER")
JWT_ACCESS_TOKEN_EXPIRES_MINUTES = int(config("JWT_ACCESS_TOKEN_EXPIRES_MINUTES"))

# Add session middleware for cookie management
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=60 * 60 * 24 * 7,  # 1 week in seconds
)


async def get_current_user(request: Request):
    """Retrieve the current user from the session."""
    if "authenticated" in request.session and request.session["authenticated"]:
        return request.session["decoded_token"]


async def authenticate(
    request: Request, token: str = None, user=Depends(get_current_user)
):
    """Authenticate the user, if not already authenticated and token is not provided."""
    if user or token:
        return user

    logger.info("Authenticating...")

    with open(CLIENT_PRIVATE_KEY, "rb") as file:
        private_key_content = file.read()

    data = {"app_id": "testapp1", "redirect_url": f"{request.url}"}
    jwt_token = generate_jwt(
        data, private_key_content, JWT_ACCESS_TOKEN_EXPIRES_MINUTES
    )

    raise HTTPException(
        status_code=302,
        headers={"Location": f"{AUTH_SERVER}/authenticate?token={jwt_token}"},
    )


async def validate_token(
    request: Request, token: str = None, user=Depends(authenticate)
):
    """Validate the JWT and set the session if token is valid."""
    if user:
        return user

    logger.info("Validating token...")

    with open(SERVER_PUBLIC_KEY, "rb") as file:
        public_key_content = file.read()

    decoded_token = decode_jwt(token, public_key_content)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    request.session["authenticated"] = True
    request.session["decoded_token"] = decoded_token
    raise HTTPException(status_code=302, headers={"Location": f"{request.url}"})


@app.get("/")
async def read_root():
    """Return the current UNIX timestamp."""
    logger.info("Read root endpoint")
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": f"{unix_timestamp}"}


@app.get("/protected")
async def protected(token: str = None, user=Depends(validate_token)):
    """Return the current UNIX timestamp and user ID if user is authenticated."""
    logger.info("Read protected route")
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": f"{unix_timestamp}", "current_user": f'{user["sub"]}'}
