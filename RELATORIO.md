# Relatório - Projeto 2 PSI: Sistema de Biblioteca Compartilhada

## 1. Equipe Integrante do Projeto

- **Heitor Emanuel Cavalcanti**: Backend e Templates (app.py e HTML)
- **Pedro Henrique Oliveira de Araújo**: Estilização CSS base e relatório (parte descritiva, de 1 até 4.5)
- **Isaac da Costa Barbosa**: CSS responsivo, testes e relatório (parte técnica, de 5 até 12)
- **André Nícolas de Oliveira Santos**: JavaScript, interatividade e correções

---

## 2. Descrição da Proposta

O projeto consiste no desenvolvimento de um **Sistema de Biblioteca Compartilhada** utilizando o framework Flask. A aplicação permite que usuários se cadastrem e façam login para gerenciar livros em uma biblioteca comum.

### Principais Funcionalidades:

- **Gerenciamento de Usuários**: Cadastro, login e logout com autenticação segura
- **Doação de Livros**: Usuários podem doar livros para a biblioteca, informando título, autor, ano e categoria
- **Busca e Filtro**: Sistema de pesquisa de livros com filtros por título, autor, categoria e ano
- **Empréstimo de Livros**: Usuários podem pegar livros emprestados de outros usuários
- **Devolução de Livros**: Controle de empréstimos e devoluções
- **Edição e Exclusão**: Doadores podem editar informações ou remover seus livros

---

## 3. Justificativa

A falta de acesso a livros é um problema enfrentado por muitos estudantes. Muitas vezes, livros caros ou específicos não estão disponíveis nas bibliotecas públicas, ou o acesso é limitado. Um sistema de biblioteca compartilhada entre usuários facilita:

- **Compartilhamento de recursos**: Democratiza o acesso a conhecimento
- **Sustentabilidade**: Reutilização de livros reduz desperdício
- **Comunidade**: Estimula a cooperação entre usuários
- **Economia**: Reduz custos para estudantes adquirirem livros novos

Este projeto serve como prova de conceito para uma solução escalável e prática.

---

## 4. Principais Problemas Técnicos Encontrados e Soluções

### 4.1 Autenticação e Autorização

**Problema**: Garantir que apenas usuários autenticados acessem rotas protegidas e que cada usuário veja apenas seus próprios dados.

**Solução**: 
- Utilização do **Flask-Login** para gerenciar sessões de usuários
- Uso de `@login_required` em rotas sensíveis
- Implementação de verificações de propriedade (ex: apenas o doador pode editar/excluir seus livros)
- Hash de senhas com `werkzeug.security.generate_password_hash` para armazenar senhas de forma segura

### 4.2 Relacionamento entre Entidades

**Problema**: Gerenciar relacionamentos entre Usuários, Livros e Empréstimos mantendo a integridade dos dados.

**Solução**:
- Uso do **SQLAlchemy** com chaves estrangeiras (`ForeignKey`)
- Modelos bem estruturados com tipos mapeados (`Mapped`)
- Validações na aplicação para evitar estados inconsistentes (ex: um usuário não pode emprestar um livro de si mesmo)

### 4.3 Filtro de Dados com Query Parameters

**Problema**: Permitir buscas flexíveis com múltiplos critérios sem criar rotas diferentes para cada combinação.

**Solução**:
- Implementação de filtros dinâmicos usando `request.args.get()`
- Construção incremental de queries SQLAlchemy baseada em parâmetros fornecidos
- Exemplo: `/livros?titulo=Python&categoria=Programação&ano=2020`

### 4.4 Responsividade em Dispositivos Móveis

**Problema**: Aplicação deve ser usável tanto em desktops quanto em celulares e tablets.

**Solução**:
- Media queries CSS para diferentes tamanhos de tela
- Menu hambúrguer (`.nav-toggle`) que aparece em telas pequenas
- Elementos reorganizados para telas pequenas (botões em bloco, inputs 100% width)
- JavaScript para controlar a abertura/fechamento do menu

### 4.5 Confirmação de Ações Críticas

**Problema**: Evitar que usuários acidentalmente deletem livros ou devolvam empréstimos.

