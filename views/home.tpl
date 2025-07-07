<h2>Bem-vindo, {{user.email}}!</h2>
<p>Data de nascimento: {{user.birthdate}}</p>

<ul>
    <li><a href="/carros/novo">Cadastrar novo carro</a></li>
    <li><a href="/manutencoes/novo">Adiconar Manutenção</a></li>
        <li><a href="/manutencoes/novo">Ver manutencoes</a></li>
    <li><a href="/carros/{{user.email}}">Ver meus carros</a></li>
    <li><a href="/logout">Sair</a></li>
</ul>
