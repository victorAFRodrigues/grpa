#!/bin/bash
# =============================================================================
# GRPA - Script de Instalação de Dependências
# =============================================================================
# Instala Docker, Docker Compose, Python 3.14+, uv e dependências do projeto
# =============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variáveis de versão
PYTHON_VERSION="3.14"
UV_VERSION="0.10.2"
MIN_DOCKER_VERSION="20.0.0"

# Flags
SKIP_DOCKER=false
SKIP_PYTHON=false
SKIP_UV=false
SKIP_PLAYWRIGHT=false
DRY_RUN=false

# =============================================================================
# Funções de Output
# =============================================================================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[ATENÇÃO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

log_step() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# =============================================================================
# Funções de Verificação
# =============================================================================
check_command() {
    command -v "$1" >/dev/null 2>&1
}

get_docker_version() {
    if check_command docker; then
        docker --version | grep -oP '\d+\.\d+\.\d+' | head -1
    else
        echo "0.0.0"
    fi
}

get_python_version() {
    if check_command python3; then
        python3 --version | grep -oP '\d+\.\d+' | head -1
    elif check_command python; then
        python --version | grep -oP '\d+\.\d+' | head -1
    else
        echo "0.0"
    fi
}

check_docker_compose() {
    if check_command docker-compose; then
        return 0
    elif docker compose version >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# =============================================================================
# Funções de Instalação - Docker
# =============================================================================
install_docker_linux() {
    log_info "Instalando Docker para Linux..."

    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        log_info "Detectado sistema Debian/Ubuntu"

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY-RUN] apt-get update"
            echo "[DRY-RUN] apt-get install -y docker.io docker-compose docker-buildx"
            return
        fi

        sudo apt-get update
        sudo apt-get install -y docker.io docker-compose docker-buildx
        sudo systemctl start docker
        sudo systemctl enable docker

    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS
        log_info "Detectado sistema RHEL/CentOS"

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY-RUN] yum install -y docker docker-compose"
            return
        fi

        sudo yum install -y docker docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker

    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        log_info "Detectado Arch Linux"

        if [ "$DRY_RUN" = true ]; then
            echo "[DRY-RUN] pacman -S docker docker-compose"
            return
        fi

        sudo pacman -S docker docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker
    else
        log_error "Distribuição Linux não suportada. Instale Docker manualmente."
        return 1
    fi

    log_success "Docker instalado com sucesso!"
}

install_docker_mac() {
    log_info "Instalando Docker no macOS..."

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] brew install --cask docker"
        return
    fi

    if ! check_command brew; then
        log_error "Homebrew não encontrado. Instale o Docker manualmente em https://www.docker.com/products/docker-desktop/"
        return 1
    fi

    brew install --cask docker
    log_success "Docker Desktop instalado! Reinicie o sistema e inicie o Docker Desktop."
}

# =============================================================================
# Funções de Instalaação - Python
# =============================================================================
install_python_linux() {
    log_info "Instalando Python ${PYTHON_VERSION}..."

    if [ -f /etc/debian_version ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY-RUN] apt-get install -y python3.14 python3.14-venv python3.14-dev"
            return
        fi

        sudo apt-get update
        sudo apt-get install -y python3.14 python3.14-venv python3.14-dev
        log_success "Python ${PYTHON_VERSION} instalado!"

    elif [ -f /etc/redhat-release ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY-RUN] yum install -y python3.14"
            return
        fi

        sudo yum install -y python3.14
        log_success "Python ${PYTHON_VERSION} instalado!"
    else
        log_warning "Instalação automática não disponível. Tentando pyenv..."
        install_python_pyenv
    fi
}

install_python_mac() {
    log_info "Instalando Python ${PYTHON_VERSION} no macOS..."

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] brew install python@3.14"
        return
    fi

    if check_command brew; then
        brew install python@3.14
        log_success "Python ${PYTHON_VERSION} instalado!"
    else
        log_error "Homebrew necessário. Instale em https://brew.sh"
        return 1
    fi
}

install_python_pyenv() {
    log_info "Instalando Python via pyenv..."

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] curl pyenv installer"
        echo "[DRY-RUN] pyenv install ${PYTHON_VERSION}"
        return
    fi

    # Instalar pyenv
    curl https://pyenv.run | bash

    # Adicionar ao shell
    shell_rc="$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        shell_rc="$HOME/.zshrc"
    fi

    cat << 'EOF' >> "$shell_rc"

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF

    source "$shell_rc"

    # Instalar Python
    pyenv install ${PYTHON_VERSION}
    pyenv global ${PYTHON_VERSION}

    log_success "Python ${PYTHON_VERSION} instalado via pyenv!"
}

# =============================================================================
# Funções de Instalação - uv
# =============================================================================
install_uv() {
    log_info "Instalando uv ${UV_VERSION}..."

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] curl -LsSf https://astral.sh/uv/install.sh | sh"
        return
    fi

    # Instalar uv
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Adicionar ao PATH se necessário
    if [ -f "$HOME/.local/bin/uv" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi

    log_success "uv instalado com sucesso!"
}

