from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import Integer, String, create_engine, ForeignKey
from flask_login import UserMixin


engine = create_engine('sqlite:///app.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=True) # Novo campo
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    # Relacionamento 1:N com Livro
    livros = relationship('Livro', backref='usuario', cascade="all, delete-orphan")

class Livro(Base):
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(engine)