"""Contém as variáveis e funções necessárias para a execução da Calculadora de Coisas."""

from math import pi
import os
import requests
import time
from datetime import timedelta

# Diretório raiz da aplicação e caminho para o ícone utilizado na UI
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_FILE = os.path.join(APP_DIR, "images", "favicon.png")

# Opções do Menu de Conversão agrupadas por categoria
CONVERSION_OPTIONS = {
    "Ângulo": (
        "Grau",
        "Radiano",
        "Grado",
    ),  # OK
    "Área": (
        "Centímetro Quadrado (cm²)",
        "Metro Quadrado (m²)",
        "Quilômetro Quadrado (km²)",
        "Hectare (ha)",
    ),  # OK
    "Comprimento": (
        "Milímetro (mm)",
        "Centímetro (cm)",
        "Metro (m)",
        "Quilômetro (km)",
        "Milha (mi)",
        "Pé (ft)",
        "Polegada (in)",
    ),  # OK
    "Contagem": (
        "Unidade",
        "Dezena",
        "Centena",
        "Milhar",
        "Milhão",
        "Bilhão",
        "Trilhão",
    ),  # OK
    "Dados": (
        "Bit (b)",
        "Byte (B)",
        "Kilobyte (kB)",
        "Megabyte (MB)",
        "Gigabyte (GB)",
        "Terabyte (TB)",
    ),  # OK
    "Energia": (
        "Joule (J)",
        "Caloria Alimentar (kcal)",
        "Quilowatt-hora (kWh)",
    ),  # OK
    "Frequência": (
        "Hertz (Hz)",
        "Quilo-hertz (kHz)",
        "Mega-hertz (MHz)",
        "Gigahertz (GHz)",
    ),  # OK
    "Moeda": (
        "Real (BRL)",
        "Dólar (USD)",
        "Euro (EUR)",
        "Bitcoin (BTC)",
    ),  # OK
    "Numeração": (
        "Binário",
        "Octal",
        "Decimal",
        "Hexadecimal",
    ),  # OK
    "Peso": (
        "Miligrama (mg)",
        "Grama (g)",
        "Quilograma (kg)",
        "Tonelada (t)",
        "Libra (lb)",
    ),  # OK
    "Potência": (
        "Watt (W)",
        "Quilowatt (kW)",
        "Cavalo-Vapor (hp)",
    ),  # OK
    "Pressão": (
        "Atmosfera (atm)",
        "Milímetro de Mercúrio (mmHg)",
        "Pascal (Pa)",
    ),  # OK
    "Temperatura": (
        "Celsius",
        "Fahrenheit",
        "Kelvin",
    ),  # OK
    "Tempo": (
        "Milissegundo",
        "Segundo",
        "Minuto",
        "Hora",
        "Dia",
        "Semana",
        "Mês",
        "Ano",
        "Década",
        "Século",
        "Milênio",
    ),  # OK
    "Velocidade": (
        "Centímetro por Segundo (cm/s)",
        "Metro por Segundo (m/s)",
        "Quilômetro por Hora (km/h)",
        "Milha por Hora (mph)",
        "Mach (Ma)",
    ),  # OK
    "Volume": (
        "Mililitro (mL)",
        "Litro (L)",
        "Metro Cúbico (m³)",
    ),  # OK
}

