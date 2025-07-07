
%rebase('layout', title='Cadastro')

<section class="form-section">
    <h1 class="section-title">Crie sua Conta</h1>

    <form action="/signup" method="post" class="styled-form">
        <div class="form-group">
            <label for="name">Nome Completo:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="birthdate">Data de Nascimento:</label>
            <input type="date" id="birthdate" name="birthdate" required>
        </div>
        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div class="form-group">
            <label for="confirm_password">Confirme a Senha:</label>
            <input type="password" id="confirm_password" name="confirm_password" required>
        </div>

        % if error:
            <div class="alert alert-danger">{{error}}</div>
        % end

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Cadastrar</button>
        </div>
    </form>
</section>
