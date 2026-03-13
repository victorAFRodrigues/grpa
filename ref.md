Chat preciso transformar o json abaixo na estrutura que vou instruir:
## estrutura de pastas:
```filesystem
automations/
   system_name/
        common/
            automation_part.py
        data/
            use_case.json
        use_cases/
            use_case.py
```
## como deve preencher cada dado:
1. system_name sera preenchido manualmente
2. use_case deve ser a mesma do json gerado pelo recorder, tanto dentro de data/ quanto dentro de use_cases/
3. automation_part deve ser modulos que os uses_cases utilizam em comum ou pra diminiuir a complexidade descrita em um arquivo só


## estrutura de cada arquivo:
### 1. automation_part.py
```python
from json import load
from core.browser_automation import PlaywrightElement, BrowserAutomation
from core.logger import Logger
from modules.utils.general.dotenv import DotEnv
from modules.utils.general.exectime import ExecTime


def run (page, log, data=None):

    try:
        page.goto('https://www.google.com')
        
        log.success("sucesso")

    except Exception as ex:
        log.error(ex)
        raise Exception(ex)

if __name__ == "__main__":
    _log = Logger('automations.system_name.common.automation_part').get_logger()

    path = f'../data/use_case.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'automation_part'):
        with BrowserAutomation() as _page:
            run(_page, _log, _data)

```

### 2. use_case.json
```json
{
  "campo":"valor"
}
```

### 2. use_case.py
```python
from json import load
from core.browser_automation import BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):
    try:
        page.goto('https://www.google.com')
        
        ret = 'sucesso'
        
        log.success(f"{ret}")

        return True, ret

    except Exception as ex:
        log.error("falha!")
        raise Exception(ex)


if __name__ == '__main__':
    _log = Logger("automations.system_name.use_cases.use_case").get_logger()

    path = f'../data/use_case.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'use_case'):
        with BrowserAutomation() as _page:
            try:
                run(_page, _log, _data)
            except Exception as ex:
                _log.error(ex)
                pass
```

## JSON de exemplo (retorno do recorder browser):

