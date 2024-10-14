
# Sci-ACSS Integration Services

This project sets up two services (`sic_service` and `acss_service`) along with their respective PostgreSQL databases using Docker Compose. Follow the instructions below to set up and run the services on your local machine.

## Prerequisites

Before you start, make sure you have the following installed:

- [Docker](https://www.docker.com/get-started) (version 20.10+ recommended)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29+ recommended)
- [Node.js](https://nodejs.org/) (version 14+ recommended)
- [npm](https://www.npmjs.com/)

## Project Structure

The project is structured as follows:

```
.
├── docker-compose.yml
├── sic-service/
│   ├── Dockerfile
│   └── ... (other app files)
├── acss-service/
│   ├── Dockerfile
│   └── ... (other app files)
├── db-data/
│   ├── postgres_sic/
│   └── postgres_acss/
└── sci-acss-integrate-frontend/
    ├── package.json
    └── ... (other frontend files)
```

## Services Overview

1. **sic_service**: A backend service built with FastAPI that connects to `postgres_db_sic`.
2. **acss_service**: Another backend service built with FastAPI that connects to `postgres_db_acss`.
3. **postgres_db_sic**: A PostgreSQL database for `sic_service`.
4. **postgres_db_acss**: A PostgreSQL database for `acss_service`.

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Build and Run Services Using Docker Compose

To build and start all services, navigate to the root directory where `docker-compose.yml` is located and run:

```bash
docker-compose up -d
```

The `-d` flag runs the services in detached mode. You can omit this flag to run in the foreground and see the logs directly in the terminal.

### 3. Verify Services

Once the services are up, you can verify they are running correctly:

- **SIC Service**: Open your browser and navigate to [http://localhost:8000](http://localhost:8000)
- **ACSS Service**: Open your browser and navigate to [http://localhost:8001](http://localhost:8001)

To check the logs of any service, use:

```bash
docker-compose logs <service-name>
```

For example:

```bash
docker-compose logs sic_service
```

### 4. Frontend Setup

The frontend application is located in the `sci-acss-integrate-frontend` directory. Follow these steps to set up and run the frontend:

1. **Navigate to the frontend directory**:

    ```bash
    cd sci-acss-integrate-frontend
    ```

2. **Install dependencies**:

    ```bash
    npm install
    ```

3. **Run the development server**:

    ```bash
    npm run dev
    ```

The frontend server should now be running, and you can access it at [http://localhost:3000](http://localhost:3000).

## Environment Variables

Make sure to update the environment variables in the `docker-compose.yml` file if needed. Here are the variables you might want to configure:

### For `sic_service`:

- `DATABASE_URL`: Connection URL for the PostgreSQL database.
- `JWT_SECRET_KEY`: Secret key for JSON Web Token (JWT) authentication.

### For `acss_service`:

- `DATABASE_URL`: Connection URL for the PostgreSQL database.
- `JWT_SECRET_KEY`: Secret key for JSON Web Token (JWT) authentication.

### For PostgreSQL Databases:

- `POSTGRES_USER`: Database username.
- `POSTGRES_PASSWORD`: Database password.
- `POSTGRES_DB`: Database name.

## Stopping Services

To stop all services, run:

```bash
docker-compose down
```

This will stop and remove the containers but will retain the volumes (database data). If you want to remove everything, including volumes, run:

```bash
docker-compose down -v
```

## Useful Commands

- **Rebuild services**: If you make changes to the Dockerfiles or service configurations, use:

    ```bash
    docker-compose up -d --build
    ```

- **Access a service shell**: To get inside a running container:

    ```bash
    docker exec -it <container-name> /bin/bash
    ```

    For example:

    ```bash
    docker exec -it sic_service /bin/bash
    ```

## Additional Notes

- **Database Data Persistence**: The database data is stored in the `db-data/postgres_sic/` and `db-data/postgres_acss/` directories. These are mapped as volumes to ensure data persistence across container restarts.
- **Modify Ports**: If you want to run the services on different ports, update the `ports` section in the `docker-compose.yml` file.

## Troubleshooting

- **Port Conflicts**: If any of the ports (e.g., `8000`, `8001`, `5434`, `5435`) are already in use, modify the `docker-compose.yml` file to use alternative ports.
- **Permission Issues**: Ensure Docker has the necessary permissions to create and write to the directories for the database volumes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
