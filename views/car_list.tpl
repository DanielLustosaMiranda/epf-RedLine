%rebase('layout', title='Meus Carros')

<section class="cars-section">
    <div class="section-header">
        <h1 class="section-title"><i class="fas fa-car"></i> Meus Carros</h1>
        <a href="/carros/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Novo Carro
        </a>
    </div>

    <div class="table-container">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Modelo / Marca</th>
                    <th>Placa</th>
                    <th>Ano</th>
                    <th>KM Atual</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                % for car in cars:
                <tr>
                    <td>{{car['marca']}} {{car['modelo']}}</td>
                    <td>{{car['placa']}}</td>
                    <td>{{car['ano']}}</td>
                    <td>{{car['km_atual']}} km</td>
                    <td class="actions">
                        <a href="/car/{{car['id']}}/manutencoes" class="btn btn-sm btn-info">
                            <i class="fas fa-history"></i> Histórico
                        </a>
                        <a href="/carros/edit/{{car['id']}}" class="btn btn-sm btn-edit">
                            <i class="fas fa-edit"></i> Editar
                        </a>
                        <a href="/carros/delete/{{car['id']}}" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza?')">
                            <i class="fas fa-trash-alt"></i> Excluir
                        </a>
                    </td>
                </tr>
                % end
                % if not cars:
                <tr>
                    <td colspan="5">Você ainda não cadastrou nenhum carro.</td>
                </tr>
                % end
            </tbody>
        </table>
    </div>

    <div class="page-actions" style="margin-top: 20px;">
        <a href="/logout" class="btn btn-secondary">Sair</a>
    </div>

</section>