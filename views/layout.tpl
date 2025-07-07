<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RedLine - {{title or 'Sistema'}}</title>
    <link rel="shortcut icon" href="/static/img/BottleLogo.png" type="image/x-icon">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
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
    
    <footer class="container_footer">
        <p>&copy; 2025, RedLine. Todos os direitos reservados.</p>
    </footer>

    <script src="/static/js/main.js"></script>
</body>
</html>