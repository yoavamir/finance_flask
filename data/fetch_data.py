from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from utils.Utils import MaxFileUtils


fetch_data_blueprint = Blueprint('fetch_data', __name__)


@fetch_data_blueprint.route('/fetch_data', methods=['GET'])
@cross_origin()
def get_monthly_shops_by_months():
    file_utils = MaxFileUtils('transaction-details_export_1586955191879.xlsx')
    df = file_utils.file_df
    df = df.rename(columns={'סכום חיוב': 'transaction_amount', 'תאריך עסקה': 'transaction_date',
                            'שם בית העסק': 'shop_name'})[{'transaction_amount', 'transaction_date', 'shop_name'}]
    df['transaction_date'] = df['transaction_date'].apply(lambda x: x[3:])
    df = df.groupby(['transaction_date', 'shop_name'], as_index=False).sum()

    df_abroad = file_utils.abroad_file_df
    df_abroad = df_abroad.rename(
        columns={'סכום חיוב': 'transaction_amount', 'תאריך עסקה': 'transaction_date', 'שם בית העסק': 'shop_name'})[
        {'transaction_amount', 'transaction_date', 'shop_name'}]
    df_abroad['transaction_date'] = df_abroad['transaction_date'].apply(lambda x: x[3:])
    df_abroad = df_abroad.groupby(['transaction_date', 'shop_name'], as_index=False).sum()

    combined_df = df.append(df_abroad)
    combined_df = combined_df.groupby(['transaction_date', 'shop_name'], as_index=False).sum()

    list_values = combined_df.values.tolist()
    list_values.sort(key=lambda x: datetime.strptime(x[0], '%m-%Y'))
    return jsonify(request.args.get('filename'),  list_values)


if __name__ == '__main__':
    get_monthly_shops_by_months()
