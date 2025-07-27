from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import date
import requests
import pendulum
import pandas as pd

def trusted_breweries(**kwargs):
    # data_atual = date.today()
    table_name = "raw_breweries" 
    try:
        pg_hook = PostgresHook(
            postgres_conn_id="postgres_default" #Configurar conexão no aifow
        )
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        sql_raw = F"SELECT * FROM {table_name} WHERE DATE(create_DT) = CURRENT_DATE;"

        df = pg_hook.get_pandas_df(sql_raw)

        print(f"Successfully fetched {len(df)} rows into a DataFrame.")
        print(df.head())

        print(df.isnull().sum())
    
    except Exception as e:
        print(f"Erro ao carregar dados para o banco de dados: {e}")
        raise
    finally:
        if "conn" in locals() and conn:
            cursor.close() # fechando o curso para não consumir recursos
            conn.close() # Fechando a conexão com o banco, liberando mais recursos


with DAG(
    dag_id="trusted_breweries",
    schedule="30 9 * * *",
    start_date=pendulum.datetime(
        2025, 7, 26, 00, 15, tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["breweries", "trusted"],
    description='DAG trusted aplicação de deduplicação, limpeza e tratamento de dados.'
) as dag_load:
    start_load = EmptyOperator(task_id="start_load")
    end_load = EmptyOperator(task_id="end_load")

    load_trusted = PythonOperator(
        task_id="truted_breweries",
        python_callable=trusted_breweries
    )

start_load >> load_trusted >> end_load