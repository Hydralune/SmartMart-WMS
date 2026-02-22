# SmartMart WMS

基于 Vue.js 3 + Flask + MySQL 的网页版超市仓库管理系统，深色现代 UI，全功能覆盖。

## 功能模块

| 模块 | 说明 |
|------|------|
| 数据看板 | ECharts 柱状图/折线图、KPI 卡片、库存预警 |
| 库存管理 | 实时明细、模糊搜索、上下限预警标红 |
| 入库管理 | 关联供应商/批次/保质期，自动更新库存 |
| 出库管理 | 先进先出扣减，库存不足弹窗拦截 |
| 库存盘点 | 账面 vs 实际对比，管理员审核后调整 |
| 商品管理 | 新增/编辑/删除商品，设置库存上下限 |
| 供应商管理 | 维护供应商信息与合作状态 |
| 操作日志 | 全量变动记录，支持 Excel 一键导出备份 |

## 权限角色

| 角色 | 权限 |
|------|------|
| 管理员 (admin) | 全功能，含审核盘点、删除数据 |
| 仓库员 (warehouse) | 入库、出库、库存查询、盘点录入 |
| 采购员 (purchaser) | 供应商管理、库存查看 |

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue.js 3 + Element Plus + ECharts + Pinia + Vue Router |
| 后端 | Python 3 + Flask + Flask-JWT-Extended + SQLAlchemy |
| 数据库 | MySQL 8 + Flask-Migrate |
| 测试 | pytest + pytest-flask（28 个测试，SQLite 内存库） |

## 快速开始

### 1. 数据库

```sql
CREATE DATABASE smartmart_wms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 后端

```bash
cd backend
pip install -r requirements.txt
```

修改 `config.py` 中的数据库连接：

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost:3306/smartmart_wms'
```

初始化数据库、写入初始数据并启动：

```bash
flask db init && flask db migrate && flask db upgrade
python scripts/init_db.py   # 创建表 + 初始账号/商品/供应商
python app.py               # 启动后端，默认 http://localhost:5000
```

### 3. 前端

```bash
cd frontend
npm install
npm run dev                 # 默认 http://localhost:3000
```

### 4. 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 仓库员 | warehouse | warehouse123 |
| 采购员 | purchaser | purchaser123 |

## 运行测试

```bash
cd backend
pip install -r tests/requirements-test.txt
pytest
```

28 个测试覆盖认证、商品、库存、入库、出库、盘点、供应商、统计、日志全模块。

## 项目结构

```
SmartMart-WMS/
├── backend/
│   ├── app.py                # Flask 应用入口
│   ├── config.py             # 配置（数据库、JWT）
│   ├── models/               # ORM 模型（8 张表）
│   ├── routes/               # API 蓝图（9 个模块）
│   ├── utils/                # 角色权限装饰器
│   ├── scripts/
│   │   └── init_db.py        # 数据库初始化脚本
│   ├── tests/                # pytest 测试套件
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/            # 8 个页面组件
│   │   ├── api/              # Axios 封装
│   │   ├── store/            # Pinia 状态管理
│   │   ├── router/           # Vue Router
│   │   └── assets/           # 全局样式
│   └── package.json
├── 项目文档.md
└── 要求.md
```

## API 前缀

所有接口统一前缀 `/api/v1`，需携带 `Authorization: Bearer <token>` 请求头。

详细接口文档见 [项目文档.md](./项目文档.md)