**Solução**:
- Uso de `data-confirm` em links que removem dados
- JavaScript que exibe confirmação antes de processar ações destrutivas
- Previne navegação inadvertida com `event.preventDefault()`

---

## 5. Tecnologias Utilizadas

| Tecnologia | Versão | Utilização |
|------------|--------|-----------|
| **Flask** | 3.x | Framework web |
| **Flask-SQLAlchemy** | 3.x | ORM para banco de dados |
| **Flask-Login** | 0.6.x | Gerenciamento de autenticação |
| **SQLite** | - | Banco de dados local |
| **HTML5** | - | Markup de páginas |
| **CSS3** | - | Estilização e responsividade |
| **JavaScript (Vanilla)** | ES6 | Interatividade |
| **Werkzeug** | - | Hash de senhas |

---

## 6. Estrutura do Projeto

```
projeto2psi/
├── app.py                          # Backend com rotas e modelos
├── static/
│   ├── css/
│   │   └── style.css              # Estilos (base + responsivo)
│   └── js/
│       └── script.js              # Interatividade
├── templates/
│   ├── base.html                  # Template base
│   ├── index.html                 # Página inicial (perfil)
│   ├── cadastro.html              # Página de cadastro
│   ├── login.html                 # Página de login
│   ├── livros.html                # Catálogo e busca
│   ├── novo_livro.html            # Formulário de doação
│   └── editar.html                # Edição de livro
├── banco.db                       # Banco de dados SQLite (gerado)
├── requirements.txt               # Dependências
└── RELATORIO.md                   # Este arquivo
```

---

## 7. Rotas Implementadas

| Rota | Método | Descrição | Autenticação |
|------|--------|-----------|--------------|
| `/` | GET | Página inicial (perfil) | Sim |
| `/cadastro` | GET, POST | Cadastro de novo usuário | Não |
| `/login` | GET, POST | Login de usuário | Não |
| `/logout` | GET | Logout de usuário | Sim |
| `/livros` | GET | Catálogo com filtros | Sim |
| `/livro/novo` | GET, POST | Adicionar novo livro | Sim |
| `/livro/editar/<id>` | GET, POST | Editar livro | Sim |
| `/livro/excluir/<id>` | GET | Remover livro | Sim |
| `/emprestar/<id>` | GET | Emprestar livro | Sim |
| `/devolver/<id>` | GET | Devolver empréstimo | Sim |

---

## 8. Modelos de Dados

### Usuarios
```
- id (PrimaryKey)
- nome (String, required)
- email (String, unique, required)
- senha (String, required - hash)
```

### Livros
```
- id (PrimaryKey)
- titulo (String, unique, required)
- autor (String, required)
- ano (Integer, required)
- categoria (String, required)
- quantidade (Integer, required)
- id_usuario (ForeignKey -> Usuarios, required)
```

### Emprestimos
```
- id (PrimaryKey)
- status (String, required)
- id_usuario (ForeignKey -> Usuarios, required)
- id_livro (ForeignKey -> Livros, required)
```

---

## 9. Como Executar o Projeto

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd projeto2psi-main
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute a aplicação
```bash
python app.py
```

5. Acesse `http://localhost:5000` no navegador

---

## 10. Testes Recomendados

- Cadastro com email duplicado (deve rejeitar)
- Login com credenciais inválidas (deve rejeitar)
- Busca com diferentes combinações de filtros
- Empréstimo do próprio livro (deve bloquear)
- Responsividade em diferentes tamanhos de tela

---

## 11. Possíveis Melhorias Futuras

- Validação de entrada mais robusta (sanitização)
- Sistema de avaliações de livros
- Histórico de empréstimos
- Notificações de devolução atrasada
- Upload de imagens dos livros
- Sistema de categorias predefinidas
- Integração com API de livros (Google Books)
- Paginação para grandes listas

---

## 12. Conclusão

O projeto demonstra com sucesso a aplicação de conceitos fundamentais do Flask incluindo roteamento, autenticação, banco de dados e interação com o usuário. A arquitetura segue boas práticas de separação de responsabilidades e oferece uma experiência responsiva em múltiplos dispositivos.

Todos os requisitos do projeto foram atendidos, e a aplicação é funcional e pronta para uso.

---

**Data de Conclusão**: 17 de Julho de 2026  