%rebase('layout', title='Formulário de Carro')

% if car:
%   action_url = f"/carros/edit/{car['id']}"
%   page_title = "Editando Carro"
% else:
%   action_url = "/carros/add"
%   page_title = "Adicionar Novo Carro"
% end

<section class="form-section">
    <h1 class="section-title">{{page_title}}</h1>

    <form action="{{action_url}}" method="post" class="styled-form">
        <div class="form-group">
            <label for="marca">Marca:</label>
            <input type="text" id="marca" name="marca" value="{{car['marca'] if car else ''}}" required>
        </div>

        <div class="form-group">
            <label for="modelo">Modelo:</label>
            <input type="text" id="modelo" name="modelo" value="{{car['modelo'] if car else ''}}" required>
        </div>

        <div class="form-group">
            <label for="ano">Ano:</label>
            <input type="number" id="ano" name="ano" value="{{car['ano'] if car else ''}}" required>
        </div>

        <div class="form-group">
            <label for="placa">Placa:</label>
            <input type="text" id="placa" name="placa" value="{{car['placa'] if car else ''}}" required>
        </div>
        
        <div class="form-group">
            <label for="km_atual">Quilometragem Atual:</label>
            <input type="number" id="km_atual" name="km_atual" value="{{car['km_atual'] if car else ''}}" required>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar</button>
            <a href="/carros" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</section>