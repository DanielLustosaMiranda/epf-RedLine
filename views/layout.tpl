<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
<<<<<<< HEAD
    <title>Sistema Bottle - {{title or 'Sistema'}}</title>
    <link rel="shortcut icon" href="/static/img/BottleLogo.png" type="image/x-icon">
=======
    <title>RedLine - {{title or 'Sistema'}}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
>>>>>>> 2504fd3f1467c4aa5802960b897f04f3803e05bf
    <link rel="stylesheet" href="/static/css/style.css" />
    <link rel="stylesheet" href="/static/css/dashboard.css">
</head>
<body>

    <header class="main-header">
        <div class="container header-container">
            <a href="/" class="logo">Home</a>
            % if defined('user_id'):
                <div class="user-info">
                    <span>Olá, {{user_name}}</span>
                    <a href="/logout" class="btn btn-secondary btn-sm">Sair</a>
                </div>
            % end
        </div>
    </header>

    <main class="container">
        {{!base}}
    </main>
    
    <footer>
        <p>&copy; 2025, RedLine. Todos os direitos reservados.</p>
    </footer>

    <script src="/static/js/main.js"></script>
</body>
</html>