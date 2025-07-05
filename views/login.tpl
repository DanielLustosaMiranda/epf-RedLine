<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    % if error:
        <p style="color:red;">{{error}}</p>
    % end
    <form method="POST" action="/login">
        <input type="text" name="user" placeholder="Usuário"><br>
        <input type="password" name="pass" placeholder="Senha"><br>
        <input type="submit" value="Entrar">
    </form>
</body>
</html>