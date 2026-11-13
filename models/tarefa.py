from con_sql import bd


class TarefaModel(bd.Model):
    __tablename__ = "tarefa"

    id = bd.Column(bd.Integer, primary_key=True)
    titulo = bd.Column(bd.String(100), nullable=False)
    descricao = bd.Column(bd.Text, nullable=False)
    estado = bd.Column(bd.String(20), nullable=False, default="Pendente")
    utilizador_id = bd.Column(bd.Integer, bd.ForeignKey("utilizador.id"), nullable=False)

    utilizador = bd.relationship("UtilizadorModel", back_populates="tarefas")

    def __init__(self, titulo, descricao, estado, utilizador_id):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        self.utilizador_id = utilizador_id

    def json(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "estado": self.estado,
            "utilizador_id": self.utilizador_id,
        }

    @classmethod
    def find_by_id(cls, tarefa_id):
        return cls.query.filter_by(id=tarefa_id).first()

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()
