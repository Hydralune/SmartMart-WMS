"""
盘点、统计、日志模块测试
"""


def auth(token):
    return {'Authorization': f'Bearer {token}'}


# ── 盘点 ──────────────────────────────────────────────

def test_create_stocktake(client, warehouse_token):
    res = client.post('/api/v1/stocktake', headers=auth(warehouse_token),
                      json={'product_id': 1, 'actual_qty': 80})
    assert res.status_code == 201
    data = res.get_json()
    assert data['actual_qty'] == 80
    assert data['status'] == 'pending'


def test_approve_stocktake_as_admin(client, admin_token, warehouse_token):
    create = client.post('/api/v1/stocktake', headers=auth(warehouse_token),
                         json={'product_id': 1, 'actual_qty': 90})
    oid = create.get_json()['id']
    res = client.put(f'/api/v1/stocktake/{oid}/approve', headers=auth(admin_token))
    assert res.status_code == 200
    assert res.get_json()['status'] == 'approved'


def test_approve_stocktake_forbidden_for_warehouse(client, warehouse_token):
    create = client.post('/api/v1/stocktake', headers=auth(warehouse_token),
                         json={'product_id': 1, 'actual_qty': 70})
    oid = create.get_json()['id']
    res = client.put(f'/api/v1/stocktake/{oid}/approve', headers=auth(warehouse_token))
    assert res.status_code == 403


# ── 统计 ──────────────────────────────────────────────

def test_inventory_stats(client, admin_token):
    res = client.get('/api/v1/stats/inventory', headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_trend_stats(client, admin_token):
    res = client.get('/api/v1/stats/trend', headers=auth(admin_token))
    assert res.status_code == 200
    data = res.get_json()
    assert 'inbound' in data and 'outbound' in data


# ── 日志 ──────────────────────────────────────────────

def test_list_logs(client, admin_token):
    res = client.get('/api/v1/logs', headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
