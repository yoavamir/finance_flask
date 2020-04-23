from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from utils import Utils
from utils.Utils import FileUtils
from utils.Consts import FileConsts


spent_by_month_blueprint = Blueprint('spent_by_month', __name__)


@spent_by_month_blueprint.route('/spent_by_month', methods=['GET'])
@cross_origin()
def get_monthly_expenses():
    combined_df = FileUtils().combined_df
    month_df = combined_df[{FileConsts.TRANSACTION_DATE, FileConsts.TRANSACTION_AMOUNT}]
    month_df = month_df.groupby(FileConsts.TRANSACTION_DATE, as_index=False).sum()
    list_values = month_df.values.tolist()
    list_values.sort(key=lambda x: datetime.strptime(x[0], '%m-%Y'))
    return jsonify(list_values)


if __name__ == '__main__':
    get_monthly_expenses()

