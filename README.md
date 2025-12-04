# Sistema de Gestão de EPIs 👷‍♂️🏗️

Sistema web desenvolvido em Django para o gerenciamento de Equipamentos de Proteção Individual (EPIs) em uma construtora. O objetivo é controlar o estoque, os empréstimos e as devoluções de equipamentos para os colaboradores, garantindo a segurança e o cumprimento das normas regulamentadoras.

## 📋 Funcionalidades

* **Gestão de Colaboradores:** Cadastro, listagem, edição e remoção de funcionários.
* **Gestão de EPIs:** Cadastro de equipamentos com controle de estoque (Total e Disponível), C.A. e validade.
* **Gestão de Usuários:** Controle de acesso ao sistema (Administradores/Técnicos).
* **Controle de Empréstimos:**
    * Registro de saída de EPIs.
    * Baixa automática no estoque ao emprestar.
    * Validação de estoque disponível.
* **Controle de Devoluções:**
    * Registro de retorno do EPI.
    * Reposição automática ao estoque.
* **Histórico:** Visualização de empréstimos ativos e devolvidos.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12+**
* **Django 5.x** (Framework Web)
* **MySQL** (Banco de Dados)
* **HTML/CSS** (Interface e Estilização)
* **Git** (Controle de Versão)

## 🚀 Como rodar o projeto

Siga os passos abaixo para executar o projeto em sua máquina local.

### 1. Pré-requisitos
Certifique-se de ter instalado:
* Python
* MySQL Server (XAMPP, Workbench ou similar)
* Git (opcional)

### 2. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/projeto-epi.git](https://github.com/seu-usuario/projeto-epi.git)
cd projeto_epi

3. Configurar o Ambiente Virtual
É recomendado usar um ambiente virtual para isolar as dependências.

No Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
No Linux/Mac:

Bash

python3 -m venv venv
source venv/bin/activate
4. Instalar Dependências
Bash

pip install -r requirements.txt
5. Configurar o Banco de Dados
Crie um banco de dados no seu MySQL chamado epi_db.

SQL

CREATE DATABASE epi_db CHARACTER SET utf8mb4;
Abra o arquivo projeto_epi/settings.py e configure as credenciais do banco na seção DATABASES (USER e PASSWORD).

6. Aplicar as Migrações
Isso criará as tabelas no seu banco de dados MySQL.

Bash

python manage.py makemigrations
python manage.py migrate
7. Criar um Superusuário (Admin)
Para acessar o sistema, crie o primeiro usuário:

Bash

python manage.py createsuperuser
Siga as instruções para definir usuário e senha.

8. Iniciar o Servidor
Bash

python manage.py runserver
O sistema estará acessível em: http://127.0.0.1:8000/

📂 Estrutura do Projeto
gestao/: App principal contendo a lógica de negócios (Models, Views, Forms).

projeto_epi/: Configurações globais do projeto (Settings, URLs).

static/: Arquivos estáticos (CSS, Imagens, JS).

templates/: Arquivos HTML base e templates do sistema.

👨‍💻 Autores
Projeto desenvolvido pelos alunos do curso de Desenvolvimento de Sistemas