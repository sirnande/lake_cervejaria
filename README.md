# lake-cervejaria
Processo de ETL caso de cervejaria

# Configuração do Ambiente

### Instalação do Docker no Windows
Para configurar o ambiente de desenvolvimento, primeiramente você precisará instalar o Docker Desktop no seu sistema operacional Windows. Siga os passos no link: https://docs.docker.com/desktop/setup/install/windows-install/


## Projeto de Engenharia de Dados

### Rodando o projeto pela primeira vez

Com o Docker instalado, vamos configurar o Apache Airflow usando Docker Compose.

1.  **Clonar o projeto na raiz do sistema na C:\ .** 

Caso tenha configurado a sua chave ssh no github:

```bash
git clone git@github.com:sirnande/lake_cervejaria.git
```

Caso queira usar a sua conta do github:

```bash
git clone https://github.com/sirnande/lake_cervejaria.git
```
 
2.  **Crie as Pastas Necessárias:** Caso não tenha as seguintes pasta criar dentro do projeto: `dags`, `logs`, `plugins` e `config`. Crie também um arquivo `.env` com o conteúdo `AIRFLOW_UID=50000`.
    * No Windows, você pode criar as pastas manualmente e o arquivo `.env` usando um editor de texto.
3.  **Inicialize o Banco de Dados do Airflow:** Antes de iniciar os serviços, inicialize o banco de dados do Airflow:
    ```bash
    docker compose up airflow-init
    ```
    Aguarde a conclusão.
4.  **Inicie os Serviços do Airflow:** Agora, inicie todos os serviços do Airflow em segundo plano:
    ```bash
    docker compose up -d
    ```
5.  **Acesse a UI do Airflow:** Após alguns minutos, o Airflow estará disponível. Acesse a interface de usuário em seu navegador: `http://localhost:8080`. As credenciais padrão são `airflow` para usuário e senha.

6.  **Configurar conexção com o posgres no airflow:** Após que tiver logado acessa no airflow:

    1. Admin -> Connections
    2. Butão add connection
        1. Connection ID: postgres_default
        2. Connection Type: Postgres
        3. Host: host.docker.internal
        4. Login: airflow
        5. Password: airflow
        6. Port: 5432
        7. Database: airflow

### Rodando o projeto dia a dia

start nos serviços do airflow
```bash
docker compose up -d
```

stop nos serviços do airflow no docker
```bash
docker compose down
```