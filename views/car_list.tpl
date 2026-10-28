% rebase('layout', title='Minha Garagem')

<div class="page-header">
    <div>
        <h1 class="page-title"><i class="fas fa-car-side"></i> Minha Garagem</h1>
        <p class="page-subtitle">Gerencie seus veículos, atualize o hodômetro rapidamente e acompanhe o índice de saúde de cada carro.</p>
    </div>
    <div class="header-actions">
        <a href="/carros/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Adicionar Veículo
        </a>
    </div>
</div>

% if cars:
<div class="garage-grid">
    % for car in cars:
    <div class="garage-card">
        <div class="garage-card-header">
            <div>
                <div class="garage-badges">
                    <span class="plate-badge">{{car['placa']}}</span>
                    <span class="badge badge-neutral">{{car['ano']}}</span>
                    <span class="badge badge-neutral">{{car['combustivel']}}</span>
                    % if car.get('cor'):
                        <span class="badge badge-neutral">{{car['cor']}}</span>
                    % end
                </div>
                <h2 class="garage-title">
                    <a href="/carros/{{car['id']}}">{{car['marca']}} {{car['modelo']}}</a>
                    % if car.get('apelido'):
                        <small class="car-nickname">"{{car['apelido']}}"</small>
                    % end
                </h2>
            </div>
            <div class="health-pill health-{{car['saude_cor']}}">
                <span>Saúde</span>
                <strong>{{car['saude']}}%</strong>
            </div>
        </div>

        <div class="health-bar-track">
            <div class="health-bar-fill bg-{{car['saude_cor']}}" style="width: {{car['saude']}}%;"></div>
        </div>

        <!-- Atualização Rápida de Hodômetro -->
        <form action="/carros/{{car['id']}}/atualizar-km" method="post" class="quick-km-form">
            <input type="hidden" name="redirect_to" value="/carros">
            <label for="km_{{car['id']}}"><i class="fas fa-road"></i> Hodômetro Atual (km):</label>
            <div class="quick-km-input-group">
                <input type="number" id="km_{{car['id']}}" name="km_atual" value="{{car['km_atual']}}" min="0" required>
                <button type="submit" class="btn btn-sm btn-secondary" title="Salvar nova quilometragem">
                    <i class="fas fa-arrows-rotate"></i> Atualizar KM
                </button>
            </div>
        </form>

        <div class="garage-metrics">
            <div class="metric-box">
                <span class="metric-label">Manutenções</span>
                <strong class="metric-val">{{format_brl(car['custo_manutencoes'])}}</strong>
                <small>{{car['qtd_manutencoes']}} registro(s)</small>
            </div>
            <div class="metric-box">
                <span class="metric-label">Combustível</span>
                <strong class="metric-val">{{format_brl(car['custo_combustivel'])}}</strong>
                <small>{{f"{car['consumo_medio_kml']} km/L" if car['consumo_medio_kml'] else 'Sem média'}}</small>
            </div>
            <div class="metric-box">
                <span class="metric-label">Alertas / Revisões</span>
                % if car['alertas_criticos'] > 0:
                    <strong class="metric-val text-danger">{{car['alertas_criticos']}} Crítico(s)</strong>
                % elif car['alertas_aviso'] > 0:
                    <strong class="metric-val text-warning">{{car['alertas_aviso']}} Próximo(s)</strong>
                % else:
                    <strong class="metric-val text-success">Em dia</strong>
                % end
                <small>{{car['qtd_itens_vida']}} peças monitoradas</small>
            </div>
        </div>

        % if car.get('observacoes'):
        <p class="car-notes"><i class="fas fa-circle-info"></i> {{car['observacoes']}}</p>
        % end

        <div class="garage-card-footer">
            <a href="/carros/{{car['id']}}" class="btn btn-primary btn-sm">
                <i class="fas fa-sliders"></i> Painel Completo do Carro
            </a>
            <div class="garage-secondary-actions">
                <a href="/car/{{car['id']}}/manutencoes/add" class="btn btn-secondary btn-sm" title="Registrar Manutenção">
                    <i class="fas fa-wrench"></i> + Serviço
                </a>
                <a href="/carros/edit/{{car['id']}}" class="btn btn-secondary btn-sm" title="Editar Veículo">
                    <i class="fas fa-pen"></i>
                </a>
                <a href="/carros/delete/{{car['id']}}" class="btn btn-danger-outline btn-sm" onclick="return confirm('Tem certeza que deseja excluir este veículo e todo o seu histórico?')" title="Excluir Veículo">
                    <i class="fas fa-trash"></i>
                </a>
            </div>
        </div>
    </div>
    % end
</div>
% else:
<div class="empty-state">
    <i class="fas fa-car"></i>
    <h3>Nenhum veículo cadastrado</h3>
    <p>Adicione seu carro para habilitar o controle de manutenções preventivas, vida útil de peças e abastecimentos.</p>
    <a href="/carros/add" class="btn btn-primary"><i class="fas fa-plus"></i> Adicionar Novo Carro</a>
</div>
% end
