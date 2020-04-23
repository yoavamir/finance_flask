from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from utils.Utils import FileUtils


amount_blueprint = Blueprint('amount_blueprint', __name__)


@amount_blueprint.route('/total_amount', methods=['GET'])
@cross_origin()
def get_amount():
    file_utils = FileUtils()
    amount = file_utils.combined_df.transaction_amount
    return jsonify(amount.sum())
