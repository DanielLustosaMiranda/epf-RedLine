% rebase('layout', title='Histórico de Manutenções')

<div class="page-header">
    <div>
        <h1 class="page-title">
            <i class="fas fa-screwdriver-wrench"></i>
            {{f"Manutenções: {car['marca']} {car['modelo']} ({car['placa']})" if car else "Histórico Geral de Manutenções"}}
        </h1>
        <p class="page-subtitle">Consulte, filtre e gerencie todos os serviços executados nos seus veículos.</p>
    </div>
    <div class="header-actions">
        % if car:
            <a href="/car/{{car['id']}}/manutencoes/add" class="btn btn-primary">
                <i class="fas fa-plus"></i> Nova Manutenção
            </a>
            <a href="/carros/{{car['id']}}" class="btn btn-secondary">
                <i class="fas fa-car"></i> Painel do Carro
            </a>
        % elif cars:
            <a href="/car/{{cars[0]['id']}}/manutencoes/add" class="btn btn-primary">
                <i class="fas fa-plus"></i> Registrar Manutenção
            </a>
        % end
    </div>
</div>

<!-- Barra de Filtros -->
<div class="filter-bar panel-card no-print">
    <form action="/manutencoes" method="get" class="filter-form">
        <div class="filter-group">
            <label for="f_car">Veículo:</label>
            <select id="f_car" name="car_id">
                <option value="">Todos os veículos</option>
                % for c in cars:
                    <option value="{{c['id']}}" {{'selected' if filtro_car_id == c['id'] else ''}}>
                        {{c['marca']}} {{c['modelo']}} ({{c['placa']}})
                    </option>
                % end
            </select>
        </div>

        <div class="filter-group">
            <label for="f_tipo">Categoria:</label>
            <select id="f_tipo" name="tipo">
                <option value="">Todas as categorias</option>
                % for tm in tipos_manutencao:
                    <option value="{{tm}}" {{'selected' if filtro_tipo == tm else ''}}>{{tm}}</option>
                % end
            </select>
        </div>

        <div class="filter-group filter-group-grow">
            <label for="f_q">Buscar serviço / oficina:</label>
            <input type="text" id="f_q" name="q" value="{{filtro_busca}}" placeholder="Ex: óleo, freio, alinhamento, oficina...">
        </div>

        <div class="filter-buttons">
            <button type="submit" class="btn btn-primary btn-sm"><i class="fas fa-filter"></i> Filtrar</button>
            <a href="/manutencoes" class="btn btn-secondary btn-sm">Limpar</a>
        </div>
    </form>
</div>

<!-- Tabela de Resultados -->
<div class="panel-card">
    <div class="panel-header">
        <h2><i class="fas fa-list-check"></i> {{len(manutencoes)}} Serviço(s) Encontrado(s)</h2>
        <div class="total-pill">
            Total Filtrado: <strong>{{format_brl(total_custo)}}</strong>
        </div>
    </div>

    % if manutencoes:
    <div class="table-responsive">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Data</th>
                    <th>Veículo</th>
                    <th>KM</th>
                    <th>Descrição do Serviço</th>
                    <th>Oficina / Garantia</th>
                    <th>Categoria</th>
                    <th>Custo</th>
                    <th class="no-print">Ações</th>
                </tr>
            </thead>
            <tbody>
                % for m in manutencoes:
                <tr>
                    <td>{{format_date_br(m['data'])}}</td>
                    <td>
                        <a href="/carros/{{m['car_id']}}"><strong>{{m.get('car_nome', 'Veículo')}}</strong></a>
                        <div><small class="text-muted">{{m.get('car_placa', '')}}</small></div>
                    </td>
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
                            <div><small class="text-success"><i class="fas fa-shield"></i> {{m['garantia_meses']}} meses</small></div>
                        % end
                    </td>
                    <td><span class="badge badge-neutral">{{m['tipo']}}</span></td>
                    <td><strong>{{format_brl(m['custo'])}}</strong></td>
                    <td class="actions-cell no-print">
                        <a href="/manutencao/edit/{{m['id']}}" class="btn btn-sm btn-secondary" title="Editar"><i class="fas fa-pen"></i></a>
                        <a href="/manutencao/delete/{{m['id']}}" class="btn btn-sm btn-danger-outline" onclick="return confirm('Tem certeza que deseja excluir esta manutenção?')" title="Excluir"><i class="fas fa-trash"></i></a>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
    </div>
    % else:
    <div class="empty-state-compact">
        <i class="fas fa-folder-open"></i>
        <p>Nenhuma manutenção encontrada para os filtros selecionados.</p>
    </div>
    % end
</div>
