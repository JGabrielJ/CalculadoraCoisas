from __future__ import annotations


def format_number(number_str: str) -> str:
    """Formata um número em string para o padrão brasileiro.

    Args:
        number_str (str): Número em formato Python (ponto decimal) ou em notação científica.

    Returns:
        str: Número formatado com separadores de milhar e vírgula decimal.
    """
    if number_str in ("Erro", "N/A", "∞"):
        return number_str

    # Mantém a notação científica como está, apenas troca o ponto decimal
    if "e" in number_str.lower():
        return number_str.replace(".", ",")

    is_negative = number_str.startswith("-")
    if is_negative:
        number_str = number_str[1:]

    if not number_str:
        number_str = "0"

    parts = number_str.split(".")
    integer_part = parts[0] or "0"
    decimal_part = parts[1] if len(parts) > 1 else None

    try:
        integer_part_formatted = f"{int(integer_part):,}".replace(",", ".")
    except ValueError:
        integer_part_formatted = integer_part

    if decimal_part is not None:
        formatted = f"{integer_part_formatted},{decimal_part}"
    else:
        formatted = integer_part_formatted

    return f"-{formatted}" if is_negative else formatted


def unformat_number(formatted_str: str) -> str:
    """Converte uma string formatada no padrão brasileiro para o padrão Python.

    Args:
        formatted_str (str): Valor no formato brasileiro.

    Returns:
        str: Valor no formato Python com ponto decimal.
    """
    if "e" in formatted_str.lower():
        return formatted_str.replace(",", ".")

    # Remove separadores de milhar e converte vírgula decimal para ponto
    return formatted_str.replace(".", "").replace(",", ".")
