import os


class Config:
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:6052')
    CHRONICLE_BASE_URL = os.environ.get('CHRONICLE_BASE_URL', 'http://localhost:6052')
    CHRONICLE_API_KEY = os.environ.get('CHRONICLE_API_KEY', 'c8dfece5cc68249206e4690fc4737a8d')

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
    REDIS_DB = int(os.environ.get('REDIS_DB', '0'))

    PRIVATE_KEY_PATH = os.environ.get('PRIVATE_KEY_PATH', "id.json")
    SOLANA_API_ENDPOINT = os.environ.get('SOLANA_API_ENDPOINT', "https://api.devnet.solana.com/")
