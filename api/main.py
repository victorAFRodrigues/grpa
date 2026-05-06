import json
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from middlewares.nocache import NoCacheMiddleware

# Patch for newer Jinja2Templates signature
_original_init = Jinja2Templates.__init__
def _patched_init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)
    self.env.trim_blocks = True
    self.env.lstrip_blocks = True
Jinja2Templates.__init__ = _patched_init
import httpx

app = FastAPI(title="GRPA Configurator")

app.add_middleware(NoCacheMiddleware)

app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="api/templates")

ENV_FILE = Path(".env")


def read_env() -> dict:
    """Read environment variables from .env file."""
    data = {
        "urlBase": "",
        "companyId": "",
        "usuario": "",
        "senha": "",
        "API_URL": "",
        "GOEVO_APP_TPTOKEN": "",
        "RPA_EXECUTOR": "",
        "RPA_VERSION": "v1.0.0",
        "ENVIRONMENT": "local",
    }
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"')
            # Map to template variable names
            key_map = {
                "API_URL": "API_URL",
                "GOEVO_APP_TPTOKEN": "GOEVO_APP_TPTOKEN",
                "RPA_EXECUTOR": "RPA_EXECUTOR",
                "RPA_VERSION": "RPA_VERSION",
                "ENVIRONMENT": "ENVIRONMENT",
            }
            if key in key_map:
                data[key_map[key]] = val
    return data


def is_configured() -> bool:
    """Verifica se as variáveis obrigatórias estão preenchidas no .env"""
    if not ENV_FILE.exists():
        return False

    data = read_env()
    # Lista de chaves que NÃO podem estar vazias para o Worker funcionar
    required_keys = [
        "API_URL",
        "GOEVO_APP_TPTOKEN",
        "RPA_EXECUTOR"
    ]

    for key in required_keys:
        value = data.get(key, "").strip()
        if not value or value == "None":
            return False

    # Verificação específica para a versão
    version = data.get("RPA_VERSION", "")
    if not version or version == "Selecione..":
        return False

    return True