# Fatores de Conversão (o quanto da base há em 1 unidade)
CONVERSION_FACTORS = {
    "Área": {
        "base": "Metro Quadrado (m²)",
        "unidades": {
            "Centímetro Quadrado (cm²)": 0.0001,
            "Metro Quadrado (m²)": 1.0,
            "Quilômetro Quadrado (km²)": 1_000_000.0,
            "Hectare (ha)": 10_000.0,
        },
    },
    "Energia": {
        "base": "Joule (J)",
        "unidades": {
            "Joule (J)": 1,
            "Caloria Alimentar (kcal)": 4_184,
            "Quilowatt-hora (kWh)": 3_600_000,
        },
    },
    "Frequência": {
        "base": "Hertz (Hz)",
        "unidades": {
            "Hertz (Hz)": 1,
            "Quilo-hertz (kHz)": 1_000,
            "Mega-hertz (MHz)": 1_000_000,
            "Gigahertz (GHz)": 1_000_000_000,
        },
    },
    "Comprimento": {
        "base": "Metro (m)",
        "unidades": {
            "Milímetro (mm)": 0.001,
            "Centímetro (cm)": 0.01,
            "Metro (m)": 1.0,
            "Quilômetro (km)": 1_000.0,
            "Milha (mi)": 1609.34,
            "Pé (ft)": 0.3048,
            "Polegada (in)": 0.0254,
        },
    },
    "Contagem": {
        "base": "Unidade",
        "unidades": {
            "Unidade": 1,
            "Dezena": 10,
            "Centena": 100,
            "Milhar": 1_000,
            "Milhão": 1_000_000,
            "Bilhão": 1_000_000_000,
            "Trilhão": 1_000_000_000_000,
        },
    },
    "Dados": {
        "base": "Byte (B)",
        "unidades": {
            "Bit (b)": 0.125,
            "Byte (B)": 1.0,
            "Kilobyte (kB)": 1_024.0,
            "Megabyte (MB)": 1_048_576.0,
            "Gigabyte (GB)": 1_073_741_824.0,
            "Terabyte (TB)": 1_099_511_627_776.0,
        },
    },
    "Peso": {
        "base": "Quilograma (kg)",
        "unidades": {
            "Miligrama (mg)": 0.000001,
            "Grama (g)": 0.001,
            "Quilograma (kg)": 1.0,
            "Tonelada (t)": 1_000.0,
            "Libra (lb)": 0.453592,
        },
    },
    "Potência": {
        "base": "Watt (W)",
        "unidades": {
            "Watt (W)": 1.0,
            "Quilowatt (kW)": 1_000.0,
            "Cavalo-Vapor (hp)": 745.7,
        },
    },
    "Pressão": {
        "base": "Pascal (Pa)",
        "unidades": {
            "Atmosfera (atm)": 101_325.0,
            "Pascal (Pa)": 1.0,
            "Milímetro de Mercúrio (mmHg)": 133.3,
        },
    },
    "Velocidade": {
        "base": "Metro por Segundo (m/s)",
        "unidades": {
            "Centímetro por Segundo (cm/s)": 0.01,
            "Metro por Segundo (m/s)": 1.0,
            "Quilômetro por Hora (km/h)": 0.277778,
            "Milha por Hora (mph)": 0.44704,
            "Mach (Ma)": 340.3,  # Aproximação ao nível do mar a 15°C
        },
    },
    "Volume": {
        "base": "Litro (L)",
        "unidades": {
            "Mililitro (mL)": 0.001,
            "Litro (L)": 1.0,
            "Metro Cúbico (m³)": 1_000.0,
        },
    },
}


# Funções de conversão com fórmulas
def _convert_angle(value: float, from_unit: str, to_unit: str) -> float:
    """Conversão entre as três unidades de ângulo.

    Args:
        value (float): O valor de entrada.
        from_unit (str): O sistema de origem.
        to_unit (str): O sistema de destino.

    Returns:
        float: O valor de saída convertido.
    """
    if from_unit == to_unit:
        return value

    # Converte para a base (grau)
    degree = 0.0
    match from_unit:
        case "Grau":
            degree = value
        case "Radiano":
            degree = value * 180 / pi
        case "Grado":
            degree = value * 180 / 200

    # Converte da base para a unidade de saída
    match to_unit:
        case "Grau":
            return degree
        case "Radiano":
            return degree * pi / 180
        case "Grado":
            return degree * 200 / 180

    return 0.0


