"""
示例数据填充脚本
用法: python scripts/seed_demo.py
- 扩充供应商、商品数据
- 生成近30天入库/出库记录
- 生成库存、盘点、操作日志数据
"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import date, datetime, timedelta, timezone
from app import create_app
from models import db
from models.user import User
from models.product import Product
from models.supplier import Supplier
from models.inventory import Inventory
from models.inbound import InboundOrder
from models.outbound import OutboundOrder
from models.stocktake import StocktakeOrder
from models.log import OperationLog

random.seed(42)

def rand_dt(days_ago_max=30, days_ago_min=0):
    delta = random.randint(days_ago_min, days_ago_max)
    return datetime.now(timezone.utc) - timedelta(days=delta, hours=random.randint(0,23), minutes=random.randint(0,59))

def seed_all():
    app = create_app()
    with app.app_context():
        db.create_all()

        users   = _seed_users()
        supps   = _seed_suppliers()
        prods   = _seed_products()
        invs    = _seed_inventory(prods)
        _seed_inbound(supps, prods, invs, users)
        _seed_outbound(prods, invs, users)
        _seed_stocktake(prods, invs, users)
        _seed_logs(users)

        db.session.commit()
        print('\n[OK] 示例数据填充完成')

# ── Users ──────────────────────────────────────────────
def _seed_users():
    data = [
        ('admin',     'admin123',     'admin'),
        ('warehouse', 'warehouse123', 'warehouse'),
        ('purchaser', 'purchaser123', 'purchaser'),
    ]
    result = {}
    for username, password, role in data:
        u = User.query.filter_by(username=username).first()
        if not u:
            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.flush()
            print(f'[ADD] 用户: {username}')
        result[username] = u
    return result

# ── Suppliers ──────────────────────────────────────────
def _seed_suppliers():
    data = [
        ('康师傅食品',   '张伟',   '13800001111', '方便食品,饮料',       'active'),
        ('农夫山泉',     '李娜',   '13800002222', '饮用水,饮料',         'active'),
        ('伊利乳业',     '王芳',   '13800003333', '乳制品,冷饮',         'active'),
        ('百事食品',     '赵磊',   '13800004444', '零食,饮料',           'active'),
        ('旺旺集团',     '陈静',   '13800005555', '零食,饼干,糖果',      'active'),
        ('统一企业',     '刘洋',   '13800006666', '方便食品,饮料,乳品',  'active'),
        ('海天味业',     '孙丽',   '13800007777', '调味品',              'active'),
        ('中粮集团',     '周强',   '13800008888', '粮油,食品',           'active'),
        ('好丽友',       '吴敏',   '13800009999', '零食,饼干',           'active'),
        ('达利食品',     '郑超',   '13900001111', '零食,饮料,面包',      'inactive'),
    ]
    result = {}
    for name, contact, phone, category, status in data:
        s = Supplier.query.filter_by(name=name).first()
        if not s:
            s = Supplier(name=name, contact=contact, phone=phone, category=category, status=status)
            db.session.add(s)
            db.session.flush()
            print(f'[ADD] 供应商: {name}')
        result[name] = s
    return result

# ── Products ───────────────────────────────────────────
def _seed_products():
    data = [
        ('康师傅红烧牛肉面', '方便食品', '100g/包',  '包', 50,  500),
        ('康师傅冰红茶500ml','饮料',     '500ml/瓶', '瓶', 80,  1200),
        ('农夫山泉550ml',    '饮料',     '550ml/瓶', '瓶', 100, 2000),
        ('农夫山泉矿泉水1L', '饮料',     '1L/瓶',    '瓶', 60,  800),
        ('伊利纯牛奶250ml',  '乳制品',   '250ml/盒', '盒', 80,  1000),
        ('伊利酸奶100g',     '乳制品',   '100g/杯',  '杯', 60,  600),
        ('百事可乐330ml',    '饮料',     '330ml/罐', '罐', 60,  1500),
        ('乐事薯片75g',      '零食',     '75g/袋',   '袋', 40,  800),
        ('旺旺雪饼84g',      '零食',     '84g/袋',   '袋', 30,  600),
        ('旺仔牛奶125ml',    '乳制品',   '125ml/罐', '罐', 50,  800),
        ('统一老坛酸菜面',   '方便食品', '108g/包',  '包', 40,  400),
        ('统一鲜橙多450ml',  '饮料',     '450ml/瓶', '瓶', 60,  1000),
        ('海天生抽500ml',    '调味品',   '500ml/瓶', '瓶', 20,  200),
        ('海天老抽500ml',    '调味品',   '500ml/瓶', '瓶', 20,  200),
        ('金龙鱼大米5kg',    '粮油',     '5kg/袋',   '袋', 30,  300),
        ('金龙鱼花生油5L',   '粮油',     '5L/桶',    '桶', 15,  150),
        ('好丽友派12枚',     '零食',     '336g/盒',  '盒', 30,  500),
        ('好丽友蘑菇饼干',   '零食',     '90g/袋',   '袋', 25,  400),
        ('达利园法式面包',   '面包',     '400g/袋',  '袋', 20,  300),
        ('可口可乐330ml',    '饮料',     '330ml/罐', '罐', 60,  1500),
    ]
    result = {}
    for name, category, spec, unit, stock_min, stock_max in data:
        p = Product.query.filter_by(name=name).first()
        if not p:
            p = Product(name=name, category=category, spec=spec, unit=unit,
                        stock_min=stock_min, stock_max=stock_max)
            db.session.add(p)
            db.session.flush()
            print(f'[ADD] 商品: {name}')
        result[name] = p
    return result

# ── Inventory ──────────────────────────────────────────
def _seed_inventory(prods):
    # quantity设计：部分正常、部分低于下限（预警）、部分超上限
    qty_map = {
        '康师傅红烧牛肉面': (320, 'A-01', date(2026,8,1)),
        '康师傅冰红茶500ml':(650, 'A-02', date(2026,9,15)),
        '农夫山泉550ml':    (980, 'B-01', date(2027,3,1)),
        '农夫山泉矿泉水1L': (30,  'B-02', date(2027,1,1)),   # 低于下限
        '伊利纯牛奶250ml':  (420, 'C-01', date(2026,5,20)),  # 即将过期
        '伊利酸奶100g':     (25,  'C-02', date(2026,4,10)),  # 低于下限+即将过期
        '百事可乐330ml':    (880, 'D-01', date(2026,12,1)),
        '乐事薯片75g':      (15,  'D-02', date(2026,7,1)),   # 低于下限
        '旺旺雪饼84g':      (280, 'E-01', date(2026,10,1)),
        '旺仔牛奶125ml':    (560, 'E-02', date(2026,8,20)),
        '统一老坛酸菜面':   (190, 'F-01', date(2026,9,1)),
        '统一鲜橙多450ml':  (720, 'F-02', date(2026,11,1)),
        '海天生抽500ml':    (85,  'G-01', date(2027,6,1)),
        '海天老抽500ml':    (12,  'G-02', date(2027,6,1)),   # 低于下限
        '金龙鱼大米5kg':    (180, 'H-01', None),
        '金龙鱼花生油5L':   (88,  'H-02', date(2027,1,1)),
        '好丽友派12枚':     (210, 'I-01', date(2026,6,15)),
        '好丽友蘑菇饼干':   (160, 'I-02', date(2026,7,20)),
        '达利园法式面包':   (8,   'J-01', date(2026,3,5)),   # 低于下限+即将过期
        '可口可乐330ml':    (1100,'J-02', date(2026,12,31)),
    }
    result = {}
    for name, p in prods.items():
        if name not in qty_map:
            continue
        qty, loc, exp = qty_map[name]
        inv = Inventory.query.filter_by(product_id=p.id).first()
        if not inv:
            batch = f'BATCH-2026-{str(p.id).zfill(3)}'
            inv = Inventory(product_id=p.id, batch_no=batch,
                            quantity=qty, location=loc, expire_date=exp)
            db.session.add(inv)
            db.session.flush()
            print(f'[ADD] 库存: {name} x{qty}')
        result[name] = inv
    return result

# ── Inbound ────────────────────────────────────────────
def _seed_inbound(supps, prods, invs, users):
    if InboundOrder.query.count() > 0:
        print('[SKIP] 入库记录已存在')
        return

    sup_list = list(supps.values())
    prod_list = list(prods.items())
    ops = [users['warehouse'], users['purchaser'], users['admin']]

    records = [
        ('康师傅食品',   '康师傅红烧牛肉面', 'BATCH-2026-001', 200, date(2026,8,1),  'A-01', 28),
        ('农夫山泉',     '农夫山泉550ml',    'BATCH-2026-003', 500, date(2027,3,1),  'B-01', 25),
        ('伊利乳业',     '伊利纯牛奶250ml',  'BATCH-2026-005', 300, date(2026,5,20), 'C-01', 22),
        ('百事食品',     '百事可乐330ml',    'BATCH-2026-007', 400, date(2026,12,1), 'D-01', 20),
        ('旺旺集团',     '旺旺雪饼84g',      'BATCH-2026-009', 200, date(2026,10,1), 'E-01', 18),
        ('统一企业',     '统一老坛酸菜面',   'BATCH-2026-011', 150, date(2026,9,1),  'F-01', 15),
        ('海天味业',     '海天生抽500ml',    'BATCH-2026-013', 100, date(2027,6,1),  'G-01', 12),
        ('中粮集团',     '金龙鱼大米5kg',    'BATCH-2026-015', 120, None,            'H-01', 10),
        ('好丽友',       '好丽友派12枚',     'BATCH-2026-017', 150, date(2026,6,15), 'I-01', 8),
        ('康师傅食品',   '康师傅冰红茶500ml','BATCH-2026-002', 300, date(2026,9,15), 'A-02', 6),
        ('农夫山泉',     '农夫山泉矿泉水1L', 'BATCH-2026-004', 200, date(2027,1,1),  'B-02', 5),
        ('伊利乳业',     '伊利酸奶100g',     'BATCH-2026-006', 200, date(2026,4,10), 'C-02', 4),
        ('百事食品',     '乐事薯片75g',      'BATCH-2026-008', 300, date(2026,7,1),  'D-02', 3),
        ('旺旺集团',     '旺仔牛奶125ml',    'BATCH-2026-010', 250, date(2026,8,20), 'E-02', 2),
        ('统一企业',     '统一鲜橙多450ml',  'BATCH-2026-012', 400, date(2026,11,1), 'F-02', 1),
    ]

    for sup_name, prod_name, batch, qty, exp, loc, days_ago in records:
        s = supps.get(sup_name)
        p = prods.get(prod_name)
        if not s or not p:
            continue
        op = random.choice(ops)
        o = InboundOrder(
            supplier_id=s.id, product_id=p.id, batch_no=batch,
            quantity=qty, expire_date=exp, operator_id=op.id,
            created_at=rand_dt(days_ago, days_ago)
        )
        db.session.add(o)
    print(f'[ADD] 入库记录 {len(records)} 条')

# ── Outbound ───────────────────────────────────────────
def _seed_outbound(prods, invs, users):
    if OutboundOrder.query.count() > 0:
        print('[SKIP] 出库记录已存在')
        return

    departments = ['收银台', '生鲜区', '熟食区', '仓储部', '配送中心', '门店补货']
    ops = [users['warehouse'], users['admin']]
    prod_list = list(prods.items())

    records = [
        ('农夫山泉550ml',    50,  '收银台',   27),
        ('百事可乐330ml',    80,  '收银台',   26),
        ('康师傅红烧牛肉面', 30,  '仓储部',   25),
        ('伊利纯牛奶250ml',  60,  '生鲜区',   24),
        ('乐事薯片75g',      40,  '收银台',   23),
        ('旺旺雪饼84g',      25,  '门店补货', 22),
        ('统一老坛酸菜面',   20,  '仓储部',   21),
        ('好丽友派12枚',     35,  '收银台',   20),
        ('可口可乐330ml',    100, '配送中心', 18),
        ('农夫山泉550ml',    80,  '门店补货', 16),
        ('伊利酸奶100g',     45,  '生鲜区',   15),
        ('金龙鱼大米5kg',    20,  '仓储部',   14),
        ('海天生抽500ml',    15,  '熟食区',   13),
        ('百事可乐330ml',    60,  '收银台',   12),
        ('康师傅冰红茶500ml',90,  '配送中心', 10),
        ('旺仔牛奶125ml',    50,  '收银台',   9),
        ('统一鲜橙多450ml',  70,  '门店补货', 8),
        ('好丽友蘑菇饼干',   30,  '收银台',   7),
        ('农夫山泉550ml',    120, '配送中心', 5),
        ('百事可乐330ml',    90,  '收银台',   4),
        ('伊利纯牛奶250ml',  80,  '生鲜区',   3),
        ('乐事薯片75g',      25,  '收银台',   2),
        ('可口可乐330ml',    150, '配送中心', 1),
        ('康师傅红烧牛肉面', 50,  '仓储部',   1),
    ]

    for prod_name, qty, dept, days_ago in records:
        p = prods.get(prod_name)
        if not p:
            continue
        op = random.choice(ops)
        o = OutboundOrder(
            product_id=p.id, quantity=qty, department=dept,
            operator_id=op.id, created_at=rand_dt(days_ago, days_ago)
        )
        db.session.add(o)
    print(f'[ADD] 出库记录 {len(records)} 条')

# ── Stocktake ──────────────────────────────────────────
def _seed_stocktake(prods, invs, users):
    if StocktakeOrder.query.count() > 0:
        print('[SKIP] 盘点记录已存在')
        return

    op_w = users['warehouse']
    op_a = users['admin']

    records = [
        ('农夫山泉550ml',    1000, 980,  'approved', 20),
        ('百事可乐330ml',    900,  880,  'approved', 18),
        ('伊利纯牛奶250ml',  450,  420,  'approved', 15),
        ('乐事薯片75g',      20,   15,   'approved', 12),
        ('旺旺雪饼84g',      290,  280,  'approved', 10),
        ('海天老抽500ml',    15,   12,   'pending',  5),
        ('达利园法式面包',   12,   8,    'pending',  3),
        ('金龙鱼花生油5L',   90,   88,   'pending',  2),
    ]

    for prod_name, book, actual, status, days_ago in records:
        p = prods.get(prod_name)
        if not p:
            continue
        s = StocktakeOrder(
            product_id=p.id, book_qty=book, actual_qty=actual,
            diff=actual - book, status=status,
            operator_id=op_w.id, created_at=rand_dt(days_ago, days_ago)
        )
        db.session.add(s)
    print(f'[ADD] 盘点记录 {len(records)} 条')

# ── Logs ───────────────────────────────────────────────
def _seed_logs(users):
    if OperationLog.query.count() > 0:
        print('[SKIP] 操作日志已存在')
        return

    op_a = users['admin']
    op_w = users['warehouse']
    op_p = users['purchaser']

    records = [
        (op_p, 'inbound',   '新增入库单：农夫山泉550ml x500，批次BATCH-2026-003',        25),
        (op_w, 'outbound',  '新增出库单：农夫山泉550ml x50，领用部门：收银台',            27),
        (op_p, 'inbound',   '新增入库单：百事可乐330ml x400，批次BATCH-2026-007',        20),
        (op_w, 'outbound',  '新增出库单：百事可乐330ml x80，领用部门：收银台',            26),
        (op_a, 'stocktake', '审核盘点单：农夫山泉550ml，账面1000→实际980，差异-20',       18),
        (op_w, 'inbound',   '新增入库单：伊利纯牛奶250ml x300，批次BATCH-2026-005',      22),
        (op_a, 'stocktake', '审核盘点单：百事可乐330ml，账面900→实际880，差异-20',        16),
        (op_p, 'inbound',   '新增入库单：康师傅红烧牛肉面 x200，批次BATCH-2026-001',     28),
        (op_w, 'outbound',  '新增出库单：伊利纯牛奶250ml x60，领用部门：生鲜区',         24),
        (op_a, 'product',   '新增商品：可口可乐330ml',                                   15),
        (op_w, 'outbound',  '新增出库单：可口可乐330ml x100，领用部门：配送中心',         18),
        (op_p, 'inbound',   '新增入库单：好丽友派12枚 x150，批次BATCH-2026-017',         8),
        (op_w, 'outbound',  '新增出库单：康师傅冰红茶500ml x90，领用部门：配送中心',      10),
        (op_a, 'supplier',  '新增供应商：好丽友',                                         30),
        (op_w, 'outbound',  '新增出库单：农夫山泉550ml x120，领用部门：配送中心',         5),
        (op_p, 'inbound',   '新增入库单：统一鲜橙多450ml x400，批次BATCH-2026-012',      1),
        (op_w, 'outbound',  '新增出库单：可口可乐330ml x150，领用部门：配送中心',         1),
        (op_a, 'stocktake', '提交盘点单：海天老抽500ml，账面15→实际12，差异-3',           5),
    ]

    for op, action, detail, days_ago in records:
        log = OperationLog(
            operator_id=op.id, action_type=action, detail=detail,
            created_at=rand_dt(days_ago, days_ago)
        )
        db.session.add(log)
    print(f'[ADD] 操作日志 {len(records)} 条')

if __name__ == '__main__':
    seed_all()
