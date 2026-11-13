from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from con_sql import bd
from models.tarefa import TarefaModel

ESTADOS = ["Pendente", "Em curso", "Concluída"]


class Tarefas(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="titulo obrigatório")
    argumentos.add_argument("descricao", type=str, required=True, help="descricao obrigatória")
    argumentos.add_argument("estado", type=str, required=True, help="estado obrigatório")

    @jwt_required()
    def get(self):
        utilizador_id = int(get_jwt_identity())
        if get_jwt().get("tipo") == "admin":
            tarefas = TarefaModel.query.all()
        else:
            tarefas = TarefaModel.query.filter_by(utilizador_id=utilizador_id).all()
        return {"tarefas": [tarefa.json() for tarefa in tarefas]}, 200

    @jwt_required()
    def post(self):
        dados = Tarefas.argumentos.parse_args()
        if dados["estado"] not in ESTADOS:
            return {"message": "Estado inválido. Usa Pendente, Em curso ou Concluída."}, 400

        tarefa = TarefaModel(
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            estado=dados["estado"],
            utilizador_id=int(get_jwt_identity()),
        )
        bd.session.add(tarefa)
        bd.session.commit()
        return tarefa.json(), 201


class Tarefa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="titulo obrigatório")
    argumentos.add_argument("descricao", type=str, required=True, help="descricao obrigatória")
    argumentos.add_argument("estado", type=str, required=True, help="estado obrigatório")

    def utilizador_tem_acesso(self, tarefa):
        utilizador_id = int(get_jwt_identity())
        return get_jwt().get("tipo") == "admin" or tarefa.utilizador_id == utilizador_id

    @jwt_required()
    def get(self, tarefa_id):
        tarefa = TarefaModel.find_by_id(tarefa_id)
        if tarefa is None:
            return {"message": "Tarefa não encontrada."}, 404
        if not self.utilizador_tem_acesso(tarefa):
            return {"message": "Não tens permissão para consultar esta tarefa."}, 403
        return tarefa.json(), 200

    @jwt_required()
    def put(self, tarefa_id):
        tarefa = TarefaModel.find_by_id(tarefa_id)
        if tarefa is None:
            return {"message": "Tarefa não encontrada."}, 404
        if not self.utilizador_tem_acesso(tarefa):
            return {"message": "Não tens permissão para alterar esta tarefa."}, 403

        dados = Tarefa.argumentos.parse_args()
        if dados["estado"] not in ESTADOS:
            return {"message": "Estado inválido. Usa Pendente, Em curso ou Concluída."}, 400

        tarefa.titulo = dados["titulo"]
        tarefa.descricao = dados["descricao"]
        tarefa.estado = dados["estado"]
        bd.session.commit()
        return tarefa.json(), 200

    @jwt_required()
    def delete(self, tarefa_id):
        tarefa = TarefaModel.find_by_id(tarefa_id)
        if tarefa is None:
            return {"message": "Tarefa não encontrada."}, 404
        if not self.utilizador_tem_acesso(tarefa):
            return {"message": "Não tens permissão para eliminar esta tarefa."}, 403

        tarefa.delete()
        return {"message": "Tarefa eliminada."}, 200
