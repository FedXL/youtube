# Multi DO Production 
CRUD emulator

## Start project
After deploying the Docker container, migrations are necessary. These migrations are performed using Alembic. Configuration files are already set up for the containers. In the root folder /src, you need to execute the following commands:

### Migrate 
```code
alembic revision
alembic upgrade head
alembic revision --autogenerate
alembic upgrade head
```

### Entry Point
The basic application is configured on port 8000 and will be available at the address 127.0.0.1:8000. Immediately after running docker-compose.
The entry point is /src/main.py, and you should run the application with the command python main.py.
## Deployment Without Docker

[Config Database File](https://github.com/FedXL/youtube/blob/5f7bd587bbbcdce5f3730802d8192a640545726f/src/base/config.py
)

To deploy without Docker, you will need to configure the configuration file for database connectivity and adjust the port and host settings in the main.py file.


