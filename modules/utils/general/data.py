import json
import re
from decimal import Decimal

# ---------------------------------------------------------------------------
# Funções de Auxiliares
# ---------------------------------------------------------------------------

def _clean_string(text: str) -> str:
    """
    Remove espaços de borda (trim) e colapsa múltiplos espaços internos em um só.
    Também remove caracteres de controle como \t, \n, \r.
    """
    if not text:
        return ""
    # substitui qualquer sequência de whitespace por um único espaço
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()

# ---------------------------------------------------------------------------
# Funções de Parsing Especial
# ---------------------------------------------------------------------------

def _parse_parcelas(raw: str) -> list[dict]:
    try:
        if not raw: return []
        data = json.loads(raw)
        if isinstance(data, dict): data = [data]

        return [
            {
                # Limpeza profunda em cada campo da parcela
                "valor": Decimal(_clean_string(p.get("VALOR", 0)).replace(',', '.')),
                "venc": _clean_string(p.get("VENC", ""))
            }
            for p in data
        ]
    except:
        return []


def _parse_pipe_semicolon(raw: str, keys: list[str]) -> list[dict]:
    if not raw: return []
    result = []
    for bloco in raw.split("|"):
        if not bloco.strip(): continue

        parts = [_clean_string(p) for p in bloco.split(";")]

        # --- NOVIDADE AQUI: Verifica se existe pelo menos um valor real nas partes ---
        # Se todas as partes forem strings vazias, ignoramos este bloco
        if not any(parts):
            continue

        parts += [""] * max(0, len(keys) - len(parts))
        result.append({k: parts[i] for i, k in enumerate(keys)})

    return result



# Mapeamento Centralizado de Campos Especiais
_SPECIAL_FIELDS = {
    "PSE_PARCE": _parse_parcelas,
    "ITENS_CONCATENADOS": lambda raw: _parse_pipe_semicolon(
        raw, ["item", "produt", "descri", "quant", "vlruni", "total", "xplaca", "cc", "conta", "ipi", "vldesc", "icms", "pis", "cofins", "icmsst", "seguro", "despesas", "valfre" ]
    ),
    "PSU_CC": lambda raw: _parse_pipe_semicolon(raw, ["cc", "dcc", "valor"]),
    "PSU_CONTA": lambda raw: _parse_pipe_semicolon(raw, ["conta", "dconta", "valor"]),
}


# ---------------------------------------------------------------------------
# Classe Data
# ---------------------------------------------------------------------------

class Data:
    def __init__(self, data_dict: dict):
        """Inicializa a classe diretamente com um dicionário já processado."""
        self._data = data_dict

    # --- Acesso estilo dicionário ---
    def __getitem__(self, key: str):
        return self._data.get(key.upper())

    def __setitem__(self, key: str, value):
        self._data[key.upper()] = value

    def __contains__(self, key: str):
        return key.upper() in self._data

    def keys(self):
        return self._data.keys()

    def get(self, key: str, default=None):
        return self._data.get(key.upper(), default)

    # --- Visualização e Debug ---
    def __repr__(self):
        return f"Data({list(self._data.keys())})"

    def __str__(self):
        """Retorna todos os dados convertidos em formato JSON bonito para printar."""
        return json.dumps(self._data, indent=4, default=str, ensure_ascii=False)

    def to_dict(self) -> dict:
        """Retorna o dicionário interno (útil para integrações)."""
        return self._data

    # --- Métodos de Construção (Factory) ---
    @classmethod
    def from_raw(cls, raw_input: str | list | dict) -> "Data":
        """
        Ponto de entrada principal.
        Aceita JSON string, lista ou dicionário vindo do Protheus/RPA.
        """
        data = raw_input
        if isinstance(raw_input, str):
            try:
                data = json.loads(raw_input)
            except json.JSONDecodeError:
                return cls({})

        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        if isinstance(data, dict) and "RPA_PARAMS" in data:
            params = data["RPA_PARAMS"]
            if isinstance(params, str):
                try:
                    data = json.loads(params)
                except json.JSONDecodeError:
                    pass
            else:
                data = params

        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        if not isinstance(data, dict):
            return cls({})

        return cls._parse_logic(data)

    @classmethod
    def _parse_logic(cls, d: dict) -> "Data":
        processed = {}

        # 1. Primeiro passamos por todos os campos para fazer o parse básico
        for key, value in d.items():
            upper_key = key.upper()
            raw_val = _clean_string(value)

            if upper_key in _SPECIAL_FIELDS:
                processed[upper_key] = _SPECIAL_FIELDS[upper_key](raw_val)
            else:
                processed[upper_key] = raw_val

        # 2. Aplicação da regra de fallback para PSU_CC e PSU_CONTA
        itens = processed.get("ITENS_CONCATENADOS", [])

        if itens:
            primeiro_item = itens[0]

            # Fallback para PSU_CC
            if not processed.get("PSU_CC"):
                processed["PSU_CC"] = [{
                    "cc": primeiro_item.get("cc", ""),
                    "dcc": "",
                    "valor": primeiro_item.get("total", "0")
                }]

            # Fallback para PSU_CONTA
            if not processed.get("PSU_CONTA"):
                processed["PSU_CONTA"] = [{
                    "conta": primeiro_item.get("conta", ""),
                    "dconta": "",
                    "valor": primeiro_item.get("total", "0")
                }]

        return cls(processed)