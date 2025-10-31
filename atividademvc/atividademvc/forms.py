from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from models import User # Precisamos importar para validações customizadas

class RegistrationForm(FlaskForm):
    """Formulário de Registro de Usuário."""
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')]
    )
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        """Validação customizada para verificar se o nome de usuário já existe."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        """Validação customizada para verificar se o email já existe."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este email já está cadastrado.')


class LoginForm(FlaskForm):
    """Formulário de Login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')


class ProductForm(FlaskForm):
    """Formulário para Adicionar/Editar Produto."""
    name = StringField('Nome do Produto', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Descrição', validators=[Length(max=500)])
    price = FloatField('Preço', validators=[
        DataRequired(), 
        NumberRange(min=0.01, message='O preço deve ser maior que zero.')
    ])
    submit = SubmitField('Salvar Produto')