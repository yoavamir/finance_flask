from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pandas as pd
import tempfile
import os

category_distribution_blueprint = Blueprint('category_distribution', __name__)


@category_distribution_blueprint.route('/category_distribution', methods=['GET'])
@cross_origin()
def category_distribution():
    file_path = os.path.join(tempfile.gettempdir(), request.args.get('filename'))
    df = pd.read_excel(file_path, skiprows=3)
    category_and_amount_df = df[['קטגוריה', 'סכום חיוב']].rename(
        columns={'קטגוריה': 'category_name', 'סכום חיוב': 'amount'})
    category_and_amount_df = category_and_amount_df.groupby('category_name', as_index=False).sum()
    return jsonify(request.args.get('filename'), category_and_amount_df.values.tolist())

