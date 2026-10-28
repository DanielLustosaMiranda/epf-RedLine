from bottle import route, request
from services import dashboard_service
from utils.auth_decorator import login_required, get_session
from utils.view_helper import render_page


@route('/dashboard')
@login_required
def show_dashboard():
    session = get_session()
    user_id = session.get('user_id')
    dados = dashboard_service.obter_dados_dashboard(user_id)
    return render_page('dashboard', **dados)


@route('/relatorios')
@login_required
def show_relatorios():
    session = get_session()
    user_id = session.get('user_id')
    car_filter = request.query.get('car_id', '').strip()
    dados = dashboard_service.obter_dados_dashboard(user_id)

    selected_car = None
    if car_filter.isdigit():
        c_id = int(car_filter)
        selected_car = next((c for c in dados['cars'] if c['id'] == c_id), None)

    return render_page(
        'relatorios',
        **dados,
        selected_car=selected_car,
        car_filter=int(car_filter) if car_filter.isdigit() else None,
    )
