from flask import Flask
from flask_cors import CORS
from sentry_sdk import init as sentry_init
import config
from database import mongo_client
from log import get_logger
from models.error_handler import error_blueprint
from models.users_handler import users_blueprint
from models.video_handler import video_blueprint

logger = get_logger(__name__)

sentry_init(config.SENTRY_DSN, traces_sample_rate=1.0)

app = Flask(__name__)

CORS(app)

app.register_blueprint(error_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(video_blueprint)

mongo_client.init_app(app, uri=config.MONGO_URI)


@app.route("/")
def home():
    return "the server is up & running"


if __name__ == "__main__":
    logger.info("starting server in local mode")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
