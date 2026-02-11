class Migrations:
    def natureza_de_operacao():
        select = Select(SE(driver, "css", 'select[id="vNOTAFISCAL_NATUREZAOPERACAOCOD"]').find())
        opcoes = []
        for opt in select.options:
            opcoes.append({
                "value": opt.get_attribute("value"),
                "text": opt.text.strip()
            })
        atualiza_naturezas_operacao.run(opcoes)

        db = Database()
        db.cursor.execute(F"SELECT code FROM naturezas_de_operacao WHERE name = '{natureza_operacao_str}'")