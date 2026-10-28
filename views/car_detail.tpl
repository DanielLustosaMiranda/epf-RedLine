% rebase('layout', title=f"{car['marca']} {car['modelo']}")

<!-- Cabeçalho 360º do Veículo -->
<div class="vehicle-hero">
    <div class="vehicle-hero-main">
        <div class="vehicle-hero-badges">
            <a href="/carros" class="back-chip"><i class="fas fa-arrow-left"></i> Minha Garagem</a>
            <span class="plate-badge">{{car['placa']}}</span>
            <span class="badge badge-neutral">{{car['ano']}}</span>
            <span class="badge badge-neutral"><i class="fas fa-gas-pump"></i> {{car['combustivel']}}</span>
            % if car.get('cor'):
                <span class="badge badge-neutral"><i class="fas fa-palette"></i> {{car['cor']}}</span>
            % end
        </div>
        <h1 class="vehicle-hero-title">
            {{car['marca']}} {{car['modelo']}}
            % if car.get('apelido'):
                <span class="car-nickname">"{{car['apelido']}}"</span>
            % end
        </h1>
        % if car.get('observacoes'):
            <p class="vehicle-hero-notes"><i class="fas fa-note-sticky"></i> {{car['observacoes']}}</p>
        % end
    </div>

    <div class="vehicle-hero-side">
        <div class="hero-health-box">
            <div class="hero-health-header">
                <span>Índice de Saúde ({{car['saude_label']}})</span>
                <strong class="text-{{car['saude_cor']}}">{{car['saude']}}%</strong>
            </div>
            <div class="health-bar-track">
                <div class="health-bar-fill bg-{{car['saude_cor']}}" style="width: {{car['saude']}}%;"></div>
            </div>
        </div>

        <form action="/carros/{{car['id']}}/atualizar-km" method="post" class="hero-km-form">
            <input type="hidden" name="redirect_to" value="/carros/{{car['id']}}">
            <div class="quick-km-input-group">
                <input type="number" name="km_atual" value="{{car['km_atual']}}" min="0" required title="Quilometragem atual">
                <button type="submit" class="btn btn-sm btn-secondary">
                    <i class="fas fa-road"></i> Atualizar KM
                </button>
            </div>
        </form>

        <div class="hero-top-buttons">
            <a href="/carros/edit/{{car['id']}}" class="btn btn-sm btn-secondary"><i class="fas fa-pen"></i> Editar Dados</a>
            <a href="/relatorios?car_id={{car['id']}}" class="btn btn-sm btn-secondary"><i class="fas fa-print"></i> Relatório</a>
        </div>
    </div>
</div>

<!-- Mini KPIs do Veículo -->
<div class="kpi-grid kpi-grid-compact">
    <div class="kpi-card">
        <div class="kpi-icon kpi-primary"><i class="fas fa-road"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Hodômetro Atual</span>
            <strong class="kpi-value">{{format_km(car['km_atual'])}}</strong>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon kpi-info"><i class="fas fa-screwdriver-wrench"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Gasto em Manutenções</span>
            <strong class="kpi-value">{{format_brl(car['custo_manutencoes'])}}</strong>
            <span class="kpi-sub">{{len(manutencoes)}} serviço(s)</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon kpi-success"><i class="fas fa-gas-pump"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Gasto em Combustível</span>
            <strong class="kpi-value">{{format_brl(combustivel_stats['total_gasto'])}}</strong>
            <span class="kpi-sub">Média: {{f"{combustivel_stats['consumo_medio_kml']} km/L" if combustivel_stats['consumo_medio_kml'] else 'N/D'}}</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon kpi-warning"><i class="fas fa-calendar-check"></i></div>
        <div class="kpi-info">
            <span class="kpi-label">Custo Operacional Total</span>
            <strong class="kpi-value">{{format_brl(car['custo_total'])}}</strong>
            <span class="kpi-sub">{{len(programadas)}} agendamento(s) &bull; {{len(itens_vida)}} peça(s)</span>
        </div>
    </div>
</div>

