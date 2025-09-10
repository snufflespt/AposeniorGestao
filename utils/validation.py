"""Validation Utilities for Streamlit Application

This module provides comprehensive validation functions and utilities
for consistent data validation across all sections of the application.
"""

import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional


# ===== CONSTANTES DE VALIDAÇÃO =====

GRAU_ESCOLARIDADE_OPCOES = [
    "Sem Escolaridade",
    "1º Ciclo (4ª classe)",
    "2º Ciclo (6º ano)",
    "3º Ciclo (9º ano)",
    "Ensino Secundário (12º ano)",
    "Licenciatura",
    "Mestrado",
    "Doutoramento",
    "Outro"
]

SITUACAO_PROFISSIONAL_OPCOES = [
    "Ativo",
    "Desempregado",
    "Estudante",
    "Reformado",
    "Doméstico/a",
    "Outra"
]

SALA_OPCOES = [
    "Sala 1",
    "Sala 2",
    "Sala 3",
    "Sala de Artes",
    "Sala Exterior",
    "Outro"
]

DIAS_SEMANA = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo"
]

NIVEL_OPCOES = [
    "Inicial",
    "Intermédio-Inicial",
    "Intermédio",
    "Intermédio-Avançado",
    "Avançado",
    "Outro"
]

ESTADO_OPCOES = [
    "Ativa",
    "Inativa"
]


# ===== FUNÇÕES DE VALIDAÇÃO ESPECÍFICAS =====

def is_valid_phone(phone: str) -> bool:
    """Verifica se um número de telefone é válido (9 dígitos).

    Args:
        phone (str): Número de telefone a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    if not phone:
        return True  # Campo opcional, válido se vazio
    cleaned_phone = phone.replace(" ", "")
    return cleaned_phone.isdigit() and len(cleaned_phone) == 9


def is_valid_nif(nif: str) -> bool:
    """Verifica se o NIF tem 9 dígitos.

    Args:
        nif (str): NIF a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    if not nif:
        return True  # Pode ser opcional
    return str(nif).strip().isdigit() and len(str(nif).strip()) == 9


def is_valid_postal_code(pc: str) -> bool:
    """Verifica se o código postal está no formato XXXX-XXX.

    Args:
        pc (str): Código postal a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    if not pc:
        return True  # Pode ser opcional
    return bool(re.match(r'^\d{4}-\d{3}$', pc.strip()))


def is_valid_email(email: str) -> bool:
    """Verifica se o formato do email é válido.

    Args:
        email (str): Email a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    if not email:
        return True  # Campo opcional, válido se vazio
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()))


def is_valid_date(date_obj: Any, min_date: Optional[date] = None, max_date: Optional[date] = None) -> bool:
    """Verifica se uma data é válida dentro de limites opcionais.

    Args:
        date_obj: Objeto de data a validar
        min_date: Data mínima permitida (opcional)
        max_date: Data máxima permitida (opcional)

    Returns:
        bool: True se válido, False caso contrário
    """
    if not date_obj:
        return False

    if not isinstance(date_obj, date):
        return False

    if min_date and date_obj < min_date:
        return False

    if max_date and date_obj > max_date:
        return False

    return True


