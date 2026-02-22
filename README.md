# SmartMart WMS

基于 Vue.js + Flask + MySQL 的网页版超市仓库管理系统。

## 功能模块

- 权限控制：管理员 / 仓库员 / 采购员三角色，JWT 鉴权
- 商品入库：关联供应商、批次、保质期，自动更新库存
- 商品出库：库存充足性校验，先进先出扣减
- 库存管理：实时明细、模糊搜索、上下限预警
- 库存盘点：账面 vs 实际对比，管理员审核后调整
- 供应商管理：新增 / 编辑 / 删除，关联入库单
- 数据统计：ECharts 柱状图（库存占比）+ 折线图（30天趋势）
- 操作日志：全量变动记录，支持 Excel 导出备份

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue.js 3 + Element Plus + ECharts |
| 后端 | Python 3 + Flask + Flask-JWT-Extended |
| 数据库 | MySQL 8 + SQLAlchemy + Flask-Migrate |

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

初始化数据库并启动：

```bash
flask db init && flask db migrate && flask db upgrade
python app.py
```

后端默认运行在 `http://localhost:5000`

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
SmartMart-WMS/
├── backend/
│   ├── app.py            # 应用入口
│   ├── config.py         # 配置
│   ├── models/           # ORM 模型
│   ├── routes/           # API 蓝图
│   └── utils/            # 工具（权限装饰器）
├── frontend/             # Vue.js 前端（待开发）
├── 项目文档.md
└── 要求.md
```

## API 前缀

所有接口统一前缀 `/api/v1`，需携带 `Authorization: Bearer <token>` 请求头。

## 当前进度

详见 [项目文档.md](./项目文档.md)
