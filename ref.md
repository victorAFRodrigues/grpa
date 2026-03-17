# Referência de Funcionalidades do Projeto - GRPA Lelac Oficial

Este documento descreve as funcionalidades e a arquitetura do projeto de automação RPA para o sistema Dealernet.

## 1. Core (Núcleo do Sistema)

Localizado no diretório `core/`, é responsável pela infraestrutura base do robô.

- **API de Integração (`api.py`)**: 
    - Busca de novas tarefas no sistema central (GoEvo).
    - Finalização de tarefas com envio de logs e screenshots em Base64.
    - Reset de tarefas e busca de variáveis globais.
    - Verificação e download automático de atualizações de pacotes (`search_update`).
- **Automação de Navegador (`browser_automation.py`)**:
    - Abstração do Playwright para interações robustas.
    - Suporte a busca recursiva em iframes aninhados.
    - Captura automática de screenshots em caso de erro.
    - Configuração flexível de browser (Headless/Docker).
- **Orquestrador de Tarefas (`worker.py`)**:
    - Carregamento dinâmico de módulos de automação (Use Cases).
    - Gerenciamento do ciclo de vida da execução e captura de exceções.
- **Gerenciador de Atualizações (`updater.py`)**:
    - Sincronização de arquivos do projeto com o servidor.
- **Logs (`logger.py`)**:
    - Sistema de log padronizado para rastreabilidade das operações.

## 2. Automações Dealernet

Localizadas em `automations/dealernet/`, estas são as funcionalidades de negócio.

### Casos de Uso (`use_cases/`)
- **Cadastro de NF de Produto (`cadastrar_nf_produto.py`)**: Fluxo completo de entrada de mercadorias via XML.
- **Cadastro de NF de Serviço (`cadastrar_nf_servico.py`)**: Fluxo de registro de notas de serviços tomados.
- **Validação de Fornecedor (`validar_fornecedor.py`)**: Verificação cadastral de fornecedores no sistema.

### Componentes Comuns (`common/`)
- **Login**: Autenticação automática no sistema Dealernet.
- **Importação e Seleção de XML**: Processamento de arquivos XML de NF-e.
- **Categorização de Produtos**: Vínculo de produtos da nota com o cadastro interno.
- **Preenchimento de Capa**: Dados gerais da nota fiscal (Número, Data, Fornecedor).
- **Gestão Financeira**:
    - **Parcelamento (`fill_installments.py`)**: Preenchimento de faturas e duplicatas.
    - **Rateio de Custos (`fill_cost_allocation.py`)**: Alocação de custos por centro de custo ou filial.
- **Troca de Filial (`switch_filial.py`)**: Navegação entre diferentes unidades da empresa.

## 3. Módulos e Utilitários (`modules/`)

- **Manipulação de XML (`xml.py`)**: Utilitário para salvar e ler conteúdos de XML vindos da API.
- **Gestão de Configurações (`dotenv.py` / `envupdate.py`)**: Gerenciamento de variáveis de ambiente e segredos.
- **Modelos de Dados (`models.py`)**: Definição de estruturas (Pydantic) para comunicação com a API.
- **Métricas (`exectime.py`)**: Decorador para medir e logar o tempo de execução de cada tarefa.

## 4. Fluxo de Execução Principal (`main.py`)

1. Verifica atualizações do projeto.
2. Entra em loop para buscar novas tarefas na API.
3. Se encontrar uma tarefa:
    - Identifica o sistema e o caso de uso.
    - Invoca o `worker` para executar a automação.
    - Em caso de falha, coleta logs e screenshots.
    - Reporta o resultado final (Sucesso/Erro) para a API.
