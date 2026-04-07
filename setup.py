import os
import sys
import subprocess

ENV_FILE = ".env"

# ── ANSI colors ────────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    WHITE   = "\033[97m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    BG_DARK = "\033[48;5;235m"

W = 68  # largura do box

def line(char="─", color=C.CYAN):
    print(f"{color}{'─' * W}{C.RESET}")

def box_line(text="", color=C.CYAN, text_color=C.WHITE):
    inner = W - 2
    print(f"{color}│{C.RESET}{text_color}{text:<{inner}}{C.RESET}{color}│{C.RESET}")

def header():
    os.system("cls" if sys.platform == "win32" else "clear")
    print()
    print(f"{C.CYAN}╔{'═' * W}╗{C.RESET}")
    box_line(f"  {'GRPA — Setup Wizard':^{W-4}}  ", C.CYAN, C.BOLD + C.WHITE)
    box_line(f"  {'Configuração do ambiente de automação RPA':^{W-4}}  ", C.CYAN, C.DIM + C.WHITE)
    print(f"{C.CYAN}╚{'═' * W}╝{C.RESET}")
    print()

def section(title: str):
    print()
    print(f"{C.CYAN}┌{'─' * W}┐{C.RESET}")
    inner = W - 2
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}{C.YELLOW}{title}{C.RESET}{' ' * (inner - len(title) - 1)}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{'─' * W}┘{C.RESET}")

def info(text: str):
    print(f"  {C.DIM}{C.WHITE}{text}{C.RESET}")

def success(text: str):
    print(f"\n  {C.GREEN}✔  {text}{C.RESET}")

def warn(text: str):
    print(f"  {C.YELLOW}⚠  {text}{C.RESET}")

def ask(label, description=None, example=None, default=None, required=False):
    if description:
        print(f"\n  {C.BOLD}{C.WHITE}{label}{C.RESET}")
        info(description)
    else:
        print(f"\n  {C.BOLD}{C.WHITE}{label}{C.RESET}")

    if example:
        info(f"Exemplo: {example}")
    if default:
        info(f"Padrão : {default}")

    tag = f"{C.RED}*{C.RESET}" if required else f"{C.DIM}?{C.RESET}"

    while True:
        prompt = f"  {tag} {C.CYAN}›{C.RESET} "
        value = input(prompt).strip()
        if not value and default:
            value = default
        if required and not value:
            warn("Esse campo é obrigatório.")
            continue
        return value

# ── .env writer ────────────────────────────────────────────────────────────────
ENV_TEMPLATE = """\
# ==================================================================== #
# Arquivo .env                                                         #
# Contém todas as variáveis de ambiente necessárias para               #
# execução das automações RPA.                                         #
#                                                                      #
# ATENÇÃO:                                                             #
# 1. Não compartilhe este arquivo publicamente (contém credenciais).   #
# 2. Não faça commit no GitHub de arquivos com senhas em texto plano.  #
# 3. Sempre faça o build do executável após alterar variáveis.         #
# ==================================================================== #

# ===================== #
# Configurações gerais  #
# ===================== #
API_URL="{API_URL}" # URL base da API utilizada pelas automações. (OBRIGATÓRIO)
GOEVO_APP_TPTOKEN="{GOEVO_APP_TPTOKEN}" # Token de autenticação do app no GOEVO (OBRIGATÓRIO)
RPA_EXECUTOR="{RPA_EXECUTOR}" # Identificador do executor RPA (nome do servidor ou agente)
GRPA_AUTOMATION_VERSION="{GRPA_AUTOMATION_VERSION}" # Identificador da versão dos módulos de automação (OBRIGATÓRIO)
ENV="{ENV}" # Modo de execução: DOCKER (headless) ou LOCAL (com janela) (OPCIONAL)

# =================== #
# Variáveis dinâmicas #
# =================== #
APPLICATION=""
SEARCH_TIMEOUT=""
SYSTEM_URL=""
USER=""
PASSWORD=""
"""

def create_env_file(data: dict):
    content = ENV_TEMPLATE.format(**data)
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    success(f"Arquivo {ENV_FILE} criado com sucesso!")

