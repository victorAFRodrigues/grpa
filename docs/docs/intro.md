# Introdução ao GRPA (General RPA)

O **GRPA** (General Robotic Process Automation) é um framework modular de automação robótica de processos baseado em **Playwright** e **Python**. 

Ele foi desenvolvido para ser altamente extensível, permitindo que novas automações sejam adicionadas como módulos dinâmicos que podem ser orquestrados por um backend via API.

## Principais Funcionalidades

- **Automação de Navegador Robusta:** Utiliza Playwright para interações rápidas e confiáveis, com suporte nativo a iframes aninhados.
- **Carregamento Dinâmico:** O Worker carrega automaticamente os casos de uso de automação baseados nas instruções recebidas da API.
- **Gerenciamento de Erros:** Captura automática de screenshots e logs em caso de falha durante a execução.
- **Comunicação Padronizada:** Interface de API integrada para buscar tarefas, reportar progresso e finalizar execuções.
- **Auto-Atualização:** Sistema integrado para verificar e atualizar os pacotes de automação dinamicamente.

## Estrutura do Projeto

Abaixo está uma visão simplificada da estrutura de pastas:

- `core/`: Classes base do framework (API, Browser, Worker, Logger).
- `automations/`: Contém os sistemas e casos de uso específicos de cada automação.
- `modules/utils/`: Utilitários gerais para ambiente, tempo de execução e manipulação de dados.
- `docs/`: Documentação oficial (este site).

## Fluxo de Execução

1. O processo `main.py` inicia e verifica por atualizações de automação.
2. Ele entra em um loop infinito, solicitando tarefas via `Api.get_task`.
3. Ao receber uma tarefa, o `Worker` identifica o sistema e o caso de uso.
4. O Worker inicia o `BrowserAutomation`, que abre o navegador.
5. A lógica da automação é executada.
6. O resultado (sucesso ou falha), junto com logs e screenshots (em caso de erro), é enviado de volta para a API.

---

Siga para a seção de **Conceitos Core** para entender como cada componente funciona detalhadamente.
