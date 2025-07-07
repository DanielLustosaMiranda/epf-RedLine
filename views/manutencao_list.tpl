%rebase('layout', title='Histórico de Manutenções')

<section class="maintenance-section">
    <div class="section-header">
        % if car:
            <h1 class="section-title">Manutenções para: {{car['marca']}} {{car['modelo']}} ({{car['placa']}})</h1>
            <a href="/car/{{car['id']}}/manutencoes/add" class="btn btn-primary">
                <i class="fas fa-plus"></i> Nova Manutenção
            </a>
        % else:
            <h1 class="section-title">Carro não encontrado</h1>
        % end
    </div>

    <div class="table-container">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Data</th>
                    <th>KM</th>
                    <th>Descrição</th>
                    <th>Tipo</th>
                    <th>Custo (R$)</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                % for m in manutencoes:
                <tr>
                    <td>{{m['data']}}</td>
                    <td>{{m['km']}} km</td>
                    <td>{{m['descricao']}}</td>
                    <td>{{m['tipo']}}</td>
                    <td>{{m['custo']}}</td>
                    <td class="actions">
                    <a href="/manutencao/edit/{{m['id']}}" class="btn btn-sm btn-edit">
                        <i class="fas fa-edit"></i> Editar
                    </a>
                    <a href="/manutencao/delete/{{m['id']}}" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza?')">
                        <i class="fas fa-trash-alt"></i> Excluir
                    </a>
                </td>
                </tr>
                % end
                % if not manutencoes:
                <tr>
                    <td colspan="6">Nenhuma manutenção registrada para este veículo.</td>
                </tr>
                % end
            </tbody>
        </table>
        <div class="form-actions">
            <a href="/carros" class="btn btn-secondary">Voltar para Meus Carros</a>
        </div>
    </div>
</section>