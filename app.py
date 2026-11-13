import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import (
    InvalidHeaderError,
    JWTDecodeError,
    NoAuthorizationError,
    RevokedTokenError,
    WrongTokenError,
)

from con_sql import bd
from blocklist import BLOCKLIST
from resources.user import UserRegister, UserLogin, UserLogout
from resources.tarefa import Tarefas, Tarefa
from models.user import UtilizadorModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "mudar_esta_chave_secreta_com_mais_de_32_bytes"

os.makedirs(app.instance_path, exist_ok=True)
bd.init_app(app)
jwt = JWTManager(app)
erros_jwt = (
    InvalidHeaderError,
    JWTDecodeError,
    NoAuthorizationError,
    RevokedTokenError,
    WrongTokenError,
)
api = Api(app, errors={
    erro.__name__: {
        "status": 401,
        "message": "Token JWT inválido, revogado ou em falta.",
    }
    for erro in erros_jwt
})


@jwt.token_in_blocklist_loader
def verificar_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def token_revogado(jwt_header, jwt_payload):
    return {"message": "Token revogado. Inicia sessão novamente."}, 401


api.add_resource(UserRegister, "/registo")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:tarefa_id>")


# Cria as tabelas e um administrador na primeira execução.
with app.app_context():
    bd.create_all()
    admin = UtilizadorModel.query.filter_by(email="admin@api.pt").first()
    if admin is None:
        admin = UtilizadorModel(
            username="admin",
            email="admin@api.pt",
            password="admin123",
            tipo="admin",
        )
        bd.session.add(admin)
        bd.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