# ── alias setup ────────────────────────────────────────────────────────────────
def setup_grpa_alias():
    is_windows = sys.platform == "win32"

    if is_windows:
        profile_cmd = subprocess.run(
            ["powershell", "-Command", "echo $PROFILE"],
            capture_output=True, text=True
        )
        profile_path = profile_cmd.stdout.strip()
        alias_line = '\nfunction grpa { uv run poe $args }\n'
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)

        existing = ""
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                existing = f.read()

        if "function grpa" not in existing:
            with open(profile_path, "a", encoding="utf-8") as f:
                f.write(alias_line)
            success(f"Alias 'grpa' adicionado no PowerShell profile.")
            info(f"Caminho: {profile_path}")
            info("Reinicie o PowerShell ou rode: . $PROFILE")
        else:
            info("Alias 'grpa' já existe no PowerShell profile.")
    else:
        alias_line = '\nalias grpa="uv run poe"\n'
        shell = os.environ.get("SHELL", "")
        rc_file = os.path.expanduser("~/.zshrc" if "zsh" in shell else "~/.bashrc")

        existing = ""
        if os.path.exists(rc_file):
            with open(rc_file, "r", encoding="utf-8") as f:
                existing = f.read()

        if 'alias grpa=' not in existing:
            with open(rc_file, "a", encoding="utf-8") as f:
                f.write(alias_line)
            success(f"Alias 'grpa' adicionado em: {rc_file}")
            info(f"Rode: source {rc_file}")
        else:
            info("Alias 'grpa' já existe.")

# ── main ───────────────────────────────────────────────────────────────────────
def start():
    header()

    section("① Conexão com a API")
    api_url = ask(
        "API_URL",
        description="URL base da API do RPAManager utilizada pelas automações.",
        example="https://empresa.goevo.net/API/v1/?EmpresaXYZ/RPAManager",
        required=True,
    )
    token = ask(
        "GOEVO_APP_TPTOKEN",
        description="Token de autenticação do aplicativo no GOEVO.\n"
                    "  Encontrado em: GOEVO Configurador › Usuarios › Editar Usuario [RPA MANAGER] › API > Token da API GoEvo (goevo_app_tptoken).",
        example="89a8e179-6cf4-4907-b1c1-b52f1f39738e",
        required=True,
    )

    section("② Identificação do Executor")
    executor = ask(
        "RPA_EXECUTOR",
        description="Nome que identifica este servidor/agente de automação.\n"
                    "  Use um nome único por máquina para rastreabilidade nos logs.",
        example="SRV_RPA_001  ou  NOTEBOOK_JOAO",
        required=True,
    )

    section("③ Versão e Ambiente")
    version = ask(
        "GRPA_AUTOMATION_VERSION",
        description="Versão dos módulos de automação. Usada para controle de atualização.",
        example="2.0.0.20260306",
        default="2.0.0.0",
    )
    env = ask(
        "ENV",
        description="Modo de execução:\n"
                    "  • DOCKER → headless (sem interface gráfica, para servidores)\n"
                    "  • LOCAL  → com janela visível (para desenvolvimento e testes)",
        example="DOCKER",
        default="DOCKER",
    )

    section("④ Configurando atalho 'grpa'")
    setup_grpa_alias()

    section("⑤ Gerando .env")
    create_env_file({
        "API_URL": api_url,
        "GOEVO_APP_TPTOKEN": token,
        "RPA_EXECUTOR": executor,
        "GRPA_AUTOMATION_VERSION": version,
        "ENV": env,
    })

    print()
    print(f"{C.CYAN}╔{'═' * W}╗{C.RESET}")
    box_line(f"  {'Setup concluído com sucesso! 🚀':^{W-4}}  ", C.CYAN, C.BOLD + C.GREEN)
    box_line(f"  {'Execute: grpa start':^{W-4}}  ", C.CYAN, C.DIM + C.WHITE)
    print(f"{C.CYAN}╚{'═' * W}╝{C.RESET}")
    print()

if __name__ == "__main__":
    start()