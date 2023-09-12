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
docker run -d -p <EXTERNAL_PORT>:<INTERNAL_PORT> -e PORT=<INTERNAL_PORT> fastapi-app
```
- <EXTERNAL_PORT>: The port on your machine/host you want to access the app through.
- <INTERNAL_PORT>: The port inside the Docker container (set in the `Dockerfile`).
3. Visit `http://localhost:<EXTERNAL_PORT>/` in your browser to see the current Unix timestamp returned by the FastAPI app.
4. Access the API Swagger docs at `http://localhost:<EXTERNAL_PORT>/docs`.


### Customizing ASGI Server

The project currently uses uvicorn as its ASGI server, as specified in the `requirements.txt` file. If you wish to use another ASGI server like `hypercorn` or `daphne`, simply update the `requirements.txt` file and modify the startup command accordingly in the `devcontainer.json` file and the `Dockerfile`. Make sure the server you choose is compatible with FastAPI.

