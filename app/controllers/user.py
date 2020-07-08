from flask import Blueprint, request, jsonify

from app.helpers.user import get_activation_code, activate_account

app = Blueprint("user", __name__, url_prefix="")


@app.route("/api/users/code", methods=['GET'])
def user_get_activation_code():
    # needs ?email=valid_email@address as query parameter
    email_address = request.args.get('email')
    if not email_address:
        return jsonify({"msg": "Email query parameter required."}), 400
    response, status_code = get_activation_code(email_address)
    return jsonify({"msg": response}), status_code


@app.route("/api/users/activation", methods=['PUT'])
def user_activate_account():
    #expects:
    # {
    #   "username": email
    #   "password": in base64
    #   "activation_code":
    # }
    activation_request = request.json
    response, status_code = activate_account(activation_request)
    return jsonify({"msg": response}), status_code

