from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)

    # 注册所有模型（确保 migrate 能发现）
    from models.user import User
    from models.product import Product
    from models.inventory import Inventory
    from models.supplier import Supplier
    from models.inbound import InboundOrder
    from models.outbound import OutboundOrder
    from models.stocktake import StocktakeOrder
    from models.log import OperationLog

    # 注册蓝图
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.inventory import inventory_bp
    from routes.inbound import inbound_bp
    from routes.outbound import outbound_bp
    from routes.stocktake import stocktake_bp
    from routes.suppliers import suppliers_bp
    from routes.stats import stats_bp
    from routes.logs import logs_bp

    app.register_blueprint(auth_bp,      url_prefix='/api/v1/auth')
    app.register_blueprint(products_bp,  url_prefix='/api/v1/products')
    app.register_blueprint(inventory_bp, url_prefix='/api/v1/inventory')
    app.register_blueprint(inbound_bp,   url_prefix='/api/v1/inbound')
    app.register_blueprint(outbound_bp,  url_prefix='/api/v1/outbound')
    app.register_blueprint(stocktake_bp, url_prefix='/api/v1/stocktake')
    app.register_blueprint(suppliers_bp, url_prefix='/api/v1/suppliers')
    app.register_blueprint(stats_bp,     url_prefix='/api/v1/stats')
    app.register_blueprint(logs_bp,      url_prefix='/api/v1/logs')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
