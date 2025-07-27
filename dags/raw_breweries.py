from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import date, datetime
from airflow.models import Variable
import pendulum
import pandas as pd
import json
import os

"""
    Função Python para carregar dados de cervejarias de um arquivo JSON
    e salvá-los em uma tabela PostgreSQL.
"""
def raw_breweries(**kwargs):
    data_atual = date.today() # Em um projeto real usariamos a data de execução da dag
    input_dir = "/tmp/airflow_data" # em projeto real essa var ficaria no airflow
    file_name = f"breweries_data_{str(data_atual).replace('-', '_')}.json"
    input_file = os.path.join(input_dir, file_name)
    table_name = "raw_breweries" 

    if not os.path.exists(input_file):
        print(
            f"Arquivo JSON não encontrado: {input_file}. Verifique se a DAG de extração foi executada com sucesso."
        )
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {input_file}")

    try:
        df = pd.read_json(input_file)
        df['create_dt'] = datetime.now()
        df['source_file'] = input_file

        # Conecta ao PostgreSQL
        pg_hook = PostgresHook(
            postgres_conn_id="postgres_default"
        ) 
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Cria a tabela se ela não existir.
        # Verifica se é a melhor solução se for rodar uma vz ao dia e os dados não pesado pode deixa caso contrário deverá
        # Ser criada a parte
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            brewery_type VARCHAR(50),
            address_1 VARCHAR(255),
            address_2 VARCHAR(255),
            address_3 VARCHAR(255),
            city VARCHAR(255),
            state_province VARCHAR(255),
            postal_code VARCHAR(20),
            country VARCHAR(100),
            longitude VARCHAR(50),
            latitude VARCHAR(50),
            phone VARCHAR(50),
            website_url TEXT,
            state VARCHAR(255),
            street VARCHAR(255),
            create_dt TIMESTAMP,
            source_file VARCHAR(255)
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print(f"Tabela '{table_name}' verificada/criada com sucesso.")

        cols = df.columns.tolist()
      
        columns_str = ", ".join(cols)
        values_placeholder = ", ".join(["%s"] * len(cols))
        insert_sql = (
            f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_placeholder});"
        )

        # Converte o DataFrame para uma lista de tuplas para inserção
        data_to_insert = [tuple(row) for row in df[cols].values]

        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()
        print(
            f"Dados das cervejarias carregados com sucesso na tabela '{table_name}'. Total de {len(df)} registros."
        )

    except FileNotFoundError as e:
        print(e)
        raise
    except Exception as e:
        print(f"Erro ao carregar dados para o banco de dados: {e}")
        raise
    finally:
        if "conn" in locals() and conn:
            cursor.close() # fechando o curso para não consumir recursos
            conn.close() # Fechando a conexão com o banco, liberando mais recursos



with DAG(
    dag_id="raw_breweries",
    schedule="0 9 * * *", 
    start_date=pendulum.datetime(
        2025, 7, 26, 00, 15, tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["breweries", "raw", "etl"],
) as dag_load:
    start_load = EmptyOperator(task_id="start_load")
    end_load = EmptyOperator(task_id="end_load")

    load_task = PythonOperator(
        task_id="raw_breweries",
        python_callable=raw_breweries,
    )

start_load >> load_task >> end_load