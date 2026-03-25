# Manutenção e Artefatos

O GRPA possui sistemas internos para garantir que as automações estejam sempre atualizadas e que os erros sejam fáceis de diagnosticar.

## Updater (`core/updater.py`)

O `Updater` gerencia a atualização dinâmica do código de automação sem a necessidade de reiniciar o container ou o processo principal.

### Funcionalidades:
- **`bootstrap_automations()`**: Garante que a pasta `automations/` esteja populada ao iniciar o robô (útil em ambientes Docker com volumes).
- **`automations(url)`**: 
  1. Baixa um arquivo `.zip` da URL fornecida.
  2. Extrai o conteúdo em um diretório temporário.
  3. Substitui a pasta `automations/` local pela nova versão.
  4. Atualiza a versão no arquivo `.env` via `GRPA_AUTOMATION_VERSION`.

> **Nota:** Este processo é chamado automaticamente pela `Api.search_update()` quando uma nova versão é detectada no backend.

---

## ArtifactManager (`core/artifact_manager.py`)

Responsável por localizar e converter artefatos de execução (logs e screenshots) para o formato esperado pela API (Base64).

### Métodos Principais:

#### `latest_log(module_name)`
Busca o arquivo de log mais recente para um determinado módulo de automação.
- **Retorno:** Dicionário contendo o nome do arquivo e o conteúdo em Base64.

#### `latest_screenshot()`
Busca a última captura de tela gerada pelo `BrowserAutomation` (geralmente após um erro).
- **Retorno:** Dicionário contendo o nome do arquivo e o conteúdo em Base64.

### Exemplo de Uso Interno (Main):

```python
from core.artifact_manager import ArtifactManager

am = ArtifactManager()
log_data = am.latest_log("validar_fornecedor")
screenshot_data = am.latest_screenshot()

# Enviando para a API
api.finish_task(..., logs_b64=log_data["b64"], screenshot_b64=screenshot_data["b64"])
```

## Diretórios de Trabalho
- `logs/`: Onde os arquivos `.log` são armazenados pelo `Logger`.
- `screenshots/`: Onde os arquivos `.png` são salvos pelo `BrowserAutomation`.
