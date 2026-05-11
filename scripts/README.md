# Scripts de Instalação - GRPA

Este diretório contém scripts para instalação automatizada das dependências do projeto GRPA.

## Dependências Instaladas

| Dependência | Versão Mínima | Descrição |
|-------------|---------------|-----------|
| Docker | 20.0.0 | Containerização |
| Docker Compose | - | Orquestração de containers |
| Python | 3.14+ | Linguagem principal |
| uv | 0.10.2 | Gerenciador de pacotes Python |
| Playwright | - | Automação de navegador (Chromium) |

## Como Usar

### Linux/macOS

```bash
# Instalação completa (recomendado)
chmod +x scripts/install.sh
./scripts/install.sh

# Instalação com validação apenas
./scripts/install.sh --validate-only

# Pular Docker (se já instalado)
./scripts/install.sh --skip-docker

# Dry-run (apenas mostra o que seria feito)
./scripts/install.sh --dry-run
```

### Windows (PowerShell)

```powershell
# Instalação completa (recomendado)
.\scripts\install.ps1

# Instalação com validação apenas
.\scripts\install.ps1 -ValidateOnly

# Pular Docker (se já instalado)
.\scripts\install.ps1 -SkipDocker

# Dry-run (apenas mostra o que seria feito)
.\scripts\install.ps1 -DryRun
```

## Opções Disponíveis

| Opção (Linux) | Opção (Windows) | Descrição |
|---------------|-----------------|-----------|
| `--skip-docker` | `-SkipDocker` | Pula instalação do Docker |
| `--skip-python` | `-SkipPython` | Pula instalação do Python |
| `--skip-uv` | `-SkipUv` | Pula instalação do uv |
| `--skip-playwright` | `-SkipPlaywright` | Pula instalação do Playwright |
| `--dry-run` | `-DryRun` | Simula instalação sem executar |
| `--validate-only` | `-ValidateOnly` | Apenas valida instalação atual |
| `--help` | `-Help` | Mostra ajuda |

## Pós-Instalação

Após a instalação, execute na ordem:

```bash
# 1. Sincronizar dependências
uv sync

# 2. Configurar ambiente
python setup.py

# 3. Iniciar aplicação
grpa
```

## Solução de Problemas

### Docker não inicia no Linux
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Reiniciar sessão
```

### Python 3.14 não disponível
O script tentará instalar via gerenciador de pacotes. Se não disponível, use:
```bash
# Linux via pyenv
curl https://pyenv.run | bash
pyenv install 3.14
pyenv global 3.14
```

### uv não encontrado após instalação
```bash
# Adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"
```

## Requisitos do Sistema

### Linux
- Ubuntu 20.04+ / Debian 11+ / RHEL 8+ / Arch Linux
- sudo privileges
- 2GB RAM mínimo
- 5GB espaço em disco

### macOS
- macOS 11.0+
- Homebrew (recomendado)
- 2GB RAM mínimo
- 5GB espaço em disco

### Windows
- Windows 10 21H2+ / Windows 11
- PowerShell 7.0+
- WSL2 (para Docker no Windows)
- 4GB RAM mínimo
- 5GB espaço em disco

## Notas

- O script é **idempotente**: pode ser executado múltiplas vezes sem problemas
- A instalação do Docker requer privilégios de administrador
- O Playwright requer ~500MB para download dos browsers
- Em produção, considere usar `docker-compose -f docker-compose.prod.yml`
