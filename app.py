from errors.v1 import handlers as error_handlers
import connexion
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = connexion.FlaskApp(__name__)

app.add_api('openapi.yaml',
            strict_validation=True,
            arguments={'title': 'JAPA'})
CORS(app.app)
app.app.register_blueprint(error_handlers.error_handlers)


limiter = Limiter(

    app=app.app,
    key_func=get_remote_address,
    storage_uri="memory://",
    #storage_uri="redis://redisrocker@localhost:6379/0",
    storage_options={"socket_connect_timeout": 30},
    default_limits=["20 per day", "10 per hour"],
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

