from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, login_manager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.secret_key = 'segredo'
db.init_app(app)
login_manager.init_app(app)

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)

class Livros(db.Model):
   __tablename__ = 'livros'

   id: Mapped[int] = mapped_column(primary_key=True)
   titulo: Mapped[str] = mapped_column(nullable=False, unique=True)
   autor: Mapped[str] = mapped_column(nullable=False)
   ano: Mapped[int] = mapped_column(nullable=False)
   categoria: Mapped[str] = mapped_column(nullable=False)
   quantidade: Mapped[int] = mapped_column(nullable=False)
   id_usuario: Mapped[int] = mapped_column(ForeignKey('usuarios.id'))

class Emprestimos(db.Model):
   __tablename__ = 'emprestimos'

   id: Mapped[int] = mapped_column(primary_key=True)
   status: Mapped[str] = mapped_column(nullable=False)
   id_usuario: Mapped[int] = mapped_column(ForeignKey('usuarios.id'))
   id_livro: Mapped[int] = mapped_column(ForeignKey('livros.id'))
   
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuarios, int(user_id))

login_manager.login_view = 'cadastro'

login_manager.login_message = 'Por favor realize o login para acessar essa página'

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    usuario = current_user

    livros = db.session.execute(db.select(Livros).filter_by(id_usuario=usuario.id)).scalars()
    emprestimos = db.session.execute(db.select(Emprestimos).filter_by(id_usuario=usuario.id)).scalars()

    return render_template('index.html', usuario=usuario, livros=livros, emprestimos=emprestimos)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario_existente = db.session.execute(db.select(Usuarios).filter_by(email=request.form.get('email'))).scalar()

        senha = request.form.get('senha')

        novo_usuario = Usuarios(
        nome = request.form.get('nome'),
        email = request.form.get('email'),
        senha = generate_password_hash(senha)
        )
        
        if usuario_existente:
            return redirect(url_for('cadastro'))

        else:
            db.session.add(novo_usuario)
            db.session.commit()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = db.session.execute(db.select(Usuarios).filter_by(email=request.form.get('email'))).scalar()

        nome = request.form.get('nome')
        senha = request.form.get('senha')

        if usuario and usuario.nome == nome and check_password_hash(usuario.senha, senha):
            login_user(usuario)

        else:
            return redirect(url_for('login'))

        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('cadastro'))

@app.route("/livros")
@login_required
def livros():
    titulo = request.args.get('titulo')
    categoria = request.args.get('categoria')
    autor = request.args.get('autor')
    ano = request.args.get('ano')

    consulta = db.select(Livros)

    if titulo:
        consulta = consulta.where(Livros.titulo.contains(titulo))

    if categoria:
        consulta = consulta.where(Livros.categoria.contains(categoria))

    if autor:
        consulta = consulta.where(Livros.autor.contains(autor))

    if ano:
        consulta = consulta.where(Livros.ano == int(ano))

    livros = db.session.execute(consulta).scalars()
    emprestimos = db.session.execute(
        db.select(Emprestimos).filter_by(id_usuario=current_user.id)
    ).scalars().all()

    return render_template(
        "livros.html",
        livros=livros,
        emprestimos=emprestimos
    )

@app.route('/livro/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    if request.method == 'POST':
        titulo = request.form.get('titulo')

        livro = db.session.execute(
            db.select(Livros).where(
                Livros.titulo == titulo,
                Livros.id_usuario == current_user.id
            )
        ).scalar()

        if livro:
            livro.quantidade += 1
        else:
            livro = Livros(
                titulo=titulo,
                autor=request.form.get('autor'),
                ano=request.form.get('ano'),
                categoria=request.form.get('categoria'),
                quantidade=1,
                id_usuario=current_user.id
            )
            db.session.add(livro)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('novo_livro.html')

@app.route('/livro/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    livro = db.session.get(Livros, id)

    if not livro or livro.id_usuario != current_user.id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        livro.titulo = request.form.get('titulo')
        livro.autor = request.form.get('autor')
        livro.ano = request.form.get('ano')
        livro.categoria = request.form.get('categoria')

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('editar.html', livro=livro)

@app.route('/livro/excluir/<int:id>')
@login_required
def excluir(id):
    livro = db.session.get(Livros, id)

    if livro.quantidade > 1:
        livro.quantidade -= 1
    else:
        db.session.delete(livro)

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/emprestar/<int:id>')
@login_required
def emprestar(id):
    livro = db.session.get(Livros, id)

    if not livro:
        return redirect(url_for('livros'))

    if livro.id_usuario == current_user.id:
        return redirect(url_for('livros'))

    if livro.quantidade > 0:
        livro.quantidade -= 1

        emprestimo = Emprestimos(
            status='Emprestado',
            id_usuario=current_user.id,
            id_livro=livro.id
        )

        db.session.add(emprestimo)
        db.session.commit()

    return redirect(url_for('livros'))

@app.route('/devolver/<int:id>')
@login_required
def devolver(id):
    emprestimo = db.session.get(Emprestimos, id)

    if not emprestimo:
        return redirect(url_for('index'))

    livro = db.session.get(Livros, emprestimo.id_livro)

    livro.quantidade += 1

    db.session.delete(emprestimo)
    db.session.commit()

    return redirect(url_for('index'))