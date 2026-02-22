"""
pytest 全局 fixtures
使用 SQLite 内存数据库，测试间完全隔离
"""
import pytest
from app import create_app
from models import db as _db
from models.user import User
from models.product import Product
from models.supplier import Supplier


@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret',
    })
    with app.app_context():
        _db.create_all()
        _seed()
        yield app
        _db.drop_all()


def _seed():
    for username, password, role in [
        ('admin',     'admin123',     'admin'),
        ('warehouse', 'warehouse123', 'warehouse'),
        ('purchaser', 'purchaser123', 'purchaser'),
    ]:
        u = User(username=username, role=role)
        u.set_password(password)
        _db.session.add(u)

    s = Supplier(name='测试供应商', contact='张三', phone='13800000000',
                 category='饮料', status='active')
    _db.session.add(s)

    p = Product(name='测试商品', category='饮料', spec='500ml',
                unit='瓶', stock_min=10, stock_max=500)
    _db.session.add(p)
    _db.session.commit()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def _login(client, username, password):
    res = client.post('/api/v1/auth/login',
                      json={'username': username, 'password': password})
    return res.get_json()['token']


@pytest.fixture(scope='session')
def admin_token(client):
    return _login(client, 'admin', 'admin123')


@pytest.fixture(scope='session')
def warehouse_token(client):
    return _login(client, 'warehouse', 'warehouse123')


@pytest.fixture(scope='session')
def purchaser_token(client):
    return _login(client, 'purchaser', 'purchaser123')
