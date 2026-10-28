from datetime import datetime
from bottle import template, request
from utils.auth_decorator import get_session, pop_flash


def format_brl(value) -> str:
    """Formata um valor numérico como moeda brasileira (R$ 1.234,56)."""
    try:
        val = float(value or 0)
        formatted = f"{val:,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"
    except (ValueError, TypeError):
        return "R$ 0,00"


def format_km(value) -> str:
    """Formata quilometragem com separador de milhar (ex: 87.000 km)."""
    try:
        val = int(float(value or 0))
        return f"{val:,}".replace(",", ".") + " km"
    except (ValueError, TypeError):
        return "0 km"


def format_date_br(date_str: str) -> str:
    """Converte data YYYY-MM-DD para DD/MM/YYYY."""
    if not date_str:
        return "-"
    try:
        dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return str(date_str)


def render_page(template_name: str, **kwargs):
    """Renderiza um template injetando automaticamente dados da sessão, alertas e formatadores."""
    session = get_session()
    if session and session.get('user_id'):
        kwargs.setdefault('user_id', session.get('user_id'))
        kwargs.setdefault('user_name', session.get('user_name', 'Motorista'))
        kwargs.setdefault('user_email', session.get('user_email', ''))

    kwargs.setdefault('flash', pop_flash())
    kwargs.setdefault('current_path', request.path)
    kwargs.setdefault('format_brl', format_brl)
    kwargs.setdefault('format_km', format_km)
    kwargs.setdefault('format_date_br', format_date_br)
    return template(template_name, **kwargs)
