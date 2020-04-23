from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pandas as pd
import tempfile
import os

time_range_blueprint = Blueprint('time_range', __name__)


@time_range_blueprint.route('/time_range', methods=['GET'])
@cross_origin()
def get_file_time_range():
    file_path = os.path.join(tempfile.gettempdir(), request.args.get('filename'))
    dates = pd.read_excel(file_path).loc[1][0]
    split_dates = dates.split('-')
    start_date = '-'.join(split_dates[:3])
    end_date = '-'.join(split_dates[3:])
    return jsonify(request.args.get('filename'), start_date, end_date)
