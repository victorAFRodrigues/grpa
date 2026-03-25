# Automação de Navegador

O GRPA utiliza o **Playwright** como motor de automação. Para facilitar o uso, o framework fornece as classes `BrowserAutomation` e `PlaywrightElement`.

## BrowserAutomation

A classe `BrowserAutomation` funciona como um **Context Manager**, garantindo que o navegador seja aberto e fechado corretamente, e que screenshots sejam tirados em caso de exceção.

### Como usar

```python
from core.browser_automation import BrowserAutomation

with BrowserAutomation() as page:
    page.goto("https://www.google.com")
    # A lógica da automação continua aqui...
```

### O que acontece nos bastidores:
- Inicializa o Playwright e abre o Chromium.
- Carrega as configurações (headless, sandbox, viewport) do ambiente.
- Se ocorrer um erro dentro do bloco `with`, um **screenshot** é salvo automaticamente na pasta `screenshots/`.

---

## PlaywrightElement

Uma classe utilitária para interagir com elementos da página de forma robusta, lidando inclusive com **iframes aninhados**.

### Métodos Principais

#### `find()`
Busca um elemento na página principal ou dentro de qualquer iframe presente. Aguarda o elemento estar disponível antes de retornar.

#### `action(action, text=None)`
Executa uma ação no elemento encontrado.
- **Ações suportadas:** `"click"`, `"write"`, `"press"`, `"move_to"`.
- **Exemplo:** `el.action("write", "Texto para digitar")`

#### `screenshot(page)` (estático)
Captura um screenshot da página inteira e o salva com um timestamp.

### Exemplo de Uso com Elementos

```python
from core.browser_automation import BrowserAutomation, PlaywrightElement

with BrowserAutomation() as page:
    # 1. Localizar um elemento (mesmo que esteja dentro de um iframe)
    search_input = PlaywrightElement(page, "input[name='q']")
    
    # 2. Executar uma ação
    search_input.action("write", "GRPA Framework")
    search_input.action("press", "Enter")
```

## Configuração do Browser
O comportamento do navegador pode ser ajustado via arquivo `.env`:
- `ENV`: Se for `'docker'`, o navegador rodará em modo **headless**.
- `viewport`: Configurado por padrão como `1280x728`.
