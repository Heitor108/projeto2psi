from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import LoginManager, UserMixin, login_required, login_user

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

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario_existente = db.session.execute(db.select(Usuarios).filter_by(email=request.form.get('email'))).scalar()

        novo_usuario = Usuarios(
        nome = request.form.get('nome'),
        email = request.form.get('email'),
        senha = request.form.get('senha')
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

        if usuario and usuario.nome == nome and usuario.senha == senha:
            login_user(usuario)

        else:
            return redirect(url_for('login'))

        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    pass