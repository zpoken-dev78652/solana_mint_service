from flask import jsonify
from flask import request

from app.api import api_bp
from app.services import token_service


@api_bp.route('/nft/contract/status', methods=['GET'])
def get_contract_status():
    ...


@api_bp.route('/nft/contract/mint/token', methods=['POST'])
def mint_new_token():
    data = request.json
    ...


@api_bp.route('/nft/contract/token/<id>', methods=['GET'])
def get_token_info():
    ...


@api_bp.route('/nft/contract/token/<id>/owner', methods=['GET'])
def get_token_owner(id):
    ...

