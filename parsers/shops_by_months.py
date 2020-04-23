from flask import Blueprint, jsonify
from flask_cors import cross_origin
from utils.Utils import FileUtils
from utils.Consts import FileConsts
from datetime import datetime

shops_by_months_blueprint = Blueprint('shops_by_months', __name__)


@shops_by_months_blueprint.route('/shops_by_months', methods=['GET'])
@cross_origin()
def get_monthly_shops_by_months():
    combined_df = FileUtils().combined_df
    grouped = combined_df.groupby([FileConsts.TRANSACTION_DATE, FileConsts.SHOP_NAME], as_index=False)
    summed = grouped.sum()
    list_values = summed.values.tolist()
    list_values.sort(key=lambda x: datetime.strptime(x[0], '%m-%Y'))
    return jsonify(list_values)


if __name__ == '__main__':
    get_monthly_shops_by_months()
