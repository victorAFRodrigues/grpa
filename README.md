# GRPA - Goevo Robot Process Automation

O **GRPA** é um ecossistema de automação robótica de processos (RPA) desenvolvido em Python, integrado ao software **GOEVO**. Ele utiliza **Playwright** para automação de navegador e segue uma arquitetura modular focada em escalabilidade, reutilização de código e facilidade de manutenção.

Este repositório serve como um **boilerplate completo** para o desenvolvimento de novas automações.

---

## 🚀 Como Começar

### Pré-requisitos
- **Python 3.14+**
- **uv** (Recomendado para gerenciamento de pacotes e ambientes virtuais)
- **Playwright Browsers**

### Instalação e Setup
1. Clone o repositório.
2. Crie e ative o ambiente virtual:
   ```bash
   uv venv
   .venv\Scripts\activate  # No Windows
   ```
3. Instale as dependências:
   ```bash
   uv sync
   ```
4. Instale os navegadores do Playwright:
   ```bash
   playwright install chromium
   ```
5. Configure o arquivo `.env` (use o `.envexample` como base).

---

## Rodando via Docker:


## Estrutura do Projeto

- `core/`: Núcleo do sistema (API, Worker, Logger, Browser Automation).
- `automations/`: Onde residem as automações específicas (separadas por sistema).
- `modules/`: Utilitários gerais (XML, DotEnv, Validações, Modelos).
- `logs/`: Logs de execução gerados automaticamente.
- `screenshots/`: Capturas de tela automáticas em caso de erro.

---

## Desenvolvendo uma Nova Automação

Siga este fluxo para garantir que sua automação seja compatível com o `worker` dinâmico do GRPA.

### 1. Estrutura de Pastas
Crie uma pasta dentro de `automations/` com o nome do sistema alvo (ex: `meu_sistema`):

```filesystem
automations/
   meu_sistema/
        common/          # Módulos reutilizáveis (login, preenchimento de capas, etc)
            __init__.py
            login.py
        data/            # Arquivos JSON para simular dados da API localmente
            meu_caso.json
        use_cases/       # Entry points da automação
            __init__.py
            meu_caso.py
```

### 2. Criando um Use Case (Entry Point)
Cada automação deve ter um arquivo em `use_cases/` que exporta obrigatoriamente uma função `run(page, log, data)`.

**Template: `automations/meu_sistema/use_cases/meu_caso.py`**
```python
from json import load
from core.browser_automation import BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime

def run(page, log, data):
    """
    Função principal executada pelo Worker.
    :param page: Instância do Playwright Page.
    :param log: Logger configurado para o processo.
    :param data: Dicionário com os parâmetros recebidos (ex: dados da NF).
    :return: (bool, str) -> (Sucesso, Mensagem de retorno para o GOEVO).
    """
    try:
        log.info(f"Iniciando processo: {data.get('id_tarefa', 'N/A')}")
        
        # Sua lógica de automação aqui...
        page.goto('https://www.exemplo.com')
        
        return True, "Processo concluído com sucesso!"

    except Exception as ex:
        log.error(f"Falha na execução: {ex}")
        raise ex # O worker capturará a exceção e salvará um screenshot

if __name__ == '__main__':
    # Bloco para teste local individual
    _log = Logger("automations.meu_sistema.use_cases.meu_caso").get_logger()
    path = f'../data/meu_caso.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'meu_caso'):
        with BrowserAutomation() as _page:
            try:
                run(_page, _log, _data)
            except Exception as ex:
                _log.error(ex)
```

### 3. Criando Módulos Comuns (Common)
Para partes complexas ou repetitivas, utilize a pasta `common/`.

**Template: `automations/meu_sistema/common/login.py`**
```python
def run(page, log, data):
    log.info("Realizando login...")
    page.fill('#usuario', data['user'])
    page.fill('#senha', data['password'])
    page.click('#btn-entrar')
```

---

## Testes Locais

Para testar sua automação sem depender da fila da API:
1. Crie um arquivo JSON em `automations/meu_sistema/data/meu_caso.json` com os dados de teste.
2. Execute o arquivo do use case diretamente:
   ```bash
   python -m automations.meu_sistema.use_cases.meu_caso
   ```

---

## 💡 Recursos do Boilerplate

### Browser Automation (`core.browser_automation`)
Use a classe `PlaywrightElement` para interações robustas que lidam automaticamente com **iframes**:
```python
from core.browser_automation import PlaywrightElement

# Clica em um elemento (mesmo que esteja dentro de um iframe aninhado)
PlaywrightElement(page, '#botao-salvar').action('click')

# Preenche um campo com timeout customizado
PlaywrightElement(page, '#campo-texto', timeout=5000).action('write', 'Valor Teste')
```

### Logger (`core.logger`)
O log é persistido em arquivo e exibido no console com cores para facilitar o debug:
```python
log.info("Iniciando etapa X")
log.success("Etapa concluída")
log.error("Erro na validação do campo Y")
```

### Captura Automática de Evidências
Se uma automação falhar (lançar uma exceção):
1. O `BrowserAutomation` tira um **screenshot** da tela exata do erro.
2. O `Logger` salva o rastreio completo.
3. O `main.py` converte essas evidências para Base64 e envia automaticamente para o **GOEVO**.

---

## Padrões de Desenvolvimento
- **Nomenclatura:** Use `snake_case` para arquivos, pastas e funções.
- **Tratamento de Erros:** Deixe as exceções críticas subirem para que o Worker registre a falha.
- **Modularização:** Evite arquivos de use case gigantes. Mova lógicas de preenchimento de formulários extensos para a pasta `common/`.
