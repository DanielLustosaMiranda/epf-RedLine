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