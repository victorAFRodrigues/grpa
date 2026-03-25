# Utilitários (Modules/Utils)

O GRPA oferece uma série de utilitários para facilitar o desenvolvimento de automações e garantir a consistência do framework.

## DotEnv (`modules/utils/general/env.py`)

Gerencia o acesso a variáveis de ambiente de forma segura e fácil.

```python
from modules.utils.general.env import DotEnv

env = DotEnv()
api_url = env.get("API_URL")
```

- **O que faz:** Lê automaticamente os arquivos `.env` e fornece um método `get` para buscar as chaves.

## Logger (`core/logger.py`)

Sistema de log personalizado com cores para facilitar o monitoramento via terminal.

```python
from core.logger import Logger

log = Logger("automations.meu_modulo").get_logger()

log.info("Processando...")
log.success("Tarefa concluída!")
log.error("Erro detectado!")
```

## ExecTime (`modules/utils/general/exectime.py`)

Um Context Manager que mede automaticamente o tempo que um bloco de código leva para ser executado.

```python
from modules.utils.general.exectime import ExecTime
from core.logger import Logger

log = Logger("timer").get_logger()

with ExecTime(log, "Processo de Busca"):
    # ... código que demora ...
    pass
```

- **Resultado no Log:** `[Processo de Busca] executado em 5.23 segundos.`

## Xml (`modules/utils/general/xml.py`)

Facilita a extração de dados de arquivos XML ou strings.

```python
from modules.utils.general.xml import Xml

xml_data = Xml("<root><name>GRPA</name></root>")
name = xml_data.find("name")  # Retorna "GRPA"
```

## Outros Utilitários

- `EnvUpdate`: Gerencia a persistência de variáveis no ambiente durante a execução.
- `ApiKey`: Gerencia chaves de acesso para APIs externas (Ex: Google Vision, etc).
- `Validate`: Funções auxiliares para validação de dados comuns (CNPJ, CPF, etc).
