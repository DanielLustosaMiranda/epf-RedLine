from bottle import template, request

def render_template(template_name, **kwargs):

    session = request.environ.get('beaker.session')
    
    # Adiciona os dados do usuário (se existirem) a todas as chamadas de template
    if session.get('user_id'):
        kwargs['user_id'] = session.get('user_id')
        kwargs['user_name'] = session.get('user_name')
    
    return template(template_name, **kwargs)