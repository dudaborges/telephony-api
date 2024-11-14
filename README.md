# API de Cálculo de Faturas de Chamadas Telefônicas

Esta aplicação oferece uma API REST para calcular faturas mensais de chamadas telefônicas realizadas a partir de um número de telefone específico. A API calcula o custo total com base em chamadas feitas durante um período específico, considerando horários de pico e a duração de cada chamada.

## Funcionalidades

- **Gerar fatura de chamadas**: A API permite calcular o total de uma fatura com base no número de telefone e no período especificado.
- **Cálculo de custos**: O custo por minuto depende do horário da chamada (horário de pico ou fora de pico).
- **Visualização de registros de chamadas**: Os registros de chamadas realizadas durante o período de cálculo são retornados.

## Endpoints

### `GET /phone-bill/{phone_number}`

Recupera a fatura de chamadas para um número de telefone específico, com base no período fornecido.

**Parâmetros**
- `phone_number` (string): O número de telefone para o qual a fatura será gerada (formato: `DDD+NUMERO`).

**Query Parameters**
- `period` (opcional): O mês para o qual a fatura será gerada, no formato `MM/YYYY`. Caso não seja fornecido, o período será calculado automaticamente para os últimos 30 dias.

**Resposta**
```json
{
  "id": "30671f73-02dd-4760-9112-7d61b3735fe1",
  "phone_number": "48999650061",
  "period": "2024-10-01",
  "total_cost": "0.00",
  "records": [
    {
      "id": "c51fe92e-72a5-4bf9-a38a-1146db8af951",
      "type": "start",
      "timestamp": "2024-10-01T12:00:00.000000Z",
      "call_id": 1,
      "source": "48999650061",
      "destination": "48991234567",
      "duration": 120
    },
    {
      "id": "d8f234a3-d455-4ced-93c2-27b09b79d871",
      "type": "end",
      "timestamp": "2024-10-01T12:02:00.000000Z",
      "call_id": 1,
      "source": "48999650061",
      "destination": "48991234567",
      "duration": 120
    }
  ]
}
```

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção da API REST.
- **Tortoise**: ORM assíncrono para interação com bancos de dados.
- **PostgreSQL**: Banco de dados para armazenar os registros de chamadas e faturas.
- **Pydantic**: Para validação de dados e resposta das APIs.
- **Datetime**: Manipulação de datas e horas para o cálculo de faturas.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/dudaborges/telephony-api
   cd telephony-api
   ```
### 2. Configuração do Docker Compose

Este projeto já vem configurado com Docker e Docker Compose. Você pode rodar a aplicação facilmente com os containers do Docker.

Para rodar o projeto com Docker Compose, basta executar o seguinte comando:

```bash
docker-compose up --build
```

Isso irá criar os containers necessários (para o aplicativo FastAPI e o banco de dados PostgreSQL) e iniciar a aplicação na porta configurada.

## Rodando Localmente

Para rodar a aplicação localmente, siga os seguintes passos:

### 1. Instalar as Dependências com Poetry

Primeiro, instale o Poetry, se ainda não o fez. Você pode seguir as instruções de instalação no [site oficial do Poetry](https://python-poetry.org/docs/#installation).

Depois, instale as dependências do projeto com o seguinte comando:

```bash
poetry install
```

Isso irá instalar todas as dependências do projeto, incluindo as de desenvolvimento.

### 2. Criar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto para definir as variáveis de ambiente necessárias para a execução local. Por exemplo:

```env
DATABASE_URL=postgres://usuario:senha@localhost:5432/telephony_api_db
```

### 3. Rodar o Projeto Localmente

Com as dependências instaladas e o arquivo `.env` configurado, você pode rodar a aplicação localmente com o comando:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 5000
```

Isso iniciará o servidor FastAPI na porta 5000.

### 4. Comandos do Taskipy

Este projeto utiliza o [Taskipy](https://github.com/python-taskipy/taskipy) para facilitar algumas tarefas de desenvolvimento. Aqui estão os principais comandos disponíveis:

- **`task lint`**: Verifica a formatação do código com o Blue e o Isort.
  
  Comando:
  ```bash
  poetry run task lint
  ```

- **`task pre_test`**: Executa o comando de linting antes dos testes.

  Comando:
  ```bash
  poetry run task pre_test
  ```

- **`task test`**: Executa os testes com o Pytest, gerando cobertura de código.

  Comando:
  ```bash
  poetry run task test
  ```

- **`task post_test`**: Gera o relatório de cobertura em HTML após os testes.

  Comando:
  ```bash
  poetry run task post_test
  ```

Esses comandos ajudam a garantir que o código esteja bem formatado e que os testes sejam executados corretamente.
