from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import date
import requests
import pendulum
import pandas as pd

import os


def extract_breweries_data(**kwargs):
    data_atual = date.today() # Em um projeto real usariamos a data de execução da dag
    api_url = "https://api.openbrewerydb.org/v1/breweries" # Em um projeto real esta informação estaria no airflow
    output_dir = "/tmp/airflow_data"  # Em um projeto real esta informação estaria no airflow
    file_name = f"breweries_data_{str(data_atual).replace('-', '_')}.json"
    output_file = os.path.join(output_dir, file_name)

    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        breweries_data = response.json()

        if breweries_data:
            df = pd.DataFrame(breweries_data)
            df.to_json(output_file, index=False)
            print(f"Dados das cervejarias extraídos e salvos em: {output_file}")
        else:
            print("Nenhum dado de cervejaria retornado pela API.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ou extrair dados da API: {e}")
        raise
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        raise


with DAG(
    dag_id="extract_breweries_api_data",
    schedule="0 8 * * *",
    start_date=pendulum.datetime(2025, 7, 20, 00, 10, tz="America/Sao_Paulo"),
    catchup=True,
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    extract_task = PythonOperator(
        task_id="extract_breweries_from_api",
        python_callable=extract_breweries_data,
    )

start >> extract_task >> end
