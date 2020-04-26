from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from parsers.amout import amount_blueprint
from parsers.split_by_shop import split_by_shop_blueprint
from parsers.spent_by_day import spent_by_day_blueprint
from parsers.category_distribution import category_distribution_blueprint
from parsers.time_range import time_range_blueprint
from parsers.spent_by_month import spent_by_month_blueprint
from parsers.shops_by_months import shops_by_months_blueprint
from utils.Consts import FileConsts
from utils.Utils import MaxFileUtils, FileUtils
from files.FileList import FileList

import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(amount_blueprint)
app.register_blueprint(split_by_shop_blueprint)
app.register_blueprint(spent_by_day_blueprint)
app.register_blueprint(category_distribution_blueprint)
app.register_blueprint(time_range_blueprint)
app.register_blueprint(spent_by_month_blueprint)
app.register_blueprint(shops_by_months_blueprint)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/upload_file', methods=['POST'])
@cross_origin()
def upload_file():
    print(request.form)
    f = request.files['file']
    file_list = FileList()
    file_list.append_to_list(f.filename)
    return jsonify(file_list.saved_files)


@app.route('/init_expense_data', methods=['POST'])
@cross_origin()
def init_expense_data():
    file_utils = FileUtils()
    months = file_utils.get_months_from_file()
    return jsonify(months)


@app.route('/init_data', methods=['GET'])
@cross_origin()
def init_data():
    file_utils = FileUtils()
    months = file_utils.get_months_from_file()
    shops = file_utils.get_shops_from_file()
    return jsonify(months, shops)


@app.route('/get_files', methods=['GET'])
@cross_origin()
def get_files():
    files_list = FileList()
    return jsonify(files_list.saved_files)


# if __name__ == '__main__':
#     app.register_blueprint(amount_blueprint)
#     app.register_blueprint(split_by_shop_blueprint)
#     app.register_blueprint(spent_by_day_blueprint)
#     app.register_blueprint(category_distribution_blueprint)
#     app.register_blueprint(time_range_blueprint)
#     app.register_blueprint(spent_by_month_blueprint)
#     app.register_blueprint(shops_by_months_blueprint)
#     app.run(port=5000)
