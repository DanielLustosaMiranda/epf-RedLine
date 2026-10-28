% rebase('layout', title='Meu Perfil')

<div class="form-page-container">
    <div class="form-card">
        <div class="form-card-header">
            <h1><i class="fas fa-user-gear"></i> Meu Perfil</h1>
            <p>Atualize seus dados cadastrais ou altere sua senha de acesso.</p>
        </div>

        % if defined('error') and error:
        <div class="alert alert-danger">
            <i class="fas fa-circle-exclamation"></i> {{error}}
        </div>
        % end

        <form action="/perfil" method="post" class="styled-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="name">Nome Completo *</label>
                    <input type="text" id="name" name="name" value="{{user.get('name', '') if user else ''}}" required>
                </div>
                <div class="form-group">
                    <label for="email">E-mail *</label>
                    <input type="email" id="email" name="email" value="{{user.get('email', '') if user else ''}}" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="birthdate">Data de Nascimento *</label>
                    <input type="date" id="birthdate" name="birthdate" value="{{user.get('birthdate', '') if user else ''}}" required>
                </div>
                <div class="form-group">
                    <label for="telefone">Telefone / WhatsApp</label>
                    <input type="text" id="telefone" name="telefone" value="{{user.get('telefone', '') if user else ''}}" placeholder="(61) 99999-9999">
                </div>
            </div>

            <hr class="form-divider">
            <h3 class="subsection-title"><i class="fas fa-key"></i> Alterar Senha (Opcional)</h3>
            <p class="text-muted" style="margin-bottom: 12px;">Deixe em branco caso deseje manter sua senha atual.</p>

            <div class="form-row">
                <div class="form-group">
                    <label for="new_password">Nova Senha</label>
                    <input type="password" id="new_password" name="new_password" placeholder="Nova senha">
                </div>
                <div class="form-group">
                    <label for="confirm_password">Confirmar Nova Senha</label>
                    <input type="password" id="confirm_password" name="confirm_password" placeholder="Repita a nova senha">
                </div>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-floppy-disk"></i> Salvar Alterações
                </button>
                <a href="/dashboard" class="btn btn-secondary">Voltar ao Painel</a>
            </div>
        </form>
    </div>
</div>
