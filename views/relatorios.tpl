% rebase('layout', title='Relatórios Financeiros e Técnicos')

<div class="page-header">
    <div>
        <h1 class="page-title"><i class="fas fa-file-invoice-dollar"></i> Relatórios & Análise de Custos</h1>
        <p class="page-subtitle">Acompanhe o Custo Total de Propriedade (Manutenções + Combustível) e imprima dossiês de revisão para valorizar seu veículo na revenda.</p>
    </div>
    <div class="header-actions no-print">
        <button type="button" class="btn btn-primary" onclick="window.print()">
            <i class="fas fa-print"></i> Imprimir / Salvar PDF
        </button>
    </div>
</div>

<!-- Filtro por Veículo para Dossiê -->
<div class="filter-bar panel-card no-print">
    <form action="/relatorios" method="get" class="filter-form">
        <div class="filter-group filter-group-grow">
            <label for="rel_car">Filtrar Dossiê por Veículo:</label>
            <select id="rel_car" name="car_id" onchange="this.form.submit()">
                <option value="">Visão Consolidada (Toda a Frota)</option>
                % for c in cars:
                    <option value="{{c['id']}}" {{'selected' if car_filter == c['id'] else ''}}>
                        {{c['marca']}} {{c['modelo']}} ({{c['placa']}})
                    </option>
                % end
            </select>
        </div>
        % if car_filter:
        <div class="filter-buttons">
            <a href="/relatorios" class="btn btn-secondary btn-sm">Ver Toda a Frota</a>
        </div>
        % end
    </form>
</div>

% if selected_car:
<!-- Dossiê Individual do Veículo -->
<div class="panel-card">
    <div class="panel-header">
        <div>
            <h2><i class="fas fa-certificate"></i> Dossiê Técnico do Veículo: {{selected_car['marca']}} {{selected_car['modelo']}}</h2>
            <p class="panel-subtitle">Placa: <strong>{{selected_car['placa']}}</strong> &bull; Ano: <strong>{{selected_car['ano']}}</strong> &bull; KM Atual: <strong>{{format_km(selected_car['km_atual'])}}</strong> &bull; Saúde: <strong>{{selected_car['saude']}}%</strong></p>
        </div>
        <div class="total-pill">
            Total Investido: <strong>{{format_brl(selected_car['custo_total'])}}</strong>
        </div>
    </div>

    <div class="kpi-grid kpi-grid-compact">
        <div class="kpi-card">
            <div class="kpi-info">
                <span class="kpi-label">Manutenções Realizadas</span>
                <strong class="kpi-value">{{format_brl(selected_car['custo_manutencoes'])}}</strong>
                <span class="kpi-sub">{{selected_car['qtd_manutencoes']}} serviços documentados</span>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-info">
                <span class="kpi-label">Gasto com Combustível</span>
                <strong class="kpi-value">{{format_brl(selected_car['custo_combustivel'])}}</strong>
                <span class="kpi-sub">Consumo: {{f"{selected_car['consumo_medio_kml']} km/L" if selected_car['consumo_medio_kml'] else 'N/D'}}</span>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-info">
                <span class="kpi-label">Componentes Monitorados</span>
                <strong class="kpi-value">{{selected_car['qtd_itens_vida']}} peças</strong>
                <span class="kpi-sub">Saúde geral: {{selected_car['saude']}}%</span>
            </div>
        </div>
    </div>

    <h3 class="subsection-title">Histórico Completo de Manutenções Documentadas</h3>
    % if selected_car['manutencoes']:
    <div class="table-responsive">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Data</th>
                    <th>KM</th>
                    <th>Serviço Executado</th>
                    <th>Oficina</th>
                    <th>Categoria</th>
                    <th>Valor</th>
                </tr>
            </thead>
            <tbody>
                % for m in selected_car['manutencoes']:
                <tr>
                    <td>{{format_date_br(m['data'])}}</td>
                    <td>{{format_km(m['km'])}}</td>
                    <td>{{m['descricao']}}</td>
                    <td>{{m.get('oficina') or '-'}}</td>
                    <td>{{m['tipo']}}</td>
                    <td><strong>{{format_brl(m['custo'])}}</strong></td>
                </tr>
                % end
            </tbody>
        </table>
    </div>
    % else:
    <p class="text-muted">Nenhuma manutenção registrada para este veículo.</p>
    % end
</div>

% else:
<!-- Relatório Consolidado da Frota -->
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon kpi-primary"><i class="fas fa-wallet"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Custo Total da Frota</span>
            <strong class="kpi-value">{{format_brl(custo_geral)}}</strong>
            <span class="kpi-sub">Manutenções + Abastecimentos</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon kpi-info"><i class="fas fa-screwdriver-wrench"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Total em Manutenções</span>
            <strong class="kpi-value">{{format_brl(custo_total_manutencoes)}}</strong>
            <span class="kpi-sub">{{total_manutencoes}} serviços realizados</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon kpi-success"><i class="fas fa-gas-pump"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Total em Combustível</span>
            <strong class="kpi-value">{{format_brl(custo_total_combustivel)}}</strong>
            <span class="kpi-sub">Em {{total_carros}} veículo(s)</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon kpi-warning"><i class="fas fa-heart-pulse"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Índice Médio de Saúde</span>
            <strong class="kpi-value">{{saude_media}}%</strong>
            <span class="kpi-sub">{{len(alertas)}} alerta(s) ativo(s)</span>
        </div>
    </div>
</div>

<div class="dashboard-grid">
    <div class="dashboard-main-col">
        <div class="panel-card">
            <div class="panel-header">
                <h2><i class="fas fa-car"></i> Comparativo de Custos por Veículo</h2>
            </div>
            % if cars:
            <div class="table-responsive">
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Veículo</th>
                            <th>Placa</th>
                            <th>KM Atual</th>
                            <th>Saúde</th>
                            <th>Manutenções</th>
                            <th>Combustível</th>
                            <th>Custo Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for c in cars:
                        <tr>
                            <td><a href="/relatorios?car_id={{c['id']}}"><strong>{{c['marca']}} {{c['modelo']}}</strong></a></td>
                            <td><span class="plate-badge">{{c['placa']}}</span></td>
                            <td>{{format_km(c['km_atual'])}}</td>
                            <td><span class="badge badge-{{c['saude_cor']}}">{{c['saude']}}%</span></td>
                            <td>{{format_brl(c['custo_manutencoes'])}} ({{c['qtd_manutencoes']}})</td>
                            <td>{{format_brl(c['custo_combustivel'])}}</td>
                            <td><strong>{{format_brl(c['custo_total'])}}</strong></td>
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>
            % else:
            <p class="text-muted">Nenhum veículo cadastrado.</p>
            % end
        </div>
    </div>

    <div class="dashboard-side-col">
        <div class="panel-card">
            <div class="panel-header">
                <h2><i class="fas fa-chart-pie"></i> Custos por Categoria</h2>
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
            <p class="text-muted">Sem dados para exibir.</p>
            % end
        </div>
    </div>
</div>
% end
