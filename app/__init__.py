import logging
import sys

from flask import Flask
from flask_cors import CORS
from utils.solana_driver import MetaplexAPI
from utils.chronicle_driver import ChronicleDriver
# from flask_sqlalchemy import SQLAlchemy
import redis
from solana.rpc.api import Client


from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

cors = CORS(app)
metaplex_api = MetaplexAPI(json_key_path=Config.PRIVATE_KEY_PATH, api_endpoint=Config.SOLANA_API_ENDPOINT)

solana_client = Client(Config.SOLANA_API_ENDPOINT)

redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB
)

chronicle_driver = ChronicleDriver(base_url=Config.CHRONICLE_BASE_URL, api_key=Config.CHRONICLE_API_KEY)
# db = SQLAlchemy(app=app)

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-%(pathname)s/%(funcName)s: %(message)s')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

root.addHandler(handler)

from app.api import api_bp as api_bp_v1

app.register_blueprint(api_bp_v1, url_prefix='/')

# from app import errors
