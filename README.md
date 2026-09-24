# 🛒 E-Commerce API

<p align="center">
  <img src="https://shields.io" alt="Python">
  <img src="https://shields.io" alt="FastAPI">
  <img src="https://shields.io" alt="SQLAlchemy">
  <img src="https://shields.io" alt="Pydantic">
</p>

Uma API REST resiliente e performática para sistemas de e-commerce, desenvolvida utilizando as melhores práticas do ecossistema Python. A aplicação gerencia fluxos essenciais de uma loja virtual, incluindo o ciclo de vida de produtos, controle de estoque, contas de usuários e gerenciamento de carrinhos.

---

## 🚧 Status do Projeto

> **⚠️ WORK IN PROGRESS (Em Desenvolvimento):** Esta API está sendo ativamente construída e refinada. Funcionalidades de segurança (autenticação JWT), integrações de pagamento e relatórios avançados de vendas estão na esteira de desenvolvimento.

---

## 🛠️ Tecnologias Utilizadas

* **[Python](https://python.org)** — Linguagem base de alta produtividade.
* **[FastAPI](https://tiangolo.com)** — Framework web moderno e de alta performance para construção de APIs.
* **[SQLAlchemy](https://sqlalchemy.org)** — ORM robusto para mapeamento e manipulação de banco de dados SQL de forma pythônica.
* **[Pydantic](https://pydantic.dev)** — Validação de dados de entrada e serialização de respostas em tempo de execução de maneira ultra veloz.

---

## 🚀 Funcionalidades & Roadmap

Abaixo está o mapeamento dos módulos da API e o progresso atual do desenvolvimento:

- [x] Configuração da infraestrutura básica da aplicação (FastAPI + SQLAlchemy)
- [x] Modelagem do Banco de Dados estruturado para E-commerce
- [/] **Módulo de Produtos & Categorias** (Em refinamento de CRUD)
- [ ] **Módulo de Autenticação** (Implementação planejada de JWT & Hashes de segurança)
- [ ] **Módulo de Carrinho & Pedidos** (Lógica de compras e controle transacional de estoque)
- [ ] **Módulo de Pagamentos** (Simulação de integração com Gateway de pagamento)

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o **Python 3.10 ou superior** instalado na sua máquina.

### 1. Clonar o Repositório
```bash
git clone https://github.com
cd ecommerce_api
```

### 2. Criar e Ativar o Ambiente Virtual (Virtualenv)
No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
No Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar as Dependências
```bash
pip install -r requeriments.txt
```

### 4. Inicializar o Servidor
*(Ajuste o comando abaixo caso seu arquivo principal de entrada no diretório `app` utilize outro nome como `main.py`)*
```bash
uvicorn app.main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`.

---

## 📖 Documentação da API (Interactive Swagger UI)

Uma das grandes vantagens deste ecossistema é a documentação viva gerada automaticamente. Com o servidor rodando, você pode acessar e testar todos os endpoints disponíveis diretamente pelo navegador:

* **Swagger UI:** `http://127.0.0`
* **Redoc:** `http://127.0.0`

---

## ✒️ Autor

* **Lucas** - [Lucas0709-glitch](https://github.com/Lucas0709-glitch)
