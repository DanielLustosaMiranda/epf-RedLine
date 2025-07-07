<<<<<<< HEAD
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="/signup" method="post">
    <input type="text" name="name" placeholder="Nome completo" required>
    <input type="email" name="email" placeholder="E-mail" required>
    <input type="date" name="birthdate" required>
    <input type="text" name="username" placeholder="Usuário" required>
    <input type="password" name="password" placeholder="Senha" required>
    <button type="submit">Cadastrar</button>
</form>
</body>
</html>
=======
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
>>>>>>> 2504fd3f1467c4aa5802960b897f04f3803e05bf
