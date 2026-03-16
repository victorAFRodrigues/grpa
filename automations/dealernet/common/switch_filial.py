from json import load
from automations.dealernet.common import login
from core.browser_automation import PlaywrightElement, BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run (page, log, filial):
    try:
        PlaywrightElement(page, '#ext-gen67').action('click')

        marcas = ['JEEP', 'CITROEN', 'HYUNDAI', 'PEUGEOT', 'OUTRAS']

        has_found = False

        filial_name = ''

        for marca in marcas:
            page.locator('.x-menu-floating .x-menu-item-text', has_text=marca).hover()

            try:
                filial_item = PlaywrightElement(page, f'a[id="{filial}"]', 200)
                if filial_item.find():
                    filial_item.action('click')
                    PlaywrightElement(page, "#W0038TABLECENTRO", 4000).find()
                    log.success('Filial Trocada!')
                break
            except Exception:
                pass

        if not has_found:
            filial_name = PlaywrightElement(page, '#ext-gen67').find().inner_text().strip()
            raise Exception(f'A filial com numero {filial} não foi encontrada. Sera mantida a filial {filial_name} durante a execucao da task')

        return True

    except Exception as ex:
        log.warning(ex)
        raise Exception(ex)

if __name__ == "__main__":
    _log = Logger('automations.dealernet.common.switch_filial').get_logger()

    path = f'../data/validar_fornecedor.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'switch filial'):
        with BrowserAutomation() as _page:

            try:
                login.run(_page, _log)

                run(_page, _log, _data['filial'])
            except Exception as ex:
                pass
