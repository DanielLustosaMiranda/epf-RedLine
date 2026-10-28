% rebase('layout', title='Painel Principal')

<div class="page-header">
    <div>
        <h1 class="page-title"><i class="fas fa-gauge-high"></i> Painel de Controle</h1>
        <p class="page-subtitle">Visão geral da saúde da sua frota, alertas de revisão e resumo financeiro.</p>
    </div>
    <div class="header-actions">
        <a href="/carros/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Novo Veículo
        </a>
        <a href="/relatorios" class="btn btn-secondary">
            <i class="fas fa-chart-column"></i> Ver Relatórios
        </a>
    </div>
</div>

<!-- KPI Cards -->
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon kpi-primary"><i class="fas fa-car"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Veículos na Garagem</span>
            <strong class="kpi-value">{{total_carros}}</strong>
            <span class="kpi-sub">Saúde média: <b>{{saude_media}}%</b></span>
        </div>
    </div>

    <div class="kpi-card">
        <div class="kpi-icon kpi-warning"><i class="fas fa-bell"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Alertas & Revisões</span>
            <strong class="kpi-value">{{len(alertas)}}</strong>
            <span class="kpi-sub">{{'Atenção necessária' if alertas else 'Tudo em dia!'}}</span>
        </div>
    </div>

    <div class="kpi-card">
        <div class="kpi-icon kpi-info"><i class="fas fa-screwdriver-wrench"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Total em Manutenções</span>
            <strong class="kpi-value">{{format_brl(custo_total_manutencoes)}}</strong>
            <span class="kpi-sub">{{total_manutencoes}} serviço(s) realizado(s)</span>
        </div>
    </div>

    <div class="kpi-card">
        <div class="kpi-icon kpi-success"><i class="fas fa-gas-pump"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Combustível & Operação</span>
            <strong class="kpi-value">{{format_brl(custo_total_combustivel)}}</strong>
            <span class="kpi-sub">Total Geral: <b>{{format_brl(custo_geral)}}</b></span>
        </div>
    </div>
</div>

