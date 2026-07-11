from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
db.init_app(app)

class Usuarios(db.Model):
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
   
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')