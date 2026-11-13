from con_sql import bd


class UtilizadorModel(bd.Model):
    __tablename__ = "utilizador"

    id = bd.Column(bd.Integer, primary_key=True)
    username = bd.Column(bd.String(40), unique=True, nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    password = bd.Column(bd.String(120), nullable=False)
    tipo = bd.Column(bd.String(20), nullable=False, default="utilizador")

    tarefas = bd.relationship("TarefaModel", back_populates="utilizador")

    def __init__(self, username, email, password, tipo="utilizador"):
        self.username = username
        self.email = email
        self.password = password
        self.tipo = tipo

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "tipo": self.tipo,
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        bd.session.add(self)
        bd.session.commit()