<div class="dashboard-grid">
    <!-- Coluna Principal: Alertas + Garagem -->
    <div class="dashboard-main-col">

        <!-- Central de Alertas Inteligentes -->
        <div class="panel-card">
            <div class="panel-header">
                <h2><i class="fas fa-bell"></i> Central de Alertas e Próximas Revisões</h2>
                <span class="badge badge-{{'danger' if any(a['nivel']=='danger' for a in alertas) else ('warning' if alertas else 'success')}}">
                    {{len(alertas)}} pendência(s)
                </span>
            </div>

            % if alertas:
            <div class="alerts-list">
                % for alerta in alertas:
                <div class="alert-item alert-item-{{alerta['nivel']}}">
                    <div class="alert-item-icon">
                        % if alerta['nivel'] == 'danger':
                            <i class="fas fa-triangle-exclamation"></i>
                        % else:
                            <i class="fas fa-clock"></i>
                        % end
                    </div>
                    <div class="alert-item-body">
                        <div class="alert-item-title">
                            <a href="/carros/{{alerta['car_id']}}">{{alerta['titulo']}}</a>
                        </div>
                        <div class="alert-item-meta">
                            <span><i class="fas fa-car"></i> {{alerta['subtitulo']}}</span>
                            <span>&bull;</span>
                            <strong>{{alerta['detalhe']}}</strong>
                        </div>
                    </div>
                    <div class="alert-item-actions">
                        <form action="{{alerta['acao_url']}}" method="post" style="display:inline;">
                            <button type="submit" class="btn btn-sm btn-{{alerta['nivel']}}" title="Registrar como resolvido agora">
                                <i class="fas fa-check"></i> {{alerta['acao_label']}}
                            </button>
                        </form>
                        <a href="/carros/{{alerta['car_id']}}" class="btn btn-sm btn-secondary">Ver Carro</a>
                    </div>
                </div>
                % end
            </div>
            % else:
            <div class="empty-state-compact">
                <i class="fas fa-shield-heart text-success"></i>
                <p><strong>Parabéns!</strong> Nenhuma revisão atrasada ou peça em estado crítico no momento.</p>
            </div>
            % end
        </div>

        <!-- Meus Veículos e Saúde -->
        <div class="panel-card">
            <div class="panel-header">
                <h2><i class="fas fa-warehouse"></i> Saúde da Frota</h2>
                <a href="/carros" class="btn btn-sm btn-secondary">Gerenciar Garagem</a>
            </div>

            % if cars:
            <div class="fleet-cards">
                % for car in cars:
                <div class="fleet-card">
                    <div class="fleet-card-top">
                        <div>
                            <span class="plate-badge">{{car['placa']}}</span>
                            <h3 class="fleet-car-title">
                                <a href="/carros/{{car['id']}}">{{car['marca']}} {{car['modelo']}}</a>
                            </h3>
                            <span class="fleet-car-meta">{{car['ano']}} &bull; {{car['combustivel']}} &bull; {{format_km(car['km_atual'])}}</span>
                        </div>
                        <div class="health-pill health-{{car['saude_cor']}}">
                            <span>Saúde</span>
                            <strong>{{car['saude']}}%</strong>
                        </div>
                    </div>

                    <div class="health-bar-track" title="Saúde geral do veículo: {{car['saude']}}% ({{car['saude_label']}})">
                        <div class="health-bar-fill bg-{{car['saude_cor']}}" style="width: {{car['saude']}}%;"></div>
                    </div>

                    <div class="fleet-card-stats">
                        <div>
                            <small>Manutenções</small>
                            <strong>{{car['qtd_manutencoes']}} ({{format_brl(car['custo_manutencoes'])}})</strong>
                        </div>
                        <div>
                            <small>Agendamentos</small>
                            <strong>{{car['qtd_programadas']}} ativo(s)</strong>
                        </div>
                        <div>
                            <small>Peças Monitoradas</small>
                            <strong>{{car['qtd_itens_vida']}} item(ns)</strong>
                        </div>
                    </div>

                    <div class="fleet-card-actions">
                        <a href="/carros/{{car['id']}}" class="btn btn-sm btn-primary">
                            <i class="fas fa-eye"></i> Painel 360º
                        </a>
                        <a href="/car/{{car['id']}}/manutencoes/add" class="btn btn-sm btn-secondary">
                            <i class="fas fa-plus"></i> Manutenção
                        </a>
                        <a href="/car/{{car['id']}}/programadas/add" class="btn btn-sm btn-secondary">
                            <i class="fas fa-calendar-plus"></i> Agendar
                        </a>
                        <a href="/car/{{car['id']}}/abastecimentos/add" class="btn btn-sm btn-secondary">
                            <i class="fas fa-gas-pump"></i> Abastecer
                        </a>
                    </div>
                </div>
                % end
            </div>
            % else:
            <div class="empty-state">
                <i class="fas fa-car-side"></i>
                <h3>Sua garagem ainda está vazia</h3>
                <p>Cadastre seu primeiro veículo para acompanhar manutenções, peças de vida útil e consumo.</p>
                <a href="/carros/add" class="btn btn-primary"><i class="fas fa-plus"></i> Cadastrar Primeiro Veículo</a>
            </div>
            % end
        </div>
    </div>

    <!-- Coluna Lateral: Últimos Serviços + Distribuição de Gastos -->
    <div class="dashboard-side-col">
        <div class="panel-card">
            <div class="panel-header">
                <h2><i class="fas fa-chart-pie"></i> Gastos por Categoria</h2>
            </div>
            % if distribuicao_tipos:
            <div class="category-bars">
                % for item in distribuicao_tipos:
                <div class="cat-bar-item">
                    <div class="cat-bar-labels">
                        <span>{{item['tipo']}}</span>
                        <strong>{{format_brl(item['valor'])}} ({{item['percentual']}}%)</strong>
                    </div>
                    <div class="health-bar-track">
                        <div class="health-bar-fill bg-primary" style="width: {{max(5, item['percentual'])}}%;"></div>
                    </div>
                </div>
                % end
            </div>
            % else:
            <p class="text-muted">Nenhuma manutenção registrada ainda.</p>
            % end
        </div>

        <div class="panel-card">
            <div class="panel-header">
                <h2><i class="fas fa-clock-rotate-left"></i> Últimos Serviços</h2>
                <a href="/manutencoes" class="link-more">Ver todos</a>
            </div>
            % if ultimas_manutencoes:
            <div class="recent-list">
                % for m in ultimas_manutencoes:
                <div class="recent-item">
                    <div class="recent-item-main">
                        <strong>{{m['descricao']}}</strong>
                        <small>{{m.get('car_nome', '')}} ({{m.get('car_placa', '')}}) &bull; {{format_date_br(m['data'])}}</small>
                    </div>
                    <div class="recent-item-cost">
                        <span class="badge badge-neutral">{{m['tipo']}}</span>
                        <strong>{{format_brl(m['custo'])}}</strong>
                    </div>
                </div>
                % end
            </div>
            % else:
            <p class="text-muted">Nenhum serviço registrado recentemente.</p>
            % end
        </div>
    </div>
</div>
