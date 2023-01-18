from errors.v1 import handlers as error_handlers
import connexion
from flask_cors import CORS

app = connexion.FlaskApp(__name__)

app.add_api('openapi.yaml',
            strict_validation=True,
            arguments={'title': 'JAPA'})
CORS(app.app)
app.app.register_blueprint(error_handlers.error_handlers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

