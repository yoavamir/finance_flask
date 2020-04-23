from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from utils.Utils import FileUtils
from utils.Consts import FileConsts

split_by_shop_blueprint = Blueprint('split_by_shop', __name__)


@split_by_shop_blueprint.route('/shops_distribution', methods=['GET'])
@cross_origin()
def shops_distribution():
    combined_df = FileUtils().combined_df
    shop_df = combined_df[{FileConsts.SHOP_NAME, FileConsts.TRANSACTION_AMOUNT}]
    shops_and_amount_df = shop_df.groupby('shop_name', as_index=False).sum()
    return jsonify(shops_and_amount_df.values.tolist())

# if __name__ == '__main__':
#     get_split()
