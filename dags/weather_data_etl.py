from airflow.sdk import dag, task
from datetime import datetime
import requests
import pandas as pd
import json
# from tabulate import tabulate
from sqlalchemy import create_engine, MetaData, Table

BASE_URL = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

@dag(
    dag_id="weather_data_etl",
    description=f"Collect weather data from {BASE_URL} and load the transformed data into a PostgreSQL DB",
    start_date=datetime(2025, 8, 7),
    schedule="@hourly",
    catchup=False,
    tags=["weather", "api", "etl"]
)
def weather_data_etl():
    @task(task_id="extract_api_data")
    def get_api_data(param: str) -> dict:
        url = f"{BASE_URL}/alerts/active?area={param}"
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/geo+json"
        }

        response = requests.get(url, headers=headers)

        return {
            "status_code": response.status_code,
            "response": response.json()
        }


    @task(task_id="transform_data")
    def filter_response(response: dict, status_code: int) -> dict | pd.DataFrame:
        if not response or 'features' not in response:
            filtered_response = {
                "status_code": status_code,
                "message": f"Failed to fetch data: {response.get('message', 'Unable to fetch alerts or no alerts found for this state.')}"
            }

            return filtered_response
        
        if not response['features']:
            filtered_response = {
                "status_code": status_code,
                "message": "No active alerts found."
            }

            return filtered_response
        

        filtered_data = [data for data in response['features']]
        geometry = [data.get('geometry', {}) for data in filtered_data]
        coordinates = []
        for key in geometry:
            if key is None:
                coordinates.append({})
            else:
                coordinates.append(key.get('coordinates', [])) 
        df_coordinates = pd.DataFrame(coordinates, columns=['coordinates'])
        # print(df_coordinates.head())
        properties = [data.get('properties', {}) for data in filtered_data]
        df_properties = pd.DataFrame(properties)
        df_properties = df_properties[['messageType', 'event', 'headline', 'areaDesc']]
        # print(df_properties.head())

        df_merged = pd.concat([df_coordinates, df_properties], axis=1)
        df_merged['coordinates'] = df_merged['coordinates'].apply(json.dumps)
        # print(tabulate(df_merged.head(), headers='keys', tablefmt='github'))

        filtered_response = {
                "status_code": status_code,
                "message": "Data fetched successfully.",
                "data": df_merged.to_dict(orient='records')
            }

        df_table1 = pd.DataFrame(filtered_response)[['status_code', 'message']]
        df_table2 = df_merged[['messageType', 'event', 'headline', 'areaDesc']]
        df_table = pd.concat([df_table1, df_table2], axis=1)

        return df_table
    
    @task(task_id="load_data_to_db")
    def load_api_data(df_table: pd.DataFrame) -> None:
        # Create your engine
        engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/data_warehouse", future=True)
        metadata = MetaData(bind=engine)
        table = Table('load_api_data', metadata, autoload_with=engine)

        # Test connection
        try:
            with engine.begin() as connection:
                # Write the DataFrame to SQL
                connection.execute(table.insert(), df_table.to_dict(orient='records'))
                print("---------------------------- DATA LOADED SUCCESSFULLY ----------------------------")
        except Exception as e:
            print(f"Error connecting to the database: {e}")



    extract = get_api_data("GA")
    transform = filter_response(extract["response"], extract["status_code"])
    load = load_api_data(transform)


    extract >> transform >> load


weather_data_etl()