from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pandas as pd
import tempfile
import os


spent_by_day_blueprint = Blueprint('spent_by_day', __name__)


@spent_by_day_blueprint.route('/spent_by_day', methods=['GET'])
@cross_origin()
def get_amount():
    file_path = os.path.join(tempfile.gettempdir(), request.args.get('filename'))
    df = pd.read_excel(file_path, skiprows=3)
    df = df.rename(columns={'סכום חיוב': 'transaction_amount', 'תאריך עסקה': 'transaction_date'})
    date_and_amount = df[{'transaction_date', 'transaction_amount'}].groupby('transaction_date', as_index=False).sum()
    return jsonify(request.args.get('filename'),  date_and_amount.values.tolist())
