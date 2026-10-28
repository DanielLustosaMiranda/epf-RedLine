<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RedLine | {{title if defined('title') and title else 'Gestão Automotiva'}}</title>
    <link rel="shortcut icon" href="/static/img/BottleLogo.png" type="image/png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body>

    <header class="main-header no-print">
        <div class="header-container">
            <a href="/" class="brand-logo">
                <span class="brand-icon"><i class="fas fa-gauge-high"></i></span>
                <div class="brand-text">
                    <span class="brand-name">Red<span>Line</span></span>
                    <span class="brand-subtitle">Gestão Automotiva</span>
                </div>
            </a>

            % if defined('user_id') and user_id:
            <nav class="main-nav">
                <a href="/dashboard" class="nav-link {{'active' if defined('current_path') and current_path == '/dashboard' else ''}}">
                    <i class="fas fa-chart-pie"></i> Painel
                </a>
                <a href="/carros" class="nav-link {{'active' if defined('current_path') and current_path.startswith('/carros') else ''}}">
                    <i class="fas fa-car-side"></i> Minha Garagem
                </a>
                <a href="/manutencoes" class="nav-link {{'active' if defined('current_path') and current_path.startswith('/manutencoes') else ''}}">
                    <i class="fas fa-screwdriver-wrench"></i> Manutenções
                </a>
                <a href="/relatorios" class="nav-link {{'active' if defined('current_path') and current_path.startswith('/relatorios') else ''}}">
                    <i class="fas fa-file-invoice-dollar"></i> Relatórios
                </a>
            </nav>

            <div class="user-menu">
                <a href="/perfil" class="user-profile-chip {{'active' if defined('current_path') and current_path == '/perfil' else ''}}" title="Editar meu perfil">
                    <i class="fas fa-user-circle"></i>
                    <span>{{user_name}}</span>
                </a>
                <a href="/logout" class="btn btn-outline-light btn-sm" title="Sair do sistema">
                    <i class="fas fa-right-from-bracket"></i> Sair
                </a>
            </div>
            % else:
            <div class="user-menu">
                <a href="/login" class="btn btn-outline-light btn-sm">Entrar</a>
                <a href="/signup" class="btn btn-primary btn-sm">Criar Conta</a>
            </div>
            % end
        </div>
    </header>

    <main class="main-wrapper">
        % if defined('flash') and flash:
        <div class="flash-banner flash-{{flash.get('category', 'info')}} no-print" id="flash-banner">
            <div class="flash-content">
                % if flash.get('category') == 'danger':
                    <i class="fas fa-circle-exclamation"></i>
                % elif flash.get('category') == 'warning':
                    <i class="fas fa-triangle-exclamation"></i>
                % else:
                    <i class="fas fa-circle-check"></i>
                % end
                <span>{{flash.get('text')}}</span>
            </div>
            <button type="button" class="flash-close" onclick="this.parentElement.remove()">&times;</button>
        </div>
        % end

        {{!base}}
    </main>

    <footer class="main-footer no-print">
        <div class="footer-container">
            <p><strong>RedLine</strong> &mdash; Sistema Completo de Manutenção, Vida Útil de Peças e Controle Veicular</p>
            <p class="footer-meta">POO em Python &bull; Arquitetura MVC &bull; Persistência JSON</p>
        </div>
    </footer>

    <script src="/static/js/main.js"></script>
</body>
</html>
