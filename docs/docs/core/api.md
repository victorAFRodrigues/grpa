# Classe Api

A classe `Api` é responsável pela comunicação centralizada entre o robô e o backend do GRPA. Ela padroniza todas as requisições para garantir consistência e segurança.

## Inicialização

A classe é inicializada carregando as configurações do arquivo `.env`.

```python
from core.api import Api

api = Api()
```

## Métodos Disponíveis

### `get_task(endpoint)`
Solicita uma nova tarefa pendente para o executor configurado no ambiente.

- **Parâmetros:** `endpoint` (str) - O caminho da API para buscar tarefas (Ex: `/IniciarTarefa`).
- **Retorno:** Objeto de resposta da biblioteca `requests`.

### `reset_task(endpoint, guid_code)`
Reseta uma tarefa em andamento, permitindo que ela seja processada novamente.

- **Parâmetros:** 
  - `endpoint` (str): Endpoint da API.
  - `guid_code` (str): Identificador único da tarefa (RPA_GUID).

### `finish_task(endpoint, rpa_msg, errorcode, guid_code, logs_b64, screenshot_b64)`
Finaliza uma tarefa informando o resultado, mensagens e anexando logs ou screenshots em caso de erro.

- **Parâmetros:**
  - `endpoint` (str): Endpoint da API (Ex: `/FinalizarTarefa`).
  - `rpa_msg` (str): Mensagem final do robô.
  - `errorcode` (str): Código do erro ("00" para sucesso, "01" para erro).
  - `guid_code` (str): RPA_GUID da tarefa.
  - `logs_b64` (str): Logs da execução codificados em base64.
  - `screenshot_b64` (str): Screenshot codificado em base64.

### `search_update()`
Verifica se existe uma nova versão das automações disponível no servidor e realiza a atualização automática se necessário.

## Exemplo de Uso Completo

```python
from core.api import Api
import json

api = Api()

# 1. Buscar Tarefa
response = api.get_task("/IniciarTarefa").json()
if response["content"]:
    task = json.loads(response["content"])[0]
    guid = task["RPA_GUID"]
    
    # ... Execução da Automação ...
    
    # 2. Finalizar Tarefa
    api.finish_task(
        endpoint="/FinalizarTarefa",
        rpa_msg="Tarefa concluída com sucesso",
        errorcode="00",
        guid_code=guid,
        logs_b64="",
        screenshot_b64=""
    )
```

## Dependências de Ambiente
Certifique-se de que as seguintes variáveis estejam no seu `.env`:
- `API_URL`: URL base do backend.
- `GOEVO_APP_TPTOKEN`: Token de autenticação.
- `RPA_EXECUTOR`: Nome identificador deste executor robótico.
