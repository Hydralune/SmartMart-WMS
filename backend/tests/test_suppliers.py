"""
供应商管理模块测试
"""


def auth(token):
    return {'Authorization': f'Bearer {token}'}


def test_list_suppliers(client, admin_token):
    res = client.get('/api/v1/suppliers', headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_create_supplier_as_purchaser(client, purchaser_token):
    res = client.post('/api/v1/suppliers', headers=auth(purchaser_token),
                      json={'name': '新供应商', 'contact': '李四',
                            'phone': '13900000001', 'category': '零食',
                            'status': 'active'})
    assert res.status_code == 201
    assert res.get_json()['name'] == '新供应商'


def test_create_supplier_forbidden_for_warehouse(client, warehouse_token):
    res = client.post('/api/v1/suppliers', headers=auth(warehouse_token),
                      json={'name': '非法供应商'})
    assert res.status_code == 403


def test_update_supplier(client, admin_token):
    create = client.post('/api/v1/suppliers', headers=auth(admin_token),
                         json={'name': '待更新供应商', 'status': 'active'})
    sid = create.get_json()['id']
    res = client.put(f'/api/v1/suppliers/{sid}', headers=auth(admin_token),
                     json={'status': 'inactive'})
    assert res.status_code == 200
    assert res.get_json()['status'] == 'inactive'


def test_delete_supplier_as_admin(client, admin_token):
    create = client.post('/api/v1/suppliers', headers=auth(admin_token),
                         json={'name': '待删除供应商', 'status': 'active'})
    sid = create.get_json()['id']
    res = client.delete(f'/api/v1/suppliers/{sid}', headers=auth(admin_token))
    assert res.status_code == 200
