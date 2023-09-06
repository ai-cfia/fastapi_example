# FastAPI with VSCode Dev Containers

This project showcases a FastAPI application developed within a VSCode Dev Container.

The FastAPI application provides a simple endpoint at the root (`/`) that returns the current Unix timestamp. You can access the API Swagger documentation by navigating to the `/docs` endpoint.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [VSCode](https://code.visualstudio.com/)
- [VSCode Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Steps to Run the Project

1. Open the project in VSCode.
2. When prompted, open the project inside the container. (Or press `F1`, type `Remote-Containers: Reopen in Container`).
3. Once inside the container, VSCode will automatically bind the project directory and forward port `5001` for the FastAPI application.
4. Visit [Localhost:5001](http://localhost:5001/) in your browser to see the current Unix timestamp returned by the FastAPI app.
5. Access the API Swagger docs [here](http://localhost:5001/docs).

### Manually Running the App (If Needed)

While inside the VSCode terminal connected to the container:

```bash
cd /workspaces/fastapi_example/src
python main.py
```
This will start the FastAPI application, and you can access it on port 5001.