# FastAPI with VSCode Dev Containers

This project showcases a FastAPI application developed within a VSCode Dev Container.

The FastAPI application provides a simple endpoint at the root (`/`) that returns the current Unix timestamp. You can access the API Swagger documentation by navigating to the `/docs` endpoint.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [VSCode](https://code.visualstudio.com/)
- [VSCode Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Steps to Run the Project from Dev Containers

1. Open the project in VSCode.
2. When prompted, open the project inside the container. (Or press `F1`, type `Remote-Containers: Reopen in Container`).
3. Once inside the container, open VSCode Terminal at the root of the project and run these commands:

```
cd src
uvicorn main:app --port <PORT>
```

This will start the FastAPI application, and you can access it on port <PORT>

4. Visit `http://localhost:<PORT>` in your browser to see the current Unix timestamp returned by the FastAPI app.
5. Access the API Swagger docs at `http://localhost:<PORT>/docs`.

### Running the unit tests from Dev Containers

Open a VsCode Terminal at the root of the project and run:

```bash
python -m unittest discover -s tests
```

### Steps to Run the Project from Dockerfile

1. Open the project in VSCode.
2. Open a VSCode Terminal at the root of the project. Then run these commands:
   ```bash
   docker build -t fastapi-app .
   docker run -d -p <EXTERNAL_PORT>:<INTERNAL_PORT> fastapi-app
   ```

- <EXTERNAL_PORT>: The port on your machine/host you want to access the app through.
- <INTERNAL_PORT>: The port inside the Docker container (set in the `Dockerfile`).

3. Visit `http://localhost:<EXTERNAL_PORT>/` in your browser to see the current Unix timestamp returned by the FastAPI app.
4. Access the API Swagger docs at `http://localhost:<EXTERNAL_PORT>/docs`.

### Customizing ASGI Server

The project currently uses uvicorn as its ASGI server, as specified in the `requirements.txt` file. If you wish to use another ASGI server like `hypercorn` or `daphne`, simply update the `requirements.txt` file and modify the startup command accordingly in the `devcontainer.json` file and the `Dockerfile`. Make sure the server you choose is compatible with FastAPI.

### Manual Testing of the Protected Route

#### Setting Up the Environment

To perform manual tests, both `louis-login-backend` and `fastapi-example` should be operational.

##### Getting `louis-login-backend` Up and Running

1. Create a `.env` file in the root directory of `louis-login-backend` if not present.
2. Populate `.env` with the following variables:
   ```text
   ALLOWED_EMAIL_DOMAINS=example.com
   SECRET_KEY=super_secret
   JWT_ACCESS_TOKEN_EXPIRES_MINUTES=2
   SESSION_TYPE=filesystem
   CLIENT_PUBLIC_KEYS_DIRECTORY=tests/client_public_keys
   SERVER_PRIVATE_KEY=tests/server_private_key/server_private_key.pem
   SERVER_PUBLIC_KEY=tests/server_public_key/server_public_key.pem
   SESSION_LIFETIME_MINUTES=4
   REDIRECT_URL_TO_LOUIS_FRONTEND=http://localhost:<fastapi-example-port>/email_form
   ```
3. Start the service:
   ```shell
   flask run --port=<louis-login-port>
   ```

##### Getting `fastapi-example` Up and Running

1. Copy the `tests` folder from `louis-login-backend` into the `src` folder in `fastapi-example` and rename it `keys`.
2. Create a `.env` file in the `src` folder of `fastapi-example`, and populate it:
   ```text
   SECRET_KEY=ultra_secret
   JWT_ACCESS_TOKEN_EXPIRES_MINUTES=2
   CLIENT_PRIVATE_KEY=keys/client_private_keys/testapp1_private_key.pem
   SERVER_PUBLIC_KEY=keys/server_public_key/server_public_key.pem
   AUTH_SERVER=http://localhost:<louis-login-port>
   ```
3. Run `fastapi-example`:
   ```shell
   cd src
   uvicorn main:app --port=<fastapi-example-port>
   ```

#### Manual Testing Procedure

1. Open a web browser and go to `localhost:<fastapi-example-port>/protected`.
2. You'll be prompted to enter an email. Use an email address that matches the domain specified in the `.env` of `louis-login-backend` (e.g., `user@example.com`). Click 'Submit'.
3. `louis-login-backend` should log a redirect URL. Copy this URL.
4. Paste the copied URL into your web browser.
5. You should now have access to the protected route.

