from app.main import app
from parsers.amout import amount_blueprint
from parsers.split_by_shop import split_by_shop_blueprint
from parsers.spent_by_day import spent_by_day_blueprint
from parsers.category_distribution import category_distribution_blueprint
from parsers.time_range import time_range_blueprint
from parsers.spent_by_month import spent_by_month_blueprint
from parsers.shops_by_months import shops_by_months_blueprint

if __name__ == "__main__":
    app.register_blueprint(amount_blueprint)
    app.register_blueprint(split_by_shop_blueprint)
    app.register_blueprint(spent_by_day_blueprint)
    app.register_blueprint(category_distribution_blueprint)
    app.register_blueprint(time_range_blueprint)
    app.register_blueprint(spent_by_month_blueprint)
    app.register_blueprint(shops_by_months_blueprint)
    app.run(port=5000)
