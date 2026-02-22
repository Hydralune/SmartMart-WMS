"""
数据库初始化脚本
用法: python scripts/init_db.py
- 创建所有数据表
- 写入初始管理员账号
- 写入示例商品、供应商数据
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from models import db
from models.user import User
from models.product import Product
from models.supplier import Supplier

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('[OK] 数据表创建完成')

        _seed_users()
        _seed_suppliers()
        _seed_products()

        db.session.commit()
        print('[OK] 初始数据写入完成')

def _seed_users():
    users = [
        ('admin',     'admin123',     'admin'),
        ('warehouse', 'warehouse123', 'warehouse'),
        ('purchaser', 'purchaser123', 'purchaser'),
    ]
    for username, password, role in users:
        if User.query.filter_by(username=username).first():
            print(f'[SKIP] 用户已存在: {username}')
            continue
        u = User(username=username, role=role)
        u.set_password(password)
        db.session.add(u)
        print(f'[ADD] 用户: {username} ({role})')

def _seed_suppliers():
    suppliers = [
        ('康师傅食品',   '张经理', '13800001111', '方便食品,饮料',   'active'),
        ('农夫山泉',     '李经理', '13800002222', '饮用水,饮料',     'active'),
        ('伊利乳业',     '王经理', '13800003333', '乳制品',          'active'),
        ('百事食品',     '赵经理', '13800004444', '零食,饮料',       'active'),
    ]
    for name, contact, phone, category, status in suppliers:
        if Supplier.query.filter_by(name=name).first():
            print(f'[SKIP] 供应商已存在: {name}')
            continue
        s = Supplier(name=name, contact=contact, phone=phone, category=category, status=status)
        db.session.add(s)
        print(f'[ADD] 供应商: {name}')

def _seed_products():
    products = [
        ('康师傅红烧牛肉面', '方便食品', '100g/包', '包', 50,  500),
        ('农夫山泉550ml',    '饮料',     '550ml/瓶', '瓶', 100, 2000),
        ('伊利纯牛奶',       '乳制品',   '250ml/盒', '盒', 80,  1000),
        ('百事可乐330ml',    '饮料',     '330ml/罐', '罐', 60,  1500),
        ('乐事薯片',         '零食',     '75g/袋',   '袋', 40,  800),
    ]
    for name, category, spec, unit, stock_min, stock_max in products:
        if Product.query.filter_by(name=name).first():
            print(f'[SKIP] 商品已存在: {name}')
            continue
        p = Product(name=name, category=category, spec=spec, unit=unit,
                    stock_min=stock_min, stock_max=stock_max)
        db.session.add(p)
        print(f'[ADD] 商品: {name}')

if __name__ == '__main__':
    init_db()
