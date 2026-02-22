"""
入库、出库、库存模块测试
"""


def auth(token):
    return {'Authorization': f'Bearer {token}'}


# ── 入库 ──────────────────────────────────────────────

def test_create_inbound(client, warehouse_token):
    res = client.post('/api/v1/inbound', headers=auth(warehouse_token),
                      json={
                          'supplier_id': 1,
                          'product_id': 1,
                          'batch_no': 'BATCH-001',
                          'quantity': 100,
                          'expire_date': '2027-01-01',
                          'location': 'A-01',
                      })
    assert res.status_code == 201
    data = res.get_json()
    assert data['quantity'] == 100
    assert data['batch_no'] == 'BATCH-001'


def test_list_inbound(client, warehouse_token):
    res = client.get('/api/v1/inbound', headers=auth(warehouse_token))
    assert res.status_code == 200
    assert len(res.get_json()) >= 1


def test_inbound_forbidden_for_purchaser(client, purchaser_token):
    res = client.post('/api/v1/inbound', headers=auth(purchaser_token),
                      json={'supplier_id': 1, 'product_id': 1, 'quantity': 10})
    assert res.status_code == 403


# ── 库存 ──────────────────────────────────────────────

def test_inventory_updated_after_inbound(client, admin_token):
    res = client.get('/api/v1/inventory', headers=auth(admin_token))
    assert res.status_code == 200
    items = res.get_json()
    total = sum(i['quantity'] for i in items if i['product_id'] == 1)
    assert total >= 100


def test_inventory_search(client, admin_token):
    res = client.get('/api/v1/inventory?q=测试', headers=auth(admin_token))
    assert res.status_code == 200


# ── 出库 ──────────────────────────────────────────────

def test_create_outbound(client, warehouse_token):
    res = client.post('/api/v1/outbound', headers=auth(warehouse_token),
                      json={'product_id': 1, 'quantity': 10, 'department': '收银台'})
    assert res.status_code == 201
    assert res.get_json()['quantity'] == 10


def test_outbound_insufficient_stock(client, warehouse_token):
    res = client.post('/api/v1/outbound', headers=auth(warehouse_token),
                      json={'product_id': 1, 'quantity': 999999, 'department': '收银台'})
    assert res.status_code == 400
    assert '库存不足' in res.get_json()['msg']


def test_outbound_forbidden_for_purchaser(client, purchaser_token):
    res = client.post('/api/v1/outbound', headers=auth(purchaser_token),
                      json={'product_id': 1, 'quantity': 1, 'department': '收银台'})
    assert res.status_code == 403