<!-- Navegação por Abas -->
<div class="tabs-nav" data-active-tab="{{aba_ativa}}">
    <button type="button" class="tab-btn {{'active' if aba_ativa in ('visao-geral', 'programadas') else ''}}" data-tab-target="tab-programadas">
        <i class="fas fa-calendar-alt"></i> Manutenções Programadas ({{len(programadas)}})
    </button>
    <button type="button" class="tab-btn {{'active' if aba_ativa == 'vida-util' else ''}}" data-tab-target="tab-vida-util">
        <i class="fas fa-microchip"></i> Vida Útil de Peças ({{len(itens_vida)}})
    </button>
    <button type="button" class="tab-btn {{'active' if aba_ativa == 'historico' else ''}}" data-tab-target="tab-historico">
        <i class="fas fa-clock-rotate-left"></i> Histórico Realizado ({{len(manutencoes)}})
    </button>
    <button type="button" class="tab-btn {{'active' if aba_ativa == 'abastecimentos' else ''}}" data-tab-target="tab-abastecimentos">
        <i class="fas fa-gas-pump"></i> Abastecimentos ({{len(abastecimentos)}})
    </button>
</div>

<!-- ABA 1: MANUTENÇÕES PROGRAMADAS -->
<section id="tab-programadas" class="tab-pane {{'active' if aba_ativa in ('visao-geral', 'programadas') else ''}}">
    <div class="panel-card">
        <div class="panel-header">
            <div>
                <h2><i class="fas fa-calendar-check"></i> Revisões e Manutenções Programadas</h2>
                <p class="panel-subtitle">Agende revisões por prazo (dias) e por quilometragem (km). Ao concluir com 1 clique, o serviço vai direto para o histórico!</p>
            </div>
            <a href="/car/{{car['id']}}/programadas/add" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Nova Manutenção Programada
            </a>
        </div>

        % if programadas:
        <div class="table-responsive">
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Serviço Programado</th>
                        <th>Última Realização</th>
                        <th>Próximo Vencimento</th>
                        <th>Custo Estimado</th>
                        <th>Ações Rápidas</th>
                    </tr>
                </thead>
                <tbody>
                    % for p in programadas:
                    <tr>
                        <td>
                            % if p['status'] == 'atrasada':
                                <span class="badge badge-danger"><i class="fas fa-circle-exclamation"></i> Atrasada</span>
                            % elif p['status'] == 'proxima':
                                <span class="badge badge-warning"><i class="fas fa-clock"></i> Próxima</span>
                            % else:
                                <span class="badge badge-success"><i class="fas fa-check"></i> Em Dia</span>
                            % end
                            <div><small class="text-muted">{{p['resumo_status']}}</small></div>
                        </td>
                        <td>
                            <strong>{{p['descricao']}}</strong>
                            <div>
                                <small class="text-muted">
                                    A cada {{p['frequencia_dias']}} dias
                                    % if p.get('frequencia_km'):
                                        ou {{format_km(p['frequencia_km'])}}
                                    % end
                                </small>
                            </div>
                        </td>
                        <td>
                            <div>{{format_date_br(p['ultima_data'])}}</div>
                            <small class="text-muted">{{format_km(p.get('ultimo_km', 0))}}</small>
                        </td>
                        <td>
                            <div><strong>{{format_date_br(p['proxima_data'])}}</strong></div>
                            % if p.get('proximo_km'):
                                <small class="text-muted">ou {{format_km(p['proximo_km'])}}</small>
                            % end
                        </td>
                        <td>{{format_brl(p.get('custo_estimado', 0))}}</td>
                        <td class="actions-cell">
                            <form action="/programada/concluir/{{p['id']}}" method="post" style="display:inline;">
                                <button type="submit" class="btn btn-sm btn-success" title="Registrar como feita hoje e reiniciar ciclo">
                                    <i class="fas fa-check"></i> Concluir
                                </button>
                            </form>
                            <a href="/programada/edit/{{p['id']}}" class="btn btn-sm btn-secondary" title="Editar">
                                <i class="fas fa-pen"></i>
                            </a>
                            <a href="/programada/delete/{{p['id']}}" class="btn btn-sm btn-danger-outline" onclick="return confirm('Remover este agendamento?')" title="Excluir">
                                <i class="fas fa-trash"></i>
                            </a>
                        </td>
                    </tr>
                    % end
                </tbody>
            </table>
        </div>
        % else:
        <div class="empty-state-compact">
            <i class="fas fa-calendar-plus"></i>
            <p>Nenhuma manutenção programada para este veículo.</p>
            <a href="/car/{{car['id']}}/programadas/add" class="btn btn-primary btn-sm">Agendar Primeira Revisão</a>
        </div>
        % end
    </div>
</section>

