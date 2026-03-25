# Worker e Fluxo de Execução

O **Worker** é o coração da execução dinâmica do GRPA. Ele é responsável por carregar o módulo de automação correto com base nos parâmetros recebidos.

## Funcionamento

O Worker recebe o nome do sistema e do caso de uso, e tenta importar dinamicamente o arquivo correspondente em `automations/`.

```python
from core.worker import worker

result, content = worker(
    guid="12345",
    system="system",
    use_case="validar_fornecedor",
    data={"cnpj": "12.345.678/0001-90"}
)
```

## O que o Worker faz:
1.  **Importação Dinâmica:** Ele mapeia o `system` e `use_case` para o caminho do arquivo (Ex: `automations.system.use_cases.validar_fornecedor`).
2.  **Gerenciamento de Cache:** Limpa o módulo do `sys.modules` se ele já tiver sido carregado, garantindo que a versão mais recente seja utilizada.
3.  **Execução Orquestrada:** 
    - Inicia o logger para o módulo específico.
    - Mede o tempo de execução usando `ExecTime`.
    - Abre o navegador usando `BrowserAutomation`.
    - Chama a função `run(page, log, data)` dentro do módulo de automação.
4.  **Captura de Resultado:** Retorna se a execução foi bem-sucedida e o conteúdo/mensagem gerado pela automação.

## Estrutura Esperada em um Módulo de Automação

Para que o Worker consiga executar uma automação, ela **deve** ter uma função `run`:

```python
def run(page, log, data):
    # page: objeto Page do Playwright
    # log: logger configurado
    # data: dicionário com os parâmetros da tarefa
    
    # ... Lógica da automação ...
    
    return True, "Mensagem de sucesso"
```

## Por que usar o Worker?
- **Isolamento:** Cada automação roda em seu próprio contexto.
- **Flexibilidade:** Permite adicionar novas automações sem alterar o código principal (`main.py`).
- **Observabilidade:** Garante logs e medição de tempo padronizados para todas as tarefas.
