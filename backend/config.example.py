import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smartmart-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'smartmart-jwt-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://用户名:密码@localhost:3306/smartmart_wms'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24小时