<!-- ABA 2: VIDA ÚTIL DE PEÇAS -->
<section id="tab-vida-util" class="tab-pane {{'active' if aba_ativa == 'vida-util' else ''}}">
    <div class="panel-card">
        <div class="panel-header">
            <div>
                <h2><i class="fas fa-microchip"></i> Monitoramento de Vida Útil de Peças e Fluidos</h2>
                <p class="panel-subtitle">Acompanhe o desgaste estimado de óleo, pneus, bateria, freios e correias por tempo de uso e quilometragem.</p>
            </div>
            <div class="header-actions">
                <form action="/car/{{car['id']}}/vida-util/kit-padrao" method="post" style="display:inline;">
                    <button type="submit" class="btn btn-secondary btn-sm" title="Gera automaticamente os 8 itens essenciais de monitoramento">
                        <i class="fas fa-wand-magic-sparkles"></i> Gerar Kit Essencial (8 Peças)
                    </button>
                </form>
                <a href="/car/{{car['id']}}/vida-util/add" class="btn btn-primary btn-sm">
                    <i class="fas fa-plus"></i> Adicionar Peça
                </a>
            </div>
        </div>

        % if itens_vida:
        <div class="parts-grid">
            % for iv in itens_vida:
            %   cor_iv = 'danger' if iv['status'] == 'critico' else ('warning' if iv['status'] == 'atencao' else 'success')
            <div class="part-card">
                <div class="part-card-top">
                    <div>
                        <h4>{{iv['nome_item']}}</h4>
                        % if iv.get('marca_peca'):
                            <span class="badge badge-neutral">{{iv['marca_peca']}}</span>
                        % end
                    </div>
                    <span class="badge badge-{{cor_iv}}">{{iv['saude_percentual']}}% Vida Útil</span>
                </div>

                <div class="health-bar-track">
                    <div class="health-bar-fill bg-{{cor_iv}}" style="width: {{max(4, iv['saude_percentual'])}}%;"></div>
                </div>

                <div class="part-details">
                    <div>
                        <small>Instalado em:</small>
                        <strong>{{format_date_br(iv['data_instalacao'])}} ({{format_km(iv.get('km_instalacao', 0))}})</strong>
                    </div>
                    <div>
                        <small>Troca prevista:</small>
                        <strong>{{format_date_br(iv['data_vencimento'])}} {{f"ou {format_km(iv['km_vencimento'])}" if iv.get('km_vencimento') else ''}}</strong>
                    </div>
                </div>

                <div class="part-actions">
                    <form action="/vida-util/renovar/{{iv['id']}}" method="post" style="display:inline;">
                        <button type="submit" class="btn btn-sm btn-secondary" title="Substituir peça hoje (reinicia para 100% e grava no histórico)">
                            <i class="fas fa-rotate"></i> Substituir Peça (100%)
                        </button>
                    </form>
                    <div>
                        <a href="/vida-util/edit/{{iv['id']}}" class="btn btn-sm btn-secondary" title="Editar"><i class="fas fa-pen"></i></a>
                        <a href="/vida-util/delete/{{iv['id']}}" class="btn btn-sm btn-danger-outline" onclick="return confirm('Remover este componente?')" title="Excluir"><i class="fas fa-trash"></i></a>
                    </div>
                </div>
            </div>
            % end
        </div>
        % else:
        <div class="empty-state-compact">
            <i class="fas fa-gears"></i>
            <p>Nenhuma peça monitorada ainda. Use o botão <strong>Gerar Kit Essencial</strong> para criar automaticamente os 8 itens principais!</p>
        </div>
        % end
    </div>
</section>