@app.get("/health")
async def health_check():
    """Endpoint para o Docker Compose monitorar"""
    if is_configured():
        return JSONResponse({"status": "ready", "configured": True}, status_code=200)

    return JSONResponse(
        {"status": "awaiting_configuration", "configured": False},
        status_code=503 # Indica que o serviço está no ar, mas não pronto
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render wizard form."""
    env_data = read_env()
    return templates.TemplateResponse(
        request=request,
        name="wizard.html",
        context={
            "env_data": env_data,
            "flash": None,
            "flash_type": None,
        }
    )


@app.post("/validate-login")
async def validate_login(request: Request):
    """Validate login credentials against GoEvo API."""
    try:
        body = await request.json()
        urlBase = body.get("urlBase", "").strip()
        companyId = body.get("companyId", "").strip()
        usuario = body.get("usuario", "").strip()
        senha = body.get("senha", "")
    except Exception:
        return JSONResponse({"success": False, "error": "JSON inválido"}, status_code=400)

    # Validate required fields
    errors = []
    if not urlBase:
        errors.append("URL Base é obrigatória.")
    if not companyId:
        errors.append("Company ID é obrigatório.")
    if not usuario:
        errors.append("Usuário é obrigatório.")
    if not senha:
        errors.append("Senha é obrigatória.")

    if errors:
        return JSONResponse({"success": False, "error": " ".join(errors)}, status_code=400)

    # Try to login to GoEvo API
    try:
        urlBase = urlBase.rstrip('/')
        login_url = f"{urlBase}/ESB/ResourceFiles/wsLogin.ashx"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                login_url,
                data={"usuario": usuario, "senha": senha},
                params={"COMPANY_ID": companyId}
            )

            # Check for error in response
            try:
                response_data = json.loads(response.text)
                if isinstance(response_data, dict) and response_data.get("errorcode") == "01":
                    return JSONResponse({
                        "success": False,
                        "error": "Usuário ou senha inválidos (ERROR CODE: 01)"
                    })
            except Exception:
                pass

            if response.status_code != 200:
                return JSONResponse({
                    "success": False,
                    "error": f"Erro na autenticação: HTTP {response.status_code}"
                })
    except httpx.TimeoutException:
        return JSONResponse({"success": False, "error": "Tempo esgotado ao conectar com GoEvo."})
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Erro de conexão: {str(e)}"})

    # Login successful - return generated API URL
    # Extract domain from urlBase
    from urllib.parse import urlparse
    parsed = urlparse(urlBase if urlBase.startswith('http') else f'https://{urlBase}')
    domain = f"{parsed.scheme}://{parsed.hostname}"
    api_url = f"{domain}/API/v1/?{companyId}/RPAManager"

    return JSONResponse({
        "success": True,
        "api_url": api_url
    })


@app.post("/list-rpa-versions")
async def list_rpa_versions(request: Request):
    """Fetch RPA versions from GoEvo API."""
    try:
        body = await request.json()
        api_url = body.get("api_url", "").strip()
        token = body.get("token", "").strip()
    except Exception:
        return JSONResponse({"success": False, "error": "JSON inválido"}, status_code=400)

    if not api_url or not token:
        return JSONResponse({"success": False, "error": "API URL e token são obrigatórios"}, status_code=400)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{api_url}/ListaRpa",
                headers={"goevo_app_tptoken": token}
            )

            response_data = json.loads(response.text)

            # Check for error code
            if isinstance(response_data, dict) and response_data.get("errorcode") == "01":
                return JSONResponse({
                    "success": False,
                    "error": "Erro ao buscar versões RPA. Verifique o token.",
                    "errorcode": "01"
                })

            # Parse content JSON string
            versions = []
            if response_data.get("content"):
                try:
                    content_data = json.loads(response_data["content"])
                    if isinstance(content_data, list):
                        versions = content_data
                except json.JSONDecodeError:
                    pass

            return JSONResponse({
                "success": True,
                "versions": versions
            })

    except httpx.TimeoutException:
        return JSONResponse({"success": False, "error": "Tempo esgotado ao conectar com GoEvo."})
    except json.JSONDecodeError:
        return JSONResponse({"success": False, "error": "Resposta inválida da API"})
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Erro de conexão: {str(e)}"})


@app.post("/save-config")
async def save_config(request: Request):
    """Save configuration to .env file."""
    form_data = await request.form()

    # Get or generate API URL
    api_url = form_data.get('API_URL', '')
    if not api_url:
        # Generate from urlBase and companyId if not provided
        url_base = form_data.get('urlBase', '')
        company_id = form_data.get('companyId', '')
        if url_base and company_id:
            from urllib.parse import urlparse
            parsed = urlparse(url_base if url_base.startswith('http') else f'https://{url_base}')
            domain = f"{parsed.scheme}://{parsed.hostname}"
            api_url = f"{domain}/API/v1/?{company_id}/RPAManager"

    content = f"""\
# ==================================================================== #
# Arquivo .env #
# Contém todas as variáveis de ambiente necessárias para #
# execução das automações RPA. #
# #
# ATENÇÃO: #
# 1. Não compartilhe este arquivo publicamente (contém credenciais). #
# 2. Não faça commit no GitHub de arquivos com senhas em texto plano. #
# 3. Sempre faça o build do executável após alterar variáveis. #
# ==================================================================== #

# ===================== #
# Configurações gerais #
# ===================== #
API_URL="{api_url}"
GOEVO_APP_TPTOKEN="{form_data.get('GOEVO_APP_TPTOKEN', '')}"
RPA_EXECUTOR="{form_data.get('RPA_EXECUTOR', '')}"
GRPA_AUTOMATION_VERSION="{form_data.get('RPA_VERSION', 'Selecione..')}"
ENV="{form_data.get('ENVIRONMENT', 'LOCAL')}"

# =================== #
# Variáveis dinâmicas #
# =================== #
APPLICATION=""
SEARCH_TIMEOUT=""
SYSTEM_URL=""
USER=""
PASSWORD=""
"""

    ENV_FILE.write_text(content, encoding="utf-8")
    return RedirectResponse(url="/success", status_code=303)


@app.get("/success")
async def success(request: Request):
    """Success page."""
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
