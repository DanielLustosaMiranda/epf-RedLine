%rebase('layout', title='Formulário de Usuário')

% if user:
%   action_url = f"/users/edit/{user['id']}"
%   page_title = f"Editando Usuário: {user['name']}"
% else:
%   action_url = "/users/add"
%   page_title = "Adicionar Novo Usuário"
% end

<section class="form-section">
    <h1 class="section-title">{{page_title}}</h1>

    <form action="{{action_url}}" method="post" class="styled-form">
        <div class="form-group">
            <label for="name">Nome:</label>
            <input type="text" id="name" name="name" value="{{user['name'] if user else ''}}" required>
        </div>

        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" value="{{user['email'] if user else ''}}" required>
        </div>

        <div class="form-group">
            <label for="birthdate">Data de Nascimento:</label>
            <input type="date" id="birthdate" name="birthdate" value="{{user['birthdate'] if user else ''}}" required>
        </div>

        % if not user:
            <div class="form-group">
                <label for="password">Senha:</label>
                <input type="password" id="password" name="password" required>
            </div>
        % end

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar</button>
            <a href="/users" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</section>