<!-- ABA 3: HISTÓRICO DE MANUTENÇÕES REALIZADAS -->
<section id="tab-historico" class="tab-pane {{'active' if aba_ativa == 'historico' else ''}}">
    <div class="panel-card">
        <div class="panel-header">
            <div>
                <h2><i class="fas fa-clock-rotate-left"></i> Histórico de Manutenções Realizadas</h2>
                <p class="panel-subtitle">Todos os serviços executados neste veículo, oficinas, garantias e valores pagos.</p>
            </div>
            <a href="/car/{{car['id']}}/manutencoes/add" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Registrar Manutenção
            </a>
        </div>

        % if manutencoes:
        <div class="table-responsive">
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>KM</th>
                        <th>Descrição do Serviço</th>
                        <th>Oficina / Garantia</th>
                        <th>Tipo</th>
                        <th>Custo</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    % for m in manutencoes:
                    <tr>
                        <td>{{format_date_br(m['data'])}}</td>
                        <td>{{format_km(m['km'])}}</td>
                        <td>
                            <strong>{{m['descricao']}}</strong>
                            % if m.get('observacoes'):
                                <div><small class="text-muted">{{m['observacoes']}}</small></div>
                            % end
                        </td>
                        <td>
                            {{m.get('oficina') or '-'}}
                            % if m.get('garantia_meses') and int(m.get('garantia_meses', 0)) > 0:
                                <div><small class="text-success"><i class="fas fa-shield"></i> Garantia: {{m['garantia_meses']}} meses</small></div>
                            % end
                        </td>
                        <td><span class="badge badge-neutral">{{m['tipo']}}</span></td>
                        <td><strong>{{format_brl(m['custo'])}}</strong></td>
                        <td class="actions-cell">
                            <a href="/manutencao/edit/{{m['id']}}" class="btn btn-sm btn-secondary" title="Editar"><i class="fas fa-pen"></i></a>
                            <a href="/manutencao/delete/{{m['id']}}" class="btn btn-sm btn-danger-outline" onclick="return confirm('Excluir esta manutenção?')" title="Excluir"><i class="fas fa-trash"></i></a>
                        </td>
                    </tr>
                    % end
                </tbody>
            </table>
        </div>
        % else:
        <div class="empty-state-compact">
            <i class="fas fa-screwdriver-wrench"></i>
            <p>Nenhuma manutenção registrada para este veículo.</p>
            <a href="/car/{{car['id']}}/manutencoes/add" class="btn btn-primary btn-sm">Registrar Primeiro Serviço</a>
        </div>
        % end
    </div>
</section>

<!-- ABA 4: ABASTECIMENTOS E CONSUMO -->
<section id="tab-abastecimentos" class="tab-pane {{'active' if aba_ativa == 'abastecimentos' else ''}}">
    <div class="panel-card">
        <div class="panel-header">
            <div>
                <h2><i class="fas fa-gas-pump"></i> Controle de Abastecimentos e Consumo</h2>
                <p class="panel-subtitle">
                    Total abastecido: <strong>{{combustivel_stats['total_litros']}} L</strong> &bull;
                    Preço médio/L: <strong>{{format_brl(combustivel_stats['preco_medio_litro'])}}</strong> &bull;
                    Consumo médio: <strong>{{f"{combustivel_stats['consumo_medio_kml']} km/L" if combustivel_stats['consumo_medio_kml'] else 'Aguardando 2+ registros'}}</strong>
                </p>
            </div>
            <a href="/car/{{car['id']}}/abastecimentos/add" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Novo Abastecimento
            </a>
        </div>

        % if abastecimentos:
        <div class="table-responsive">
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>KM</th>
                        <th>Combustível</th>
                        <th>Posto</th>
                        <th>Litros</th>
                        <th>Preço/L</th>
                        <th>Valor Total</th>
                        <th>Média (km/L)</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    % for a in abastecimentos:
                    <tr>
                        <td>{{format_date_br(a['data'])}}</td>
                        <td>{{format_km(a['km'])}}</td>
                        <td>{{a['combustivel']}}</td>
                        <td>{{a.get('posto') or '-'}}</td>
                        <td>{{a['litros']}} L</td>
                        <td>{{format_brl(a.get('preco_litro', 0))}}</td>
                        <td><strong>{{format_brl(a['valor_total'])}}</strong></td>
                        <td>
                            % if a.get('consumo_kml'):
                                <span class="badge badge-success">{{a['consumo_kml']}} km/L</span>
                            % else:
                                <span class="text-muted">-</span>
                            % end
                        </td>
                        <td class="actions-cell">
                            <a href="/abastecimento/delete/{{a['id']}}" class="btn btn-sm btn-danger-outline" onclick="return confirm('Remover este abastecimento?')"><i class="fas fa-trash"></i></a>
                        </td>
                    </tr>
                    % end
                </tbody>
            </table>
        </div>
        % else:
        <div class="empty-state-compact">
            <i class="fas fa-gas-pump"></i>
            <p>Nenhum abastecimento registrado para este veículo.</p>
            <a href="/car/{{car['id']}}/abastecimentos/add" class="btn btn-primary btn-sm">Registrar Primeiro Abastecimento</a>
        </div>
        % end
    </div>
</section>
