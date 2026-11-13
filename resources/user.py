from hmac import compare_digest

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

from blocklist import BLOCKLIST
from models.user import UtilizadorModel


class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="username obrigatório")
    argumentos.add_argument("email", type=str, required=True, help="email obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="password obrigatória")

    def post(self):
        dados = UserRegister.argumentos.parse_args()
        if UtilizadorModel.find_by_email(dados["email"]):
            return {"message": "Este email já está registado."}, 400
        if UtilizadorModel.find_by_username(dados["username"]):
            return {"message": "Este username já está registado."}, 400

        utilizador = UtilizadorModel(
            username=dados["username"],
            email=dados["email"],
            password=dados["password"],
            tipo="utilizador",
        )
        utilizador.save()
        return utilizador.json(), 201


class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("email", type=str, required=True, help="email obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="password obrigatória")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        utilizador = UtilizadorModel.find_by_email(dados["email"])

        if utilizador and compare_digest(utilizador.password, dados["password"]):
            token = create_access_token(
                identity=str(utilizador.id),
                additional_claims={"tipo": utilizador.tipo},
            )
            return {"access_token": token}, 200
        return {"message": "Email ou password inválidos."}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        BLOCKLIST.add(get_jwt()["jti"])
        return {"message": "Sessão terminada."}, 200