def is_valid_time(time_obj: Any) -> bool:
    """Verifica se um objeto tempo é válido.

    Args:
        time_obj: Objeto tempo a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    if not time_obj:
        return False

    try:
        # Verificar se é um objeto time válido
        if hasattr(time_obj, 'hour') and hasattr(time_obj, 'minute'):
            return 0 <= time_obj.hour <= 23 and 0 <= time_obj.minute <= 59
        return False
    except Exception:
        return False


def check_time_overlap(start1: Any, end1: Any, start2: Any, end2: Any) -> bool:
    """Verifica se dois intervalos de tempo se sobrepõem.

    Args:
        start1: Hora de início do primeiro intervalo
        end1: Hora de fim do primeiro intervalo
        start2: Hora de início do segundo intervalo
        end2: Hora de fim do segundo intervalo

    Returns:
        bool: True se há sobreposição, False caso contrário
    """
    try:
        # Converter para minutos para facilitar comparação
        def to_minutes(t):
            if hasattr(t, 'hour') and hasattr(t, 'minute'):
                return t.hour * 60 + t.minute
            return 0

        s1 = to_minutes(start1)
        e1 = to_minutes(end1)
        s2 = to_minutes(start2)
        e2 = to_minutes(end2)

        # Verificar sobreposição
        return s1 < e2 and s2 < e1
    except Exception:
        return False


def normalize_string(s: str) -> str:
    """Normaliza uma string para comparação, removendo acentos e convertendo para minúsculas.

    Args:
        s (str): String a normalizar

    Returns:
        str: String normalizada
    """
    if not s or not isinstance(s, str):
        return ""

    import unicodedata
    s = unicodedata.normalize('NFD', s.lower())
    s = s.encode('ascii', 'ignore').decode('utf-8')
    return s


def parse_date(date_str: str) -> Optional[date]:
    """Converte uma string de data (DD/MM/YYYY) para um objeto date.

    Args:
        date_str (str): String de data no formato DD/MM/YYYY

    Returns:
        date: Objeto date ou None se inválido
    """
    if not date_str or not isinstance(date_str, str):
        return None

    try:
        return datetime.strptime(date_str.strip(), '%d/%m/%Y').date()
    except ValueError:
        return None


def format_date_for_display(date_obj: Any) -> str:
    """Formata um objeto de data para exibição.

    Args:
        date_obj: Objeto de data a formatar

    Returns:
        str: Data formatada ou string vazia se inválida
    """
    if not date_obj:
        return ""

    if isinstance(date_obj, str):
        parsed = parse_date(date_obj)
        return parsed.strftime('%d/%m/%Y') if parsed else date_obj

    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime('%d/%m/%Y')

    return str(date_obj)


def format_time_for_display(time_obj: Any) -> str:
    """Formata um objeto tempo para exibição.

    Args:
        time_obj: Objeto tempo a formatar

    Returns:
        str: Tempo formatado ou string vazia se inválido
    """
    if not time_obj:
        return ""

    if hasattr(time_obj, 'strftime'):
        return time_obj.strftime('%H:%M')

    return str(time_obj)


def validate_range(value: float, min_val: Optional[float] = None, max_val: Optional[float] = None) -> bool:
    """Verifica se um valor numérico está dentro de um intervalo.

    Args:
        value (float): Valor a validar
        min_val: Valor mínimo permitido (opcional)
        max_val: Valor máximo permitido (opcional)

    Returns:
        bool: True se válido, False caso contrário
    """
    if min_val is not None and value < min_val:
        return False

    if max_val is not None and value > max_val:
        return False

    return True


# ===== VALIDAÇÃO COMPREENSIVA =====

def compile_validation_errors(validation_results: Dict[str, Any]) -> List[str]:
    """Compila todos os erros de validação em uma lista de mensagens.

    Args:
        validation_results (Dict[str, Any]): Resultados de várias validações

    Returns:
        List[str]: Lista de mensagens de erro
    """
    errors = []

    for field, result in validation_results.items():
        if isinstance(result, bool) and not result:
            errors.append(f"Campo '{field}' tem valor inválido")

        elif isinstance(result, tuple) and len(result) == 2:
            is_valid, message = result
            if not is_valid and message:
                errors.append(message)

        elif isinstance(result, list):
            errors.extend([err for err in result if err])

        elif isinstance(result, str) and result:
            errors.append(f"{field}: {result}")

    return errors


def validate_form_data(form_data: Dict[str, Any], validation_rules: Dict[str, Any]) -> List[str]:
    """Valida dados de formulário contra regras específicas.

    Args:
        form_data (Dict[str, Any]): Dados do formulário
        validation_rules (Dict[str, Any]): Regras de validação

    Returns:
        List[str]: Lista de mensagens de erro
    """
    errors = []

    for field, rules in validation_rules.items():
        if field not in form_data and rules.get('required'):
            errors.append(f"Campo '{rules.get('label', field)}' é obrigatório")
            continue

        value = form_data.get(field)
        if value is None or (isinstance(value, (str, list)) and len(str(value)) == 0):
            if rules.get('required'):
                errors.append(f"Campo '{rules.get('label', field)}' é obrigatório")
            continue

        # Validações específicas por tipo
        field_type = rules.get('type', 'text')

        if field_type == 'phone':
            if not is_valid_phone(value):
                field_name = rules.get('label', field)
                errors.append(f"'{field_name}' deve ter 9 dígitos")

        elif field_type == 'email':
            if not is_valid_email(value):
                field_name = rules.get('label', field)
                errors.append(f"'{field_name}' tem formato inválido")

        elif field_type == 'nif':
            if not is_valid_nif(value):
                field_name = rules.get('label', field)
                errors.append(f"'{field_name}' deve ter 9 dígitos")

        elif field_type == 'postal_code':
            if not is_valid_postal_code(value):
                field_name = rules.get('label', field)
                errors.append(f"'{field_name}' deve estar no formato XXXX-XXX")

        elif field_type == 'numeric':
            try:
                num_value = float(value)
                min_val = rules.get('min_value')
                max_val = rules.get('max_value')

                if min_val is not None and num_value < min_val:
                    errors.append(f"'{rules.get('label', field)}' deve ser pelo menos {min_val}")
                elif max_val is not None and num_value > max_val:
                    errors.append(f"'{rules.get('label', field)}' não pode ser maior que {max_val}")
            except (ValueError, TypeError):
                errors.append(f"'{rules.get('label', field)}' deve ser um número válido")

    return errors


# ===== FUNÇÕES DE FORMATAÇÃO =====

def format_display_name(name: str, max_length: int = 50) -> str:
    """Formata um nome para exibição com limite de caracteres.

    Args:
        name (str): Nome a formatar
        max_length (int): Comprimento máximo (padrão: 50)

    Returns:
        str: Nome formatado
    """
    if not name:
        return "N/A"

    if len(name) > max_length:
        return f"{name[:max_length-3]}..."

    return name


def format_status_badge(status: str, active_value: str = "Ativo") -> str:
    """Formata um status como badge HTML.

    Args:
        status (str): Status a formatar
        active_value (str): Valor que indica status ativo

    Returns:
        str: HTML do badge
    """
    if not status:
        return '<span style="background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">● DESCONHECIDO</span>'

    is_active = normalize_string(status).startswith(normalize_string(active_value))

    if is_active:
        color = "#28a745"  # Verde
        bg_color = "#d4edda"
        text_color = "#155724"
    else:
        color = "#dc3545"  # Vermelho
        bg_color = "#f8d7da"
        text_color = "#721c24"

    status_text = status.upper()

    return f'<span style="background-color: {bg_color}; color: {text_color}; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">● {status_text}</span>'


def format_currency(value: Any, currency: str = "€") -> str:
    """Formata um valor como moeda.

    Args:
        value: Valor a formatar
        currency (str): Símbolo da moeda

    Returns:
        str: Valor formatado como moeda
    """
    try:
        if isinstance(value, str) and not value.strip():
            return f"0{currency}"

        num_value = float(value)
        return f"{num_value:.2f}{currency}"
    except (ValueError, TypeError):
        return f"0{currency}"
