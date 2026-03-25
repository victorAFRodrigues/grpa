# Criando uma Nova Automação

O framework GRPA foi desenhado para facilitar a adição de novas automações sem a necessidade de modificar o núcleo do sistema (`core/`).

## Passo 1: Estrutura de Pastas

Todas as automações devem seguir esta estrutura dentro da pasta `automations/`:

```text
automations/
└── <nome_do_sistema>/
    ├── common/          # Componentes reutilizáveis (login, menu, etc)
    ├── data/            # Arquivos JSON de teste ou dados estáticos
    └── use_cases/       # A lógica principal de cada tarefa
        └── <nome_da_tarefa>.py
```

## Passo 2: Criando o Use Case

Crie um arquivo Python dentro de `use_cases/` (ex: `meu_processo.py`). Toda automação **deve** conter a função `run(page, log, data)`.

```python
from core.browser_automation import PlaywrightElement

def run(page, log, data):
    log.info("Iniciando meu processo...")
    
    # Navegação
    page.goto("https://meusite.com")
    
    # Interação usando PlaywrightElement
    campo = PlaywrightElement(page, "#input_id")
    campo.action("write", data['valor'])
    
    # Finalização
    if "Sucesso" in page.content():
        return True, "Processado com sucesso"
    
    return False, "Erro ao processar"
```

## Passo 3: Componentes Comuns (`common/`)

Se várias automações do mesmo sistema usam o mesmo login, crie um arquivo em `common/login.py`:

```python
# common/login.py
def run(page, log, data):
    page.goto("https://meusite.com/login")
    page.fill("#user", data['user'])
    page.fill("#pass", data['password'])
    page.click("#btn-login")

# No seu use_case:
from automations.meu_sistema.common import login

def run(page, log, data):
    login.run(page, log, data)
    # ... resto da lógica ...
```

## Passo 4: Testando Localmente

Para testar sua automação sem precisar da API, você pode adicionar um bloco `if __name__ == '__main__':` no final do seu arquivo de use case:

```python
if __name__ == '__main__':
    from core.browser_automation import BrowserAutomation
    from core.logger import Logger
    
    log = Logger("teste").get_logger()
    data = {"valor": "teste", "user": "admin", "password": "123"}
    
    with BrowserAutomation() as page:
        run(page, log, data)
```

## Boas Práticas
- **Não hardcode** URLs ou seletores; prefira usar o dicionário `data` ou constantes.
- **Use o Logger** em cada passo importante; isso facilita muito a depuração.
- **Prefira o PlaywrightElement** ao invés de usar `page.locator` diretamente, para garantir robustez com iframes.
