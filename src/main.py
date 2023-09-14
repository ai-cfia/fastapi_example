import os
from datetime import datetime
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from starlette.middleware.sessions import SessionMiddleware

from environment_validation import validate_environment_settings
from jwt_utils import decode_jwt, generate_jwt

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Retrieve and validate environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
CLIENT_PRIVATE_KEY = Path(os.getenv("CLIENT_PRIVATE_KEY", ""))
SERVER_PUBLIC_KEY = Path(os.getenv("SERVER_PUBLIC_KEY", ""))
AUTH_SERVER = os.getenv("AUTH_SERVER")
JWT_ACCESS_TOKEN_EXPIRES_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30)
)
validate_environment_settings(
    SECRET_KEY, CLIENT_PRIVATE_KEY, SERVER_PUBLIC_KEY, AUTH_SERVER
)

# Add session middleware for cookie management
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=60 * 60 * 24 * 7,  # 1 week in seconds
)


async def get_current_user(request: Request):
    """
    Retrieve the current user from the session.
    """
    if "authenticated" in request.session and request.session["authenticated"]:
        print(f"found user {request.session['decoded_token']}")
        return request.session["decoded_token"]


async def authenticate(
    request: Request, token: str = None, user=Depends(get_current_user)
):
    """
    Authenticate the user, if not already authenticated and token is not provided.
    """
    if user or token:
        return user

    print("authenticating...")
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
    """
    Validate the JWT and set the session if token is valid.
    """
    if user:
        return user

    print("validating token...")
    with open(SERVER_PUBLIC_KEY, "rb") as file:
        public_key_content = file.read()

    decoded_token = decode_jwt(token, public_key_content)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    request.session["authenticated"] = True
    request.session["decoded_token"] = decoded_token
    raise HTTPException(
        status_code=302,
        headers={"Location": f"{request.url}"},
    )


@app.get("/")
async def read_root():
    """
    Return the current UNIX timestamp.
    """
    print("read root")
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": f"{unix_timestamp}"}


@app.get("/protected")
async def protected(
    token: Annotated[str | None, Query(...)] = None, user=Depends(validate_token)
):
    """
    Return the current UNIX timestamp and user ID, but only if user is authenticated.
    """
    print("read protected route")
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": f"{unix_timestamp}", "current_user": f'{user["sub"]}'}