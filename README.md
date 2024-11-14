# API de Cálculo de Faturas de Chamadas Telefônicas

Esta aplicação oferece uma API REST para calcular faturas mensais de chamadas telefônicas realizadas a partir de um número de telefone específico. A API calcula o custo total com base em chamadas feitas durante um período específico, considerando horários de pico e a duração de cada chamada.

## Funcionalidades

- **Gerar fatura de chamadas**: A API permite calcular o total de uma fatura com base no número de telefone e no período especificado.
- **Cálculo de custos**: O custo por minuto depende do horário da chamada (horário de pico ou fora de pico).
- **Visualização de registros de chamadas**: Os registros de chamadas realizadas durante o período de cálculo são retornados.


## Endpoints da API

A API possui os seguintes endpoints disponíveis:

### 1. `GET /phone_bill/{phone_number}`

Este endpoint retorna as faturas de chamadas para um número de telefone específico, baseado no período informado (se não informado, o período padrão será o mês atual).

#### Parâmetros de URL

- `phone_number` (obrigatório): O número de telefone para o qual as faturas serão recuperadas.

#### Parâmetros de Query (Opcional)

- `period` (opcional): O período no formato `YYYY-MM` para o qual as faturas devem ser retornadas. Se não fornecido, o período padrão será o mês atual.

#### Exemplo de Requisição

```bash
GET /phone-bill/48999650061?period=2024-10
```

#### Exemplo de Resposta

```json
{
  "id": "30671f73-02dd-4760-9112-7d61b3735fe1",
  "phone_number": "48999650061",
  "period": "2024-10-01",
  "total_cost": "0.00",
  "records": []
}
```

### 2. `POST /create`

Este endpoint cria uma fatura de chamadas para um número de telefone especificado.

#### Parâmetros de URL

- `phone_number` (obrigatório): O número de telefone para o qual a fatura será criada.

#### Corpo da Requisição

O corpo da requisição deve conter os detalhes das chamadas, incluindo o tipo de evento (`start` ou `end`), timestamp e outros detalhes relacionados.

#### Exemplo de Corpo de Requisição

```json
{
  "type": "start",
  "timestamp": "2024-11-14T00:28:39.981000Z",
  "call_id": -2147483648,
  "source": "48999650061",
  "destination": "string",
  "phone_bill": []
}
```

#### Exemplo de Resposta

```json
{
  "message": "Fatura criada com sucesso.",
  "phone_number": "48999650061",
  "call_id": -2147483648
}
```

### 3. `GET /call_records`

Este endpoint retorna todos os registros de chamadas.

#### Parâmetros de URL

- `phone_number` (obrigatório): O número de telefone para o qual os registros de chamadas serão recuperados.

#### Exemplo de Requisição

```bash
GET /call_records
```

#### Exemplo de Resposta

```json
[
  {
    "id": "c51fe92e-72a5-4bf9-a38a-1146db8af951",
    "type": "start",
    "timestamp": "2024-11-13T23:57:07.140000Z",
    "call_id": -2147483648,
    "source": "48999650061",
    "destination": "string",
    "phone_bill": []
  },
  {
    "id": "a5294478-0ea5-4a15-b302-c8b863a10410",
    "type": "end",
    "timestamp": "2024-11-14T00:29:31.073000Z",
    "call_id": -2147483648,
    "source": "48999650061",
    "destination": "string",
    "phone_bill": []
  }
]
```

### 4. `GET /call_records/{phone_number}`

Este endpoint retorna todos os registros de chamadas para um número de telefone especificado.

#### Parâmetros de URL

- `phone_number` (obrigatório): O número de telefone.

#### Corpo da Requisição

O corpo da requisição deve conter os detalhes da chamada, incluindo o tipo de evento (start ou end), timestamp, e outros detalhes relacionados.

#### Exemplo de Corpo de Requisição

#### Exemplo de Requisição

```bash
GET /call_records/48999650061
```

#### Exemplo de Resposta

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "type": "string",
  "timestamp": "2024-11-14T01:31:27.215Z",
  "call_id": -2147483648,
  "source": "string",
  "destination": "string",
  "phone_bill": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "phone_number": "string",
      "period": "2024-11-14",
      "total_cost": "string"
    }
  ]
}
```

Esses são os endpoints principais disponíveis na API para consulta, criação e verificação de faturas de chamadas telefônicas. Certifique-se de incluir as variáveis de ambiente adequadas, como as credenciais de banco de dados, para que a aplicação funcione corretamente.

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
