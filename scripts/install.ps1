# =============================================================================
# GRPA - Script de Instalação de Dependências (PowerShell)
# =============================================================================
# Instala Docker, Docker Compose, Python 3.14+, uv e dependências do projeto
# =============================================================================

#Requires -Version 7.0

# Configurações
$PYTHON_VERSION = "3.14"
$UV_VERSION = "0.10.2"
$ErrorActionPreference = "Stop"

# Flags
$SkipDocker = $false
$SkipPython = $false
$SkipUv = $false
$SkipPlaywright = $false
$DryRun = $false
$ValidateOnly = $false

# =============================================================================
# Funções de Output
# =============================================================================
function Log-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Log-Success {
    param([string]$Message)
    Write-Host "[SUCESSO] $Message" -ForegroundColor Green
}

function Log-Warning {
    param([string]$Message)
    Write-Host "[ATENÇÃO] $Message" -ForegroundColor Yellow
}

function Log-Error {
    param([string]$Message)
    Write-Host "[ERRO] $Message" -ForegroundColor Red
}

function Log-Step {
    param([string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

# =============================================================================
# Funções de Verificação
# =============================================================================
function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-DockerVersion {
    try {
        $version = docker --version 2>&1
        if ($version) {
            return ($version -match '\d+\.\d+\.\d+' ? $matches[0] : "0.0.0")
        }
    } catch {
        return "0.0.0"
    }
    return "0.0.0"
}

function Get-PythonVersion {
    try {
        $version = python --version 2>&1
        if ($version -match 'Python (\d+\.\d+)') {
            return $matches[1]
        }
    } catch {
        try {
            $version = python3 --version 2>&1
            if ($version -match 'Python (\d+\.\d+)') {
                return $matches[1]
            }
        } catch {}
    }
    return "0.0"
}

function Test-DockerCompose {
    try {
        # Testa docker-compose (antigo)
        if (Test-Command "docker-compose") {
            return $true
        }
        # Testa docker compose (novo plugin)
        $result = docker compose version 2>&1
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# =============================================================================
# Funções de Instalação - Docker
# =============================================================================
function Install-Docker {
    Log-Info "Instalando Docker Desktop para Windows..."

    if ($DryRun) {
        Write-Host "[DRY-RUN] winget install --id Docker.DockerDesktop"
        return
    }

    # Tenta winget primeiro
    if (Test-Command "winget") {
        Log-Info "Instalando via winget..."
        winget install --id Docker.DockerDesktop --silent --accept-package-agreements --accept-source-agreements
    }
    # Tenta Chocolatey
    elseif (Test-Command "choco") {
        Log-Info "Instalando via Chocolatey..."
        choco install docker-desktop -y
    }
    else {
        Log-Error "Nenhum gerenciador de pacotes encontrado (winget/choco)"
        Log-Info "Baixe Docker Desktop em: https://www.docker.com/products/docker-desktop/"
        return $false
    }

    Log-Success "Docker Desktop instalado! Reinicie o sistema se necessário."
    return $true
}

# =============================================================================
# Funções de Instalação - Python
# =============================================================================
function Install-Python {
    Log-Info "Instalando Python $PYTHON_VERSION..."

    if ($DryRun) {
        Write-Host "[DRY-RUN] winget install --id Python.Python.3.14"
        return
    }

    if (Test-Command "winget") {
        winget install --id Python.Python.3.14 --silent --accept-package-agreements --accept-source-agreements
    }
    elseif (Test-Command "choco") {
        choco install python314 -y
    }
    else {
        Log-Error "Nenhum gerenciador de pacotes encontrado"
        Log-Info "Baixe Python 3.14 em: https://www.python.org/downloads/"
        return $false
    }

    Log-Success "Python $PYTHON_VERSION instalado!"
    return $true
}

# =============================================================================
# Funções de Instalação - uv
# =============================================================================
function Install-Uv {
    Log-Info "Instalando uv $UV_VERSION..."

    if ($DryRun) {
        Write-Host "[DRY-RUN] powershell -ExecutionPolicy Bypass -Command `" irm https://astral.sh/uv/install.ps1 | iex `""
        return
    }

    # Instala via script oficial
    $env:POWERSHELL_TELEMETRY_OPTOUT = "1"
    irm https://astral.sh/uv/install.ps1 | iex

    Log-Success "uv instalado com sucesso!"
    return $true
}

# =============================================================================
# Funções de Instalação - Playwright
# =============================================================================
function Install-Playwright {
    Log-Info "Instalando Playwright e dependências..."

    if ($DryRun) {
        Write-Host "[DRY-RUN] uv run playwright install-deps chromium"
        Write-Host "[DRY-RUN] uv run playwright install chromium"
        return
    }

    # Instala dependências do sistema
    Log-Info "Instalando dependências do sistema para Playwright..."

    # Instala browsers do Playwright
    uv run playwright install-deps chromium
    uv run playwright install chromium

    Log-Success "Playwright instalado com sucesso!"
    return $true
}

# =============================================================================
# Validações
# =============================================================================
function Validate-Installation {
    Log-Step "Validando instalação..."
    $errors = 0

    # Validar Docker
    if (Test-Command "docker") {
        Log-Success "Docker: $(Get-DockerVersion)"
    } else {
        Log-Error "Docker: NÃO INSTALADO"
        $errors++
    }

    # Validar Docker Compose
    if (Test-DockerCompose) {
        Log-Success "Docker Compose: instalado"
    } else {
        Log-Error "Docker Compose: NÃO INSTALADO"
        $errors++
    }

    # Validar Python
    $pythonVer = Get-PythonVersion
    if ($pythonVer -ne "0.0") {
        Log-Success "Python: $pythonVer"
    } else {
        Log-Error "Python: NÃO INSTALADO"
        $errors++
    }

    # Validar uv
    if (Test-Command "uv") {
        Log-Success "uv: $(uv --version)"
    } else {
        Log-Error "uv: NÃO INSTALADO"
        $errors++
    }

    # Validar dependências do projeto
    if (Test-Path "uv.lock") {
        Log-Info "Verificando dependências do projeto..."
        try {
            uv sync --check 2>&1 | Out-Null
            Log-Success "Dependências do projeto: OK"
        } catch {
            Log-Warning "Dependências do projeto: sincronizar com 'uv sync'"
        }
    }

    Write-Host ""
    if ($errors -eq 0) {
        Log-Success "Todas as validações passaram!"
        return $true
    } else {
        Log-Error "$errors validação(ões) falharam"
        return $false
    }
}

# =============================================================================
# Usage
# =============================================================================
function Show-Usage {
    Write-Host @"
Uso: .\install.ps1 [OPÇÕES]

Opções:
  -SkipDocker      Pular instalação do Docker
  -SkipPython      Pular instalação do Python
  -SkipUv          Pular instalação do uv
  -SkipPlaywright  Pular instalação do Playwright
  -DryRun          Mostra o que seria feito sem executar
  -ValidateOnly    Apenas valida a instalação atual
  -Help            Mostra esta mensagem

Exemplo:
  .\install.ps1 -SkipDocker -ValidateOnly
"@
}

# =============================================================================
# Parse Arguments
# =============================================================================
param(
    [switch]$SkipDocker,
    [switch]$SkipPython,
    [switch]$SkipUv,
    [switch]$SkipPlaywright,
    [switch]$DryRun,
    [switch]$ValidateOnly,
    [switch]$Help
)

# =============================================================================
# Main
# =============================================================================
if ($Help) {
    Show-Usage
    exit 0
}

if ($ValidateOnly) {
    Validate-Installation
    exit 0
}

try {
    Log-Step "Iniciando instalação GRPA"
    Log-Info "Sistema: Windows $(Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentName' -ProductName)"

    # Docker
    if (-not $SkipDocker) {
        if (-not (Test-Command "docker")) {
            Install-Docker
        } else {
            Log-Info "Docker já está instalado: $(Get-DockerVersion)"
        }
    } else {
        Log-Info "Pulando instalação do Docker (-SkipDocker)"
    }

    # Python
    if (-not $SkipPython) {
        $pythonVer = Get-PythonVersion
        if ($pythonVer -eq "0.0" -or [float]::Parse($pythonVer, [System.Globalization.CultureInfo]::InvariantCulture) -lt 3.14) {
            Install-Python
        } else {
            Log-Info "Python já está instalado: $pythonVer"
        }
    } else {
        Log-Info "Pulando instalação do Python (-SkipPython)"
    }

    # uv
    if (-not $SkipUv) {
        if (-not (Test-Command "uv")) {
            Install-Uv
        } else {
            Log-Info "uv já está instalado: $(uv --version)"
        }
    } else {
        Log-Info "Pulando instalação do uv (-SkipUv)"
    }

    # Sync dependencies
    Log-Step "Sincronizando dependências do projeto..."
    if (-not $DryRun) {
        uv sync
        Log-Success "Dependências sincronizadas!"
    } else {
        Write-Host "[DRY-RUN] uv sync"
    }

    # Playwright
    if (-not $SkipPlaywright) {
        Log-Step "Verificando Playwright..."
        if (-not (Test-Command "playwright")) {
            Install-Playwright
        } else {
            Log-Info "Playwright já está instalado"
        }
    } else {
        Log-Info "Pulando instalação do Playwright (-SkipPlaywright)"
    }

    # Validate
    Validate-Installation

    Log-Step "Instalação concluída!"
    Log-Info "Próximos passos:"
    Write-Host "  1. Execute 'uv sync' para garantir dependências atualizadas"
    Write-Host "  2. Execute 'python setup.py' para configurar o ambiente"
    Write-Host "  3. Execute 'grpa' para iniciar a aplicação"

} catch {
    Log-Error "Erro durante instalação: $_"
    exit 1
}
