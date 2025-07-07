%rebase('layout', title='Login')

<section class="form-section">
    <h1 class="section-title">Login</h1>

    <form action="/login" method="post" class="styled-form">
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" required>
        </div>

        % if error:
            <div class="alert alert-danger">
                {{error}}
            </div>
        % end

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Entrar</button>
        </div>
    </form>

    <div class="sub-link">
        <p>Não tem uma conta? <a href="/signup">Cadastre-se</a></p>
    </div>
</section>