```json

{
    "title": "logar_goevo_lelac",
    "steps": [
        {
            "type": "setViewport",
            "width": 1257,
            "height": 951,
            "deviceScaleFactor": 1,
            "isMobile": false,
            "hasTouch": false,
            "isLandscape": false
        },
        {
            "type": "navigate",
            "url": "https://www.google.com/",
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://www.google.com/",
                    "title": "Google"
                }
            ]
        },
        {
            "type": "navigate",
            "url": "https://grupolelac.goevo.net/Empresas/Grupolelac/ModulesTetris/CFG/index.html#",
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://grupolelac.goevo.net/Empresas/Grupolelac/ModulesTetris/CFG/index.html#",
                    "title": "GoEvo Configurador"
                }
            ]
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "#form1"
                ],
                [
                    "xpath///*[@id=\"form1\"]"
                ],
                [
                    "pierce/#form1"
                ]
            ],
            "offsetY": 100,
            "offsetX": 124.5
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ]
            ],
            "offsetY": 14.703125,
            "offsetX": 117.5
        },
        {
            "type": "change",
            "value": "",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ]
            ],
            "offsetY": 22.703125,
            "offsetX": 54.5
        },
        {
            "type": "change",
            "value": "9c04c616",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Usuário ou Email"
                ],
                [
                    "#wucLogin_txtUsuario"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtUsuario\"]"
                ],
                [
                    "pierce/#wucLogin_txtUsuario"
                ]
            ],
            "offsetY": 13.703125,
            "offsetX": 61.5
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "CapsLock"
        },
        {
            "type": "keyUp",
            "key": "CapsLock",
            "target": "main"
        },
        {
            "type": "change",
            "value": "GOEVO",
            "selectors": [
                [
                    "aria/Usuário ou Email"
                ],
                [
                    "#wucLogin_txtUsuario"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtUsuario\"]"
                ],
                [
                    "pierce/#wucLogin_txtUsuario"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Acessar"
                ],
                [
                    "#wucLogin_btnLogin"
                ],
                [
                    "xpath///*[@id=\"wucLogin_btnLogin\"]"
                ],
                [
                    "pierce/#wucLogin_btnLogin"
                ],
                [
                    "text/Acessar"
                ]
            ],
            "offsetY": 3.703125,
            "offsetX": 27.765625,
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://grupolelac.goevo.net/ESB/TetrisACCESS/Login.aspx",
                    "title": "GoEvo Login"
                }
            ]
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ]
            ],
            "offsetY": 13.703125,
            "offsetX": 81.5
        },
        {
            "type": "change",
            "value": "9c04c616",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Usuário ou Email"
                ],
                [
                    "#wucLogin_txtUsuario"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtUsuario\"]"
                ],
                [
                    "pierce/#wucLogin_txtUsuario"
                ],
                [
                    "text/GOEVO"
                ]
            ],
            "offsetY": 7.703125,
            "offsetX": 109.5
        },
        {
            "type": "change",
            "value": "admin",
            "selectors": [
                [
                    "aria/Usuário ou Email"
                ],
                [
                    "#wucLogin_txtUsuario"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtUsuario\"]"
                ],
                [
                    "pierce/#wucLogin_txtUsuario"
                ],
                [
                    "text/GOEVO"
                ]
            ],
            "target": "main"
        },
        {
            "type": "change",
            "value": "3ff070de",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ],
                [
                    "text/9c04c616"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ],
                [
                    "text/3ff070de"
                ]
            ],
            "offsetY": 30.703125,
            "offsetX": 113.5
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ],
                [
                    "text/3ff070de"
                ]
            ],
            "offsetY": 29.703125,
            "offsetX": 112.5
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ],
                [
                    "text/3ff070de"
                ]
            ],
            "offsetY": 28.703125,
            "offsetX": 111.5
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "Control"
        },
        {
            "type": "keyDown",
            "target": "main",
            "key": "A"
        },
        {
            "type": "keyUp",
            "key": "A",
            "target": "main"
        },
        {
            "type": "change",
            "value": "9c04c616",
            "selectors": [
                [
                    "aria/Senha"
                ],
                [
                    "#wucLogin_txtSenha"
                ],
                [
                    "xpath///*[@id=\"wucLogin_txtSenha\"]"
                ],
                [
                    "pierce/#wucLogin_txtSenha"
                ],
                [
                    "text/9c04c616"
                ]
            ],
            "target": "main"
        },
        {
            "type": "keyUp",
            "key": "Control",
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Acessar"
                ],
                [
                    "#wucLogin_btnLogin"
                ],
                [
                    "xpath///*[@id=\"wucLogin_btnLogin\"]"
                ],
                [
                    "pierce/#wucLogin_btnLogin"
                ],
                [
                    "text/Acessar"
                ]
            ],
            "offsetY": 8.703125,
            "offsetX": 44.765625,
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://grupolelac.goevo.net/ESB/TetrisACCESS/Login.aspx",
                    "title": ""
                }
            ]
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "#wucLogin_ddlModulo"
                ],
                [
                    "xpath///*[@id=\"wucLogin_ddlModulo\"]"
                ],
                [
                    "pierce/#wucLogin_ddlModulo"
                ]
            ],
            "offsetY": 10.703125,
            "offsetX": 170.5
        },
        {
            "type": "change",
            "value": "SCM",
            "selectors": [
                [
                    "#wucLogin_ddlModulo"
                ],
                [
                    "xpath///*[@id=\"wucLogin_ddlModulo\"]"
                ],
                [
                    "pierce/#wucLogin_ddlModulo"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "#wucLogin_ddlModulo"
                ],
                [
                    "xpath///*[@id=\"wucLogin_ddlModulo\"]"
                ],
                [
                    "pierce/#wucLogin_ddlModulo"
                ]
            ],
            "offsetY": 15.703125,
            "offsetX": 139.5
        },
        {
            "type": "change",
            "value": "CFG",
            "selectors": [
                [
                    "#wucLogin_ddlModulo"
                ],
                [
                    "xpath///*[@id=\"wucLogin_ddlModulo\"]"
                ],
                [
                    "pierce/#wucLogin_ddlModulo"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "#wucLogin_ddlModulo"
                ],
                [
                    "xpath///*[@id=\"wucLogin_ddlModulo\"]"
                ],
                [
                    "pierce/#wucLogin_ddlModulo"
                ]
            ],
            "offsetY": 15.703125,
            "offsetX": 116.5
        },
        {
            "type": "change",
            "value": "SCM",
            "selectors": [
                [
                    "#wucLogin_ddlModulo"
                ],
                [
                    "xpath///*[@id=\"wucLogin_ddlModulo\"]"
                ],
                [
                    "pierce/#wucLogin_ddlModulo"
                ]
            ],
            "target": "main"
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/Acessar"
                ],
                [
                    "#wucLogin_btnLoginSelectApp"
                ],
                [
                    "xpath///*[@id=\"wucLogin_btnLoginSelectApp\"]"
                ],
                [
                    "pierce/#wucLogin_btnLoginSelectApp"
                ],
                [
                    "text/Acessar"
                ]
            ],
            "offsetY": 24.703125,
            "offsetX": 53.765625,
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://grupolelac.goevo.net/ESB/TetrisACCESS/Home.aspx?modulo=SCM&empresa=Grupolelac",
                    "title": ""
                }
            ]
        }
    ]
}

```