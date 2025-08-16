# Weather Data ETL with Apache Airflow

This project provides an ETL pipeline using [Apache Airflow](https://airflow.apache.org/) to collect weather alerts from the [weather.gov API](https://api.weather.gov), transform the data, and load it into a PostgreSQL database. The environment is orchestrated using Docker Compose.

## Features

- **ETL DAGs**: Automated workflows for extracting, transforming, and loading weather alert data.
- **PostgreSQL Integration**: Stores transformed weather data for further analysis.
- **Docker Compose Setup**: Easily run Airflow, PostgreSQL, Redis, and pgAdmin locally.
- **Sample Data Model**: See [`api_response_model.json`](api_response_model.json) for example API responses.

## Project Structure

```
.
├── dags/
│   ├── hello_world_dag.py
│   ├── my_dag.py
│   └── weather_data_etl.py
├── config/
│   └── airflow.cfg
├── logs/
├── plugins/
├── api_response_model.json
├── docker-compose.yaml
├── .env
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Setup

1. **Clone the repository**  
   ```sh
   git clone <https://github.com/msremigio/apache-airflow-dags.git>
   cd docker-run-airflow
   ```

2. **Configure environment variables**  
   Optionally, edit `.env` for custom settings.

3. **Configuration & Credentials**

> 3.1 **Database Connection**:  
  The PostgreSQL database credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) and port mapping are configured in [`docker-compose.yaml`](docker-compose.yaml).  
  Default values:
  - User: `airflow`
  - Password: `airflow`
  - Database: `airflow`
  - Port: `5000` (host) → `5432` (container)

> 3.2 **Airflow Admin Login**:  
  The admin username and password for the Airflow web interface are set in your Airflow configuration file ([`config/airflow.cfg`](config/airflow.cfg)).  
  Default values:
  - Username: `airflow`
  - Password: `airflow`

> 3.3 **pgAdmin Login**:  
  Credentials for pgAdmin are set in [`docker-compose.yaml`](docker-compose.yaml):
  - Email: `admin@admin.com`
  - Password: `admin`

> **Tip:**  
> Always review and update these credentials for production deployments to ensure

4. **Start the services**  
   ```sh
   docker-compose up --build
   ```

5. **Access Airflow UI**  
   - Airflow API Server: [http://localhost:8080](http://localhost:8080)
     (Default credentials: admin@admin.com / admin)
   - pgAdmin: [http://localhost:5050](http://localhost:5050)  
     (Default credentials: admin@admin.com / admin)

6. **Check DAGs**  
   - The main ETL DAG is [`weather_data_etl`](dags/weather_data_etl.py).
   - Example: Extracts weather alerts for Georgia (`GA`), transforms, and loads to PostgreSQL.

## Usage

- To run the ETL pipeline, enable the `weather_data_etl` DAG in the Airflow UI.
- The DAG will fetch weather alerts, process them with Pandas, and insert them into the `load_api_data` table in the PostgreSQL database.

## Customization

- To change the state/area for weather alerts, modify the parameter in [`weather_data_etl.py`](dags/weather_data_etl.py).
- Database connection settings can be adjusted in [`docker-compose.yaml`](docker-compose.yaml).

## Troubleshooting

- Ensure Docker and Docker Compose are installed and running.
- If you encounter database connection issues, check the `ports` and credentials in [`docker-compose.yaml`](docker-compose.yaml).
- Airflow logs are available in the `logs/` directory once the docker containers are up and running.

## License

See [LICENSE](LICENSE) for details.

## Author

Matheus Remigio  
Contact: matheus.remido@gmail.com
