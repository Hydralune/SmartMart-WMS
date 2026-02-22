"""
商品管理模块测试
"""


def auth(token):
    return {'Authorization': f'Bearer {token}'}


def test_list_products(client, admin_token):
    res = client.get('/api/v1/products', headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_create_product_as_admin(client, admin_token):
    res = client.post('/api/v1/products', headers=auth(admin_token),
                      json={'name': '新商品A', 'category': '零食',
                            'spec': '100g', 'unit': '袋',
                            'stock_min': 20, 'stock_max': 300})
    assert res.status_code == 201
    assert res.get_json()['name'] == '新商品A'


def test_create_product_forbidden_for_warehouse(client, warehouse_token):
    res = client.post('/api/v1/products', headers=auth(warehouse_token),
                      json={'name': '非法商品', 'category': '零食'})
    assert res.status_code == 403


def test_update_product(client, admin_token):
    # 先创建
    create = client.post('/api/v1/products', headers=auth(admin_token),
                         json={'name': '待更新商品', 'category': '饮料',
                               'spec': '330ml', 'unit': '罐',
                               'stock_min': 10, 'stock_max': 200})
    pid = create.get_json()['id']
    res = client.put(f'/api/v1/products/{pid}', headers=auth(admin_token),
                     json={'stock_min': 50})
    assert res.status_code == 200
    assert res.get_json()['stock_min'] == 50


def test_delete_product(client, admin_token):
    create = client.post('/api/v1/products', headers=auth(admin_token),
                         json={'name': '待删除商品', 'category': '乳制品',
                               'spec': '250ml', 'unit': '盒',
                               'stock_min': 5, 'stock_max': 100})
    pid = create.get_json()['id']
    res = client.delete(f'/api/v1/products/{pid}', headers=auth(admin_token))
    assert res.status_code == 200
