% rebase('layout', title='Login')

<div class="auth-wrapper">
    <div class="auth-card">
        <div class="auth-header">
            <div class="auth-badge"><i class="fas fa-car-burst"></i></div>
            <h1>Bem-vindo ao Red<span>Line</span></h1>
            <p>Controle revisões, peças, abastecimentos e custos da sua garagem em um só lugar.</p>
        </div>

        % if defined('error') and error:
        <div class="alert alert-danger">
            <i class="fas fa-circle-exclamation"></i> {{error}}
        </div>
        % end

        <form action="/login" method="post" class="styled-form">
            <div class="form-group">
                <label for="email"><i class="fas fa-envelope"></i> E-mail</label>
                <input type="email" id="email" name="email" placeholder="seu@email.com" required autofocus>
            </div>

            <div class="form-group">
                <label for="password"><i class="fas fa-lock"></i> Senha</label>
                <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
            </div>

            <button type="submit" class="btn btn-primary btn-block">
                <i class="fas fa-right-to-bracket"></i> Entrar na Garagem
            </button>
        </form>

        <div class="demo-access-box">
            <p class="demo-title"><i class="fas fa-bolt"></i> Quer testar agora mesmo?</p>
            <p class="demo-desc">Acesse uma garagem pré-configurada com veículos, histórico, agendamentos e peças monitoradas:</p>
            <form action="/login/demo" method="post">
                <button type="submit" class="btn btn-secondary btn-block">
                    <i class="fas fa-rocket"></i> Entrar com Conta Demonstração (1 Clique)
                </button>
            </form>
            <small class="demo-credentials">Credenciais demo: <code>demo@redline.com</code> / senha: <code>123456</code></small>
        </div>

        <div class="auth-footer">
            Não tem uma conta? <a href="/signup">Cadastre-se gratuitamente</a>
        </div>
    </div>
</div>
