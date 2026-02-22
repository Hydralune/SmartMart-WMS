"""
认证模块测试
"""


def test_login_success(client):
    res = client.post('/api/v1/auth/login',
                      json={'username': 'admin', 'password': 'admin123'})
    assert res.status_code == 200
    data = res.get_json()
    assert 'token' in data
    assert data['user']['role'] == 'admin'


def test_login_wrong_password(client):
    res = client.post('/api/v1/auth/login',
                      json={'username': 'admin', 'password': 'wrong'})
    assert res.status_code == 401


def test_login_unknown_user(client):
    res = client.post('/api/v1/auth/login',
                      json={'username': 'nobody', 'password': 'x'})
    assert res.status_code == 401


def test_protected_route_without_token(client):
    res = client.get('/api/v1/products')
    assert res.status_code == 401
