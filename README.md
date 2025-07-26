# lake-cervejaria
Processo de ETL caso de cervejaria

# Configuração do Ambiente

### Instalação do Docker no Windows
Para configurar o ambiente de desenvolvimento, primeiramente você precisará instalar o Docker Desktop no seu sistema operacional Windows. Siga os passos no link: https://docs.docker.com/desktop/setup/install/windows-install/

### Instalação do Airflow Usando Docker
Com o Docker instalado, podemos prosseguir para a instalação do Apache Airflow usando Docker Compose, que é a maneira recomendada para configurar o Airflow para desenvolvimento e produção.

1. **Crie um Diretório para o Projeto:** Crie uma pasta vazia onde você irá armazenar os arquivos do projeto Airflow na raiz. Por exemplo, `C:\lake_cervejaria`.

### Instalação do Airflow Usando Docker

Com o Docker instalado, vamos configurar o Apache Airflow usando Docker Compose.

1.  **Crie um Diretório para o Projeto:** Crie uma pasta vazia para seu projeto Airflow, por exemplo, `C:\airflow_project`.
2.  **Baixe o `docker-compose.yaml` do Airflow:** No terminal, navegue até a pasta que você criou e baixe o arquivo:
    ```bash
    curl -LfO '[https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml)'
    ```
    *Para a versão mais atualizada, verifique o site oficial do Airflow.*
3.  **Crie as Pastas Necessárias:** Crie as subpastas `dags`, `logs`, `plugins` e `config` dentro do seu diretório do projeto. Crie também um arquivo `.env` com o conteúdo `AIRFLOW_UID=50000`.
    * No Windows, você pode criar as pastas manualmente e o arquivo `.env` usando um editor de texto.
4.  **Inicialize o Banco de Dados do Airflow:** Antes de iniciar os serviços, inicialize o banco de dados do Airflow:
    ```bash
    docker compose up airflow-init
    ```
    Aguarde a conclusão.
5.  **Inicie os Serviços do Airflow:** Agora, inicie todos os serviços do Airflow em segundo plano:
    ```bash
    docker compose up -d
    ```
6.  **Acesse a UI do Airflow:** Após alguns minutos, o Airflow estará disponível. Acesse a interface de usuário em seu navegador: `http://localhost:8080`. As credenciais padrão são `airflow` para usuário e senha.

---

## Projeto de Engenharia de Dados
comando
inciando airflow
```bash
    docker compose up -d
```