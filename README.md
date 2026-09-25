# 🛒 E-commerce API

API REST para gerenciamento de um sistema de e-commerce, desenvolvida com **Python, FastAPI e SQLAlchemy**.

> ⚠️ **Status do projeto: Em desenvolvimento**
>
> Esta API ainda está **incompleta**. Algumas funcionalidades previstas na arquitetura do projeto ainda serão implementadas nas próximas etapas. O projeto está sendo desenvolvido de forma incremental, com novas funcionalidades sendo adicionadas e testadas ao longo do desenvolvimento.

---

## 🚀 Tecnologias

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **SQLite**
* **Pydantic**
* **Uvicorn**
* **Swagger / OpenAPI**
* **Git / GitHub**

---

## 📌 Funcionalidades atuais

Atualmente, a API possui funcionalidades relacionadas ao gerenciamento de usuários e produtos.

### 👤 Usuários

* Cadastro de usuários
* Persistência dos dados no banco de dados
* Estrutura preparada para futuras funcionalidades de autenticação

### 📦 Produtos

* Cadastro de produtos
* Listagem de produtos
* Busca de produto por ID
* Atualização de produtos
* Exclusão de produtos
* Controle básico de estoque
* Validação dos dados recebidos
* Tratamento de produto não encontrado (`404`)

### 📚 Documentação

A API possui documentação automática através do **Swagger UI**, disponibilizada pelo FastAPI.

Após iniciar a aplicação, ela pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

---

## 🏗️ Funcionalidades planejadas

O projeto ainda está em desenvolvimento e possui funcionalidades planejadas para as próximas etapas.

### 🛍️ Pedidos

Será implementado um sistema de pedidos contendo:

* Criação de pedidos
* Associação entre usuário e pedido
* Adição de produtos ao pedido
* Quantidade de cada produto
* Preço do produto no momento da compra
* Cálculo automático do valor total
* Consulta dos pedidos de um usuário
* Status do pedido

### 📦 Controle de estoque

Serão implementadas regras de negócio para o gerenciamento do estoque, incluindo:

* Verificação de disponibilidade antes da compra
* Redução automática do estoque após adicionar produtos ao pedido
* Impedimento de pedidos com quantidade superior ao estoque disponível

### 🔐 Autenticação

Futuramente será implementado um sistema de autenticação utilizando:

* Login de usuários
* Senhas armazenadas de forma segura
* JWT
* Proteção de endpoints
* Autorização baseada no usuário autenticado

### 🧪 Testes

Serão adicionados testes automatizados para validar:

* Usuários
* Produtos
* Pedidos
* Itens dos pedidos
* Regras de estoque
* Autenticação

### 🐳 Docker

Também está planejada a configuração do projeto para execução utilizando **Docker**, facilitando a instalação e execução da aplicação em diferentes ambientes.

---

## 🗂️ Estrutura do projeto

```text
ecommerce_api/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── order_item.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── order_item.py
│   │
│   ├── crud/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── order_item.py
│   │
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── user.py
│   │           ├── product.py
│   │           ├── order.py
│   │           └── auth.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   └── tests/
│       ├── test_user.py
│       ├── test_product.py
│       └── test_order.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

> **Observação:** algumas partes da estrutura já estão preparadas para funcionalidades que ainda serão implementadas.

---

## 🗃️ Modelo de dados

A arquitetura do projeto foi planejada em torno das seguintes entidades:

```text
User
 │
 │ 1:N
 ▼
Order
 │
 │ 1:N
 ▼
OrderItem
 ▲
 │ N:1
 │
Product
```

### User

Representa os usuários cadastrados na plataforma.

Principais atributos:

* `id`
* `nome`
* `email`
* `senha_hash`
* `criado_em`

### Product

Representa os produtos disponíveis no catálogo.

Principais atributos:

* `id`
* `nome`
* `descricao`
* `preco`
* `estoque`
* `criado_em`

### Order

Representa os pedidos realizados pelos usuários.

Principais atributos:

* `id`
* `usuario_id`
* `status`
* `total`
* `criado_em`

### OrderItem

Representa os produtos pertencentes a um pedido.

Principais atributos:

* `id`
* `pedido_id`
* `produto_id`
* `quantidade`
* `preco_unitario`

O `preco_unitario` será armazenado no momento da compra para preservar o valor praticado quando o pedido foi realizado, independentemente de futuras alterações no preço do produto.

---

## ⚙️ Regras de negócio planejadas

Entre as principais regras previstas para o sistema estão:

1. Um pedido pertence a um usuário.
2. Um pedido pode possuir vários itens.
3. Um produto pode aparecer em vários pedidos.
4. Um produto não poderá ser adicionado ao pedido caso não exista estoque suficiente.
5. Ao adicionar um produto ao pedido, sua quantidade em estoque será reduzida.
6. O valor total do pedido será calculado com base na quantidade e no preço unitário de cada item.
7. O preço registrado no `OrderItem` representará o preço praticado no momento da compra.

---

## ▶️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Lucas0709-glitch/ecommerce_api.git
```

Entre na pasta:

```bash
cd ecommerce_api
```

### 2. Crie o ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

---

## 📖 Documentação da API

Com a aplicação em execução, a documentação interativa pode ser acessada através do Swagger:

```text
http://127.0.0.1:8000/docs
```

Também é possível acessar a documentação alternativa do FastAPI:

```text
http://127.0.0.1:8000/redoc
```

---

## 🛣️ Roadmap

### Concluído

* [x] Estrutura inicial do projeto
* [x] Configuração do FastAPI
* [x] Conexão com banco de dados
* [x] Modelagem inicial de usuários
* [x] Cadastro de usuários
* [x] Modelagem de produtos
* [x] CRUD de produtos
* [x] Validação de dados
* [x] Tratamento de erros básicos
* [x] Documentação inicial com Swagger
* [x] Versionamento com Git
* [x] Repositório no GitHub

### Em desenvolvimento

* [ ] Pedidos
* [ ] Itens dos pedidos
* [ ] Relacionamentos entre entidades
* [ ] Regras de estoque
* [ ] Cálculo automático do total dos pedidos

### Planejado

* [ ] Autenticação
* [ ] JWT
* [ ] Proteção de endpoints
* [ ] Testes automatizados
* [ ] Docker
* [ ] Melhorias de documentação
* [ ] Refinamento da arquitetura

---

## 🎯 Objetivo do projeto

Este projeto está sendo desenvolvido como uma aplicação prática para aprofundar conhecimentos em **desenvolvimento Backend**, especialmente em:

* Desenvolvimento de APIs REST
* Python
* FastAPI
* SQLAlchemy
* Bancos de dados relacionais
* Modelagem de dados
* Autenticação
* Regras de negócio
* Testes automatizados
* Docker
* Documentação de APIs

O objetivo é evoluir gradualmente a aplicação, adicionando funcionalidades de acordo com a arquitetura planejada e utilizando boas práticas de desenvolvimento.

---

## 📄 Licença

Este projeto está sob a licença **MIT**.

Consulte o arquivo `LICENSE` para mais informações.
