from flask import Flask, jsonify, abort, request
from modelo import db, Monitoreo
import json
from flask_restplus import Resource, Api
from flask_restplus import fields
from commands import get_all_checks,get_last_cpu_checks


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/monitoreo.db'
db.init_app(app)

api = Api(app,version='V1.0', title='API', description='Emmanuel Parcial 2')
ns = api.namespace('', description='checks de monitoreo')


@ns.route('/checks')
class ChecksCollection(Resource):

    @api.response(200, 'todos los checks')
    def get(self):
        """ retorna todos los checks """
        list = {}
        list["checks: "] = get_all_checks()
        return json.dumps(list), 200

    @api.response(404, 'HTTP 404 NOT FOUND')
    def post(self):
        return 'HTTP 404 NOT FOUND', 404

    @api.response(404, 'HTTP 404 NOT FOUND')
    def put(self):
        return 'HTTP 404 NOT FOUND', 404

    @api.response(404, 'HTTP 404 NOT FOUND')
    def delete(self):
        return 'HTTP 404 NOT FOUND', 404


@ns.route('/checks/cpu/history')
class ChecksByHistory(Resource):

    @api.response(200, 'Obtiene los ultimos n checks registrados')
    @api.doc(params={'size': 'el numero de registros a consultar'})
    def get(self):

        size = request.args.get("size")
        list = {}
        list["cpu: "] = get_last_cpu_checks(size)
        return json.dumps(list), 200

    @api.response(404, 'HTTP 404 NOT FOUND')
    def post(self):
        return 'HTTP 404 NOT FOUND', 404

    @api.response(404, 'HTTP 404 NOT FOUND')
    def put(self):
        return 'HTTP 404 NOT FOUND', 404

    @api.response(404, 'HTTP 404 NOT FOUND')
    def delete(self):
        return 'HTTP 404 NOT FOUND', 404


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug='True')
