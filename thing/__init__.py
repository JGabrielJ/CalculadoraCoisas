"""Contém as variáveis e funções necessárias para a execução da Calculadora de Coisas."""

import os   # Arquivos do App
BONK_FILE = os.path.abspath('./files/bonk.mp3')
ICON_FILE = os.path.abspath('./files/icon.ico')

# Opções do Menu de Conversão
CONVERSION_OPTIONS = {
    'Ângulo': ('Grau', 'Radiano', 'Gradiano'),
    'Área': ('Centímetro Quadrado (cm²)', 'Metro Quadrado (m²)', 'Quilômetro Quadrado (km²)', 'Hectare (ha)'),
    'Comprimento': ('Milímetro (mm)', 'Centímetro (cm)', 'Metro (m)', 'Quilômetro (km)', 'Milha (mi)', 'Polegada (in)'), # OK
    'Contagem': ('Unidade', 'Dezena', 'Centena', 'Milhar', 'Milhão', 'Bilhão', 'Trilhão'), # OK
    'Dados': ('Bit (b)', 'Byte (B)', 'Kilobyte (kB)', 'Megabyte (MB)', 'Gigabyte (GB)', 'Terabyte (TB)'),
    'Energia': ('Joule (J)', 'Caloria (cal)', 'Quilocaloria (kcal)', 'Quilowatt-hora (kWh)'),
    'Frequência': ('Hertz (Hz)', 'Quilo-hertz (kHz)', 'Mega-hertz (MHz)', 'Gigahertz (GHz)'),
    'Moeda': ('Real (BRL)', 'Dólar (USD)', 'Euro (EUR)', 'Bitcoin (BTC)'),
    'Numeração': ('Binário', 'Octal', 'Decimal', 'Hexadecimal'), # OK
    'Peso': ('Miligrama (mg)', 'Grama (g)', 'Quilograma (kg)', 'Tonelada (t)', 'Libra (lb)'), # OK
    'Potência': ('Watt (W)', 'Quilowatt (kW)', 'Cavalo-Vapor (hp)'),
    'Pressão': ('Atmosfera (atm)', 'Milímetro de Mercúrio (mmHg)', 'Pascal (Pa)'),
    'Temperatura': ('Celsius', 'Fahrenheit', 'Kelvin'), # OK
    'Tempo': ('Milissegundo', 'Segundo', 'Minuto', 'Hora', 'Dia', 'Semana', 'Mês', 'Ano', 'Década', 'Século', 'Milênio', 'Era'),
    'Velocidade': ('Centímetro por Segundo (cm/s)', 'Metro por Segundo (m/s)', 'Quilômetro por Hora (km/h)', 'Milha por Hora (mph)', 'Mach (Ma)'),
    'Volume': ('Mililitro (mL)', 'Centímetro cúbico (cm³)', 'Litro (L)', 'Metro Cúbico (m³)'),
}

# Fatores de Conversão
CONVERSION_FACTORS = {
    'Comprimento': {
        'base': 'Metro (m)',
        'unidades': {
            'Milímetro (mm)': 0.001, 'Centímetro (cm)': 0.01, 'Metro (m)': 1.0,
            'Quilômetro (km)': 1000.0, 'Milha (mi)': 1609.34, 'Polegada (in)': 0.0254,
        }
    },
    'Contagem': {
        'base': 'Unidade',
        'unidades': {
            'Unidade': 1, 'Dezena': 10, 'Centena': 100, 'Milhar': 1000,
            'Milhão': 1_000_000, 'Bilhão': 1_000_000_000, 'Trilhão': 1_000_000_000_000,
        }
    },
    'Peso': {
        'base': 'Grama (g)',
        'unidades': {
            'Miligrama (mg)': 0.001, 'Grama (g)': 1.0, 'Quilograma (kg)': 1000.0,
            'Tonelada (t)': 1_000_000.0, 'Libra (lb)': 453.592,
        }
    },
    # TODO: Adicionar outras categorias com fatores simples aqui!!!
}

# Funções de Conversão Especial
def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Conversão entre as três unidades de temperatura.

    Args:
        value (float): O valor de entrada.
        from_unit (str): A unidade de origem.
        to_unit (str): A unidade de destino.

    Returns:
        float: O valor de saída convertido.
    """
    if from_unit == to_unit: return value

    # Converte para a base (Celsius)
    celsius = 0.0
    match from_unit:
        case 'Celsius': celsius = value
        case 'Fahrenheit': celsius = (value - 32) * 5 / 9
        case 'Kelvin': celsius = value - 273.15

    # Converte da base para a unidade de saída
    match to_unit:
        case 'Celsius': return celsius
        case 'Fahrenheit': return (celsius * 9 / 5) + 32
        case 'Kelvin': return celsius + 273.15

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
    base_map = {'Binário': 2, 'Octal': 8, 'Decimal': 10, 'Hexadecimal': 16}

    try:
        # Converte o valor de entrada para um inteiro decimal
        decimal_value = int(value, base_map[from_base])

        # Converte o valor decimal para a base de saída
        match to_base:
            case 'Binário': return bin(decimal_value)[2:]
            case 'Octal': return oct(decimal_value)[2:]
            case 'Decimal': return str(decimal_value)
            case 'Hexadecimal': return hex(decimal_value)[2:].upper()

    except (ValueError, TypeError):
        pass

    return "Error"

# Fatores de Lógica Específica
CONVERSION_LOGIC = {
    'Temperatura': _convert_temperature,
    'Numeração': _convert_number_system,
    # TODO: Adicionar outras lógicas especiais aqui!!!
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
        # Se a categoria possuir uma função de lógica específica
        if category in CONVERSION_LOGIC:
            val = str(int(value)) if category == 'Numeração' else value
            result = CONVERSION_LOGIC[category](val, from_unit, to_unit)
            return str(result)

        # Se não, utiliza o sistema de fatores de conversão
        elif category in CONVERSION_FACTORS:
            factors = CONVERSION_FACTORS[category]['unidades']
            value_in_base = value * factors[from_unit]
            result = value_in_base / factors[to_unit]
            return f"{result:.4f}".rstrip('0').rstrip('.')

    except (ValueError, KeyError, ZeroDivisionError):
        return "Error"
    
    return "N/A" # Se a categoria não for encontrada
