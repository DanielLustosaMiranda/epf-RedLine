%rebase('layout', title='Painel Principal')

<section class="dashboard-section">
    <div class="section-header">
        <h2>Bem-vindo(a), {{user['name']}}!</h2>
        <a href="/logout" class="btn btn-secondary">Sair</a>
    </div>

    <p><b>Email:</b> {{user['email']}}</p>
    <p><b>Data de nascimento:</b> {{user['birthdate']}}</p>

    <hr>
    <h3>Ações Rápidas</h3>
    <ul>
        <li><a href="/carros/add">Cadastrar novo carro</a></li>
        <li><a href="/carros">Ver meus carros</a></li>
        <li><a href="/users/edit/{{user['id']}}">Editar meu perfil</a></li>
    </ul>
</section>