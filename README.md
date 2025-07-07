# Projeto Template: POO com Python + Bottle + JSON

Este é um projeto de template educacional voltado para o ensino de **Programação Orientada a Objetos (POO)** do Prof. Lucas Boaventura, Universidade de Brasília (UnB).

Utiliza o microframework **Bottle**. Ideal para uso em disciplinas introdutórias de Engenharia de Software ou Ciência da Computação.

## 💡 Objetivo

Fornecer uma base simples, extensível e didática para construção de aplicações web orientadas a objetos com aplicações WEB em Python, ideal para trabalhos finais ou exercícios práticos.

---

## 🗂 Estrutura de Pastas

```bash 
epf-RedLine/
├── app.py               # Ponto de entrada da aplicação Bottle
├── config.py            # Configurações globais do projeto
├── main.py              # Inicialização da aplicação
├── requirements.txt     # Dependências
├── README.md            # Este arquivo
├── controllers/         # Lógica de controle e rotas
│   ├── auth_controller.py
│   ├── base_controller.py
│   ├── carro_controller.py
│   ├── manutencao_controller.py
│   ├── user_controller.py
│   └── __init__.py
├── models/              # Definição das entidades e dados
│   ├── carro.py
│   ├── manutencao.py
│   ├── manutencaoProgramada.py
│   ├── itemVidaUtil.py
│   └── user.py
├── services/            # Manipulação e persistência de dados
│   └── user_service.py
├── views/               # Templates HTML Bottle
│   ├── layout.tpl
│   ├── login.tpl
│   ├── signup.tpl
│   ├── carros.tpl
│   ├── cadastro_carro.tpl
│   ├── manutencoes.tpl
│   ├── cadastro_manutencao.tpl
│   └── users.tpl
├── data/                # Dados persistidos (JSON)
│   ├── users.json
│   ├── carros.json
│   └── manutencoes.json
├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── img/
└── test.py              # Script de testes ou inicialização auxiliar

```
---

## 📁 Descrição das Pastas

### `controllers/`
Responsáveis pelas rotas e lógica de fluxo da aplicação:

- **auth_controller.py** – Login e cadastro.
- **carro_controller.py** – CRUD de carros.
- **manutencao_controller.py** – CRUD de manutenções.
- **user_controller.py** – Gerenciamento de usuários.

### `models/`
Definem as entidades e estruturas de dados:

- `User`: dados de usuário (login e informações pessoais)
- `Carro`: dados de veículos
- `Manutencao`: serviços realizados nos veículos
- Outros modelos auxiliares

### `services/`
Responsáveis pela **persistência** e manipulação de dados JSON:
- `user_service.py`: operações de usuário (`create_account`, `authenticate`, etc.)
### `views/`
Templates HTML (Bottle Templating Language) usados como páginas da aplicação:

- `login.tpl`, `signup.tpl`: telas de autenticação
- `carros.tpl`: listagem de carros
- `manutencoes.tpl`: listagem de manutenções
- `layout.tpl`: layout base reutilizável

---

### `static/`
Arquivos estáticos como:
- `css/style.css`: estilos básicos.
- `js/main.js`: scripts JS opcionais.
- `img/BottleLogo.png`: exemplo de imagem.

### `data/`
Arquivos JSON que simulam o banco de dados:

- `users.json`
- `carros.json
- `manutencoes.json`
---

---

## ▶️ Como Executar

1. Crie o ambiente virtual na pasta fora do seu projeto:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

2. Entre dentro do seu projeto criado a partir do template e instale as dependências:
```bash
pip install -r requirements.txt
```

3. Rode a aplicação:
```bash
python main.py
```

4. Accese sua aplicação no navegador em: [http://localhost:8080](http://localhost:8080)

---

## ✍️ Personalização
Para adicionar novos modelos (ex: Atividades):

1. Crie a classe no diretório **models/**.

2. Crie o service correspondente para manipulação do JSON.

3. Crie o controller com as rotas.

4. Crie as views .tpl associadas.

---

## 🧠 Autor e Licença
Projeto desenvolvido como template didático para disciplinas de Programação Orientada a Objetos, baseado no [BMVC](https://github.com/hgmachine/bmvc_start_from_this).
Você pode reutilizar, modificar e compartilhar livremente.
# epf-RedLine