# =============================================================================
# Funções de Instalação - Playwright
# =============================================================================
install_playwright() {
    log_info "Instalando Playwright e dependências do navegador..."

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] uv run playwright install-deps chromium"
        echo "[DRY-RUN] uv run playwright install chromium"
        return
    fi

    # Instalar dependências do sistema para Playwright
    if [ -f /etc/debian_version ]; then
        sudo apt-get update
        sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y alsa-lib libdrm xorg-x11-server-Xorg xorg-x11-xauth xkbcore libxkbcommon nss at-spi2-atk
    fi

    # Instalar browsers do Playwright
    uv run playwright install-deps chromium
    uv run playwright install chromium

    log_success "Playwright instalado com sucesso!"
}

# =============================================================================
# Validações
# =============================================================================
validate_installation() {
    log_step "Validando instalação..."
    local errors=0

    # Validar Docker
    if check_command docker; then
        log_success "Docker: $(docker --version)"
    else
        log_error "Docker: NÃO INSTALADO"
        ((errors++))
    fi

    # Validar Docker Compose
    if check_docker_compose; then
        log_success "Docker Compose: instalado"
    else
        log_error "Docker Compose: NÃO INSTALADO"
        ((errors++))
    fi

    # Validar Python
    python_ver=$(get_python_version)
    if [[ "$python_ver" != "0.0" ]]; then
        log_success "Python: $python_ver"
    else
        log_error "Python: NÃO INSTALADO"
        ((errors++))
    fi

    # Validar uv
    if check_command uv; then
        log_success "uv: $(uv --version)"
    else
        log_error "uv: NÃO INSTALADO"
        ((errors++))
    fi

    # Validar dependências do projeto
    if [ -f "uv.lock" ]; then
        log_info "Verificando dependências do projeto..."
        if uv sync --check >/dev/null 2>&1; then
            log_success "Dependências do projeto: OK"
        else
            log_warning "Dependências do projeto: sincronizar com 'uv sync'"
        fi
    fi

    echo ""
    if [ $errors -eq 0 ]; then
        log_success "Todas as validações passaram!"
        return 0
    else
        log_error "$errors validação(ões) falharam"
        return 1
    fi
}

# =============================================================================
# Usage
# =============================================================================
show_usage() {
    cat << EOF
Uso: $0 [OPÇÕES]

Opções:
  --skip-docker      Pular instalação do Docker
  --skip-python      Pular instalação do Python
  --skip-uv          Pular instalação do uv
  --skip-playwright  Pular instalação do Playwright
  --dry-run          Mostra o que seria feito sem executar
  --validate-only    Apenas valida a instalação atual
  -h, --help         Mostra esta mensagem

Exemplo:
  $0 --skip-docker --validate-only
EOF
}

# =============================================================================
# Main
# =============================================================================
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-docker) SKIP_DOCKER=true; shift ;;
            --skip-python) SKIP_PYTHON=true; shift ;;
            --skip-uv) SKIP_UV=true; shift ;;
            --skip-playwright) SKIP_PLAYWRIGHT=true; shift ;;
            --dry-run) DRY_RUN=true; shift ;;
            --validate-only)
                validate_installation
                exit $?
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    log_step "Iniciando instalação GRPA"
    log_info "Sistema: $(uname -s) $(uname -m)"

    os_type=$(uname -s)

    # Docker
    if [ "$SKIP_DOCKER" = false ]; then
        if ! check_command docker || [ "$(get_docker_version)" = "0.0.0" ]; then
            if [ "$os_type" = "Linux" ]; then
                install_docker_linux
            elif [ "$os_type" = "Darwin" ]; then
                install_docker_mac
            else
                log_warning "Sistema não suportado para instalação automática do Docker"
            fi
        else
            log_info "Docker já está instalado: $(get_docker_version)"
        fi
    else
        log_info "Pulando instalação do Docker (--skip-docker)"
    fi

    # Python
    if [ "$SKIP_PYTHON" = false ]; then
        python_ver=$(get_python_version)
        if [[ "$python_ver" == "0.0" ]] || [[ "$python_ver" < "3.14" ]]; then
            if [ "$os_type" = "Linux" ]; then
                install_python_linux
            elif [ "$os_type" = "Darwin" ]; then
                install_python_mac
            else
                log_warning "Sistema não suportado para instalação automática do Python"
            fi
        else
            log_info "Python já está instalado: $python_ver"
        fi
    else
        log_info "Pulando instalação do Python (--skip-python)"
    fi

    # uv
    if [ "$SKIP_UV" = false ]; then
        if ! check_command uv; then
            install_uv
        else
            log_info "uv já está instalado: $(uv --version)"
        fi
    else
        log_info "Pulando instalação do uv (--skip-uv)"
    fi

    # Sync dependencies
    log_step "Sincronizando dependências do projeto..."
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] uv sync"
    else
        uv sync
        log_success "Dependências sincronizadas!"
    fi

    # Playwright
    if [ "$SKIP_PLAYWRIGHT" = false ]; then
        log_step "Verificando Playwright..."
        if ! command -v playwright >/dev/null 2>&1; then
            install_playwright
        else
            log_info "Playwright já está instalado"
        fi
    else
        log_info "Pulando instalação do Playwright (--skip-playwright)"
    fi

    # Validate
    validate_installation

    log_step "Instalação concluída!"
    log_info "Próximos passos:"
    echo "  1. Execute 'uv sync' para garantir dependências atualizadas"
    echo "  2. Execute 'python setup.py' para configurar o ambiente"
    echo "  3. Execute 'grpa' para iniciar a aplicação"
}

# Run main
main "$@"