def _convert_number_system(value: str, from_base: str, to_base: str) -> str:
    """Conversão entre os sistemas numéricos.

    Args:
        value (str): O valor de entrada.
        from_base (str): O sistema de origem.
        to_base (str): O sistema de destino.

    Returns:
        str: O valor de saída convertido.
    """
    base_map = {"Binário": 2, "Octal": 8, "Decimal": 10, "Hexadecimal": 16}

    try:
        # Converte o valor de entrada para um inteiro decimal
        decimal_value = int(value, base_map[from_base])

        # Converte o valor decimal para a base de saída
        match to_base:
            case "Binário":
                return bin(decimal_value)[2:]
            case "Octal":
                return oct(decimal_value)[2:]
            case "Decimal":
                return str(decimal_value)
            case "Hexadecimal":
                return hex(decimal_value)[2:].upper()

    except (ValueError, TypeError):
        pass

    return "Erro"


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Conversão entre as três unidades de temperatura.

    Args:
        value (float): O valor de entrada.
        from_unit (str): A unidade de origem.
        to_unit (str): A unidade de destino.

    Returns:
        float: O valor de saída convertido.
    """
    if from_unit == to_unit:
        return value

    # Converte para a base (Celsius)
    celsius = 0.0
    match from_unit:
        case "Celsius":
            celsius = value
        case "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        case "Kelvin":
            celsius = value - 273.15

    # Converte da base para a unidade de saída
    match to_unit:
        case "Celsius":
            return celsius
        case "Fahrenheit":
            return (celsius * 9 / 5) + 32
        case "Kelvin":
            return celsius + 273.15

    return 0.0


def _convert_time(value: float, from_unit: str, to_unit: str) -> float:
    """Conversão entre várias unidades de tempo.

    Args:
        value (float): O valor de entrada.
        from_unit (str): A unidade de origem.
        to_unit (str): A unidade de destino.

    Returns:
        float: O valor de saída convertido.
    """
    if from_unit == to_unit:
        return value

    # Média de dias em 1 ano
    DAYS_IN_YEAR = 365.25

    # Fatores de conversão para a base (dias)
    to_days_factors = {
        "Milissegundo": 1 / (1000 * 60 * 60 * 24),
        "Segundo": 1 / (60 * 60 * 24),
        "Minuto": 1 / (60 * 24),
        "Hora": 1 / 24,
        "Dia": 1,
        "Semana": 7,
        "Mês": DAYS_IN_YEAR / 12,
        "Ano": DAYS_IN_YEAR,
        "Década": DAYS_IN_YEAR * 10,
        "Século": DAYS_IN_YEAR * 100,
        "Milênio": DAYS_IN_YEAR * 1000,
    }

    try:
        # Converte o valor de entrada para a base
        total_days = value * to_days_factors[from_unit]

        # Usa `timedelta` para conversões precisas quando possível
        td = timedelta(days=total_days)

        # Converte da base (dias) para a unidade de destino
        return td.total_seconds() / (to_days_factors[to_unit] * 86400)

    except KeyError:
        return 0.0


# Cache para cotações de moeda a fim de evitar chamadas excessivas à API
# A cache é válida por 1 hora (60 minutos = 3600 segundos)
_currency_cache = {"rates": None, "timestamp": 0, "ttl": 3600}


def _fetch_currency_rates() -> dict | None:
    """Busca as cotações de moeda de uma API e as armazena em cache.

    Returns:
        dict|None: As cotações de moeda obtidas através da API.
    """
    now = time.time()

    # Verifica se a cache é recente e válido
    if _currency_cache["rates"] and (
        now - _currency_cache["timestamp"] < _currency_cache["ttl"]
    ):
        return _currency_cache["rates"]

    try:
        # API gratuita que não requer chave, com base em USD
        api_url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("result") == "success":
            # Adiciona a cotação do Bitcoin (BTC) manualmente, pois não vem na mesma API
            btc_response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
                timeout=5,
            )
            btc_response.raise_for_status()
            btc_data = btc_response.json()
            data["rates"]["BTC"] = 1 / btc_data["bitcoin"]["usd"]

            _currency_cache["rates"] = data["rates"]
            _currency_cache["timestamp"] = now

            return _currency_cache["rates"]

        return None

    except (requests.exceptions.RequestException, ValueError, KeyError):
        # Retorna a cache antiga se a API falhar, ou None se não houver cache
        return _currency_cache["rates"]


def _convert_currency(value: float, from_unit: str, to_unit: str) -> float:
    """Conversão entre moedas usando uma API externa com cache.

    Args:
        value (float): O valor de entrada.
        from_unit (str): A moeda de origem.
        to_unit (str): A moeda de destino.

    Returns:
        float: O valor de saída convertido.
    """
    if from_unit == to_unit:
        return value

    rates = _fetch_currency_rates()
    if not rates:
        return 0.0

    # Extrai o código da moeda
    from_code = from_unit.split("(")[-1].strip(")")
    to_code = to_unit.split("(")[-1].strip(")")

    try:
        # Converte o valor de entrada para USD
        rate_from = rates[from_code]
        value_in_usd = value / rate_from

        # Converte de USD para a moeda de destino
        return value_in_usd * rates[to_code]

    except KeyError:
        return 0.0


# Fatores de lógica específica
CONVERSION_LOGIC = {
    "Ângulo": _convert_angle,
    "Moeda": _convert_currency,
    "Numeração": _convert_number_system,
    "Temperatura": _convert_temperature,
    "Tempo": _convert_time,
}


def convert(category: str, from_unit: str, to_unit: str, value: float) -> str:
    """Função central para conversão de medidas com base na categoria selecionada.

    Args:
        category (str): A categoria de conversão.
        from_unit (str): A unidade de origem.
        to_unit (str): A unidade de destino.
        value (float): O valor de entrada.

    Returns:
        str: O valor de saída convertido.
    """
    try:
        result = None

        # Se a categoria possuir uma função de lógica específica...
        if category in CONVERSION_LOGIC:
            # Categorias que exigem cálculo específico usam funções dedicadas
            val = str(int(value)) if category == "Numeração" else value
            result = CONVERSION_LOGIC[category](val, from_unit, to_unit)

        # Se a categoria usa fatores de conversão simples, aplica a fórmula de base
        elif category in CONVERSION_FACTORS:
            factors = CONVERSION_FACTORS[category]["unidades"]
            value_in_base = value * factors[from_unit]
            result = value_in_base / factors[to_unit]

        # Porém, caso a categoria não tenha sido encontrada...
        else:
            return "N/A"

        # A categoria `Numeração` retorna uma string e não deve ser formatada
        if category == "Numeração":
            return str(result)

        # Formata o resultado numérico para o padrão brasileiro
        if result == 0:
            return "0"
        formatted_str = f"{result:.10f}".rstrip("0").replace(".", ",")

        if "," in formatted_str:
            integer_part, decimal_part = formatted_str.split(",")
            formatted_integer = f"{int(integer_part):,}".replace(",", ".")
            return (
                f"{formatted_integer},{decimal_part}"
                if decimal_part
                else formatted_integer
            )

        return f"{int(formatted_str):,}".replace(",", ".")

    except (ValueError, KeyError, ZeroDivisionError):
        return "Erro"
