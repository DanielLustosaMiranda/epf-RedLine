%rebase('layout', title='Formulário de Manutenção')

% if manutencao:
%   action_url = f"/manutencao/edit/{manutencao['id']}"
%   page_title = "Editando Manutenção"
% else:
%   action_url = f"/car/{car['id']}/manutencoes/add"
%   page_title = f"Adicionar Manutenção para: {car['marca']} {car['modelo']}"
% end

<section class="form-section">
    <h1 class="section-title">{{page_title}}</h1>

    <form action="{{action_url}}" method="post" class="styled-form">
        <div class="form-group">
            <label for="data">Data:</label>
            <input type="date" id="data" name="data" value="{{manutencao.get('data', '') if manutencao else ''}}" required>
        </div>
        <div class="form-group">
            <label for="km">Quilometragem:</label>
            <input type="number" id="km" name="km" value="{{manutencao.get('km', '') if manutencao else ''}}" required>
        </div>
        <div class="form-group">
            <label for="descricao">Descrição do Serviço:</label>
            <input type="text" id="descricao" name="descricao" value="{{manutencao.get('descricao', '') if manutencao else ''}}" required>
        </div>
        <div class="form-group">
            <label for="tipo">Tipo de Manutenção:</label>
            <input type="text" id="tipo" name="tipo" value="{{manutencao.get('tipo', '') if manutencao else ''}}">
        </div>
        <div class="form-group">
            <label for="custo">Custo (R$):</label>
            <input type="number" step="0.01" id="custo" name="custo" value="{{manutencao.get('custo', '') if manutencao else ''}}" required>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar</button>
            <a href="/car/{{car['id']}}/manutencoes" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</section>