from flask import Flask, abort, send_file
from flask_restx import Api, Resource
from .retiler import Retiler, InvalidInputParamException
import json
import io

app = Flask(__name__)
api = Api(app)

retiler = None


def init():
    global retiler
    config_path = "config.json"
    config = None
    with open(config_path, "r") as fin:
        config = json.load(fin)
    retiler = Retiler(config)


@api.route('/retile/<string:provider_name>/<int(signed=True):level>/<int(signed=True):resolution>/<int(signed=True):z>/'
           '<int(signed=True):x>/<int(signed=True):y>.png')
class GetRetile(Resource):
    def get(self, provider_name, level, resolution, z, x, y):
        try:
            res_img = retiler.retile(provider_name, level, resolution, z, x, y)
            buf = io.BytesIO()
            res_img.save(buf, format='PNG')
            buf.seek(0)
            byte_im = buf.getvalue()
            return send_file(buf, mimetype="image/png")
        except InvalidInputParamException as exc:
            abort(422, str(exc))
        except Exception as exc:
            abort(500, str(exc))


if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0', port=8080)
