<!DOCTYPE html>
<html>
<head><title>Cadastro</title></head>
<body>
    <h2>Cadastro</h2>
    % if error:
        <p style="color:red;">{{error}}</p>
    % end
    <form method="POST" action="/signup">
        <input type="text" name="user" placeholder="Usuário"><br>
        <input type="password" name="pass" placeholder="Senha"><br>
        <input type="submit" value="Cadastrar">
    </form>
</body>
</html>