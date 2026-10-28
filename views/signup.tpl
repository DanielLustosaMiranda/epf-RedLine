% rebase('layout', title='Criar Conta')

<div class="auth-wrapper">
    <div class="auth-card">
        <div class="auth-header">
            <div class="auth-badge"><i class="fas fa-user-plus"></i></div>
            <h1>Crie sua Conta</h1>
            <p>Comece a monitorar a saúde e as revisões dos seus veículos.</p>
        </div>

        % if defined('error') and error:
        <div class="alert alert-danger">
            <i class="fas fa-circle-exclamation"></i> {{error}}
        </div>
        % end

        <form action="/signup" method="post" class="styled-form">
            <div class="form-group">
                <label for="name"><i class="fas fa-user"></i> Nome Completo *</label>
                <input type="text" id="name" name="name" placeholder="Ex: João da Silva" required>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="email"><i class="fas fa-envelope"></i> E-mail *</label>
                    <input type="email" id="email" name="email" placeholder="seu@email.com" required>
                </div>
                <div class="form-group">
                    <label for="telefone"><i class="fas fa-phone"></i> Telefone</label>
                    <input type="text" id="telefone" name="telefone" placeholder="(61) 99999-9999">
                </div>
            </div>

            <div class="form-group">
                <label for="birthdate"><i class="fas fa-calendar"></i> Data de Nascimento *</label>
                <input type="date" id="birthdate" name="birthdate" required>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="password"><i class="fas fa-lock"></i> Senha *</label>
                    <input type="password" id="password" name="password" placeholder="Mínimo 4 caracteres" required>
                </div>
                <div class="form-group">
                    <label for="confirm_password"><i class="fas fa-check-double"></i> Confirmar Senha *</label>
                    <input type="password" id="confirm_password" name="confirm_password" placeholder="Repita a senha" required>
                </div>
            </div>

            <button type="submit" class="btn btn-primary btn-block">
                <i class="fas fa-check"></i> Finalizar Cadastro
            </button>
        </form>

        <div class="auth-footer">
            Já possui uma conta? <a href="/login">Fazer Login</a>
        </div>
    </div>
</div>
