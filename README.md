# 血压守护 - Blood Pressure Guardian

智能服药提醒与家庭协同看护系统

## 项目概述

「血压守护」是一款基于微信生态的智能健康管理应用，旨在帮助高血压患者（尤其是老年人）实现科学服药管理，同时让子女和保姆能够协同参与看护工作。

## 核心功能

### 1. 用户与家庭管理
- 微信授权登录
- 创建/加入家庭组
- 家庭成员管理（父母、子女、保姆）
- 邀请码机制

### 2. 智能药程配置
- 药物信息录入（名称、剂量、频次）
- 服药时间配置
- 服药周期管理
- 服药渠道优先级设置

### 3. 多渠道提醒
- 微信模板消息
- 小程序订阅消息
- 手环震动提醒
- AI个性化提醒语生成

### 4. 服药追踪
- 服药日志记录
- 按时确认/保姆协助确认
- 漏服状态追踪
- 历史记录查询

### 5. 分级预警体系
- 一级预警（10分钟）：通知管理员子女和保姆
- 二级预警（25分钟）：通知所有子女和保姆
- 紧急预警（40分钟）：TTS电话外呼

### 6. 血压管理
- 血压数据录入
- 趋势分析
- 健康状态评估
- 数据可视化

### 7. 保姆协同
- 今日任务列表
- 健康快照查看
- 异常快速上报
- 交班小结生成

### 8. 库存管理
- 药物库存追踪
- 购药提醒
- 库存预警

## 技术架构

### 后端技术栈
- **框架**: Flask 3.0
- **数据库**: SQLite / MySQL
- **ORM**: SQLAlchemy
- **定时任务**: APScheduler
- **微信API**: 官方API

### 前端技术栈
- 微信小程序
- WXML/WXSS/JavaScript

## 项目结构

```
blood-pressure-guardian/
├── backend/                      # 后端服务
│   ├── app/
│   │   ├── __init__.py          # 应用工厂
│   │   ├── models/               # 数据模型
│   │   │   └── __init__.py      # 8个数据表
│   │   ├── routes/               # API路由
│   │   │   ├── auth.py           # 认证相关
│   │   │   ├── medication.py     # 药物相关
│   │   │   └── bp.py             # 血压相关
│   │   └── services/             # 业务服务
│   │       ├── alert_service.py  # 预警服务
│   │       └── wechat_service.py # 微信服务
│   ├── run.py                    # 启动入口
│   ├── requirements.txt          # 依赖列表
│   └── start.bat                 # 启动脚本
├── mini_program/                 # 微信小程序
│   ├── children/                 # 子女端
│   ├── nanny/                    # 保姆端
│   └── parent/                   # 父母端
├── admin/                        # 管理后台
└── README.md                     # 项目文档
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///blood_pressure_guardian.db
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret
```

### 3. 启动服务

```bash
python run.py
```

或双击 `start.bat`

### 4. 验证服务

访问 http://localhost:5000/api/health 应返回：

```json
{"status": "ok", "service": "Blood Pressure Guardian API"}
```

## 数据库模型

### User（用户）
- 用户基本信息
- 微信openid
- 角色：child（子女）/ nanny（保姆）/ admin（管理员）

### FamilyGroup（家庭组）
- 家庭组信息
- 邀请码
- 成员数量

### FamilyMember（家庭成员关系）
- 用户与家庭组的关联
- 成员角色

### Parent（父母）
- 被看护者信息
- 健康状态

### Medication（药物）
- 药物名称、剂量、频次
- 服药时间配置
- 起止日期

### MedicationLog（服药日志）
- 计划时间、实际时间
- 服药状态
- 确认人

### BloodPressureRecord（血压记录）
- 收缩压、舒张压、心率
- 测量时间
- 记录人

### Alert（预警）
- 预警等级
- 预警信息
- 处理状态

## API接口

### 认证相关
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/user/<id>` - 获取用户信息
- `PUT /api/auth/user/<id>` - 更新用户信息

### 家庭组相关
- `POST /api/family/groups` - 创建家庭组
- `GET /api/family/groups` - 获取用户家庭组列表
- `POST /api/family/groups/<id>/join` - 加入家庭组
- `GET /api/family/groups/<id>/members` - 获取成员列表
- `GET /api/family/groups/<id>/parents` - 获取父母列表
- `POST /api/family/groups/<id>/parents` - 添加父母

### 药物相关
- `POST /api/medications` - 创建药物
- `GET /api/medications/parent/<id>` - 获取父母的药物
- `PUT /api/medications/<id>` - 更新药物
- `DELETE /api/medications/<id>` - 删除药物

### 服药日志
- `POST /api/logs` - 创建服药日志
- `GET /api/logs/parent/<id>` - 获取服药记录
- `GET /api/logs/today/<id>` - 获取今日服药计划
- `POST /api/logs/<id>/confirm` - 确认服药

### 血压相关
- `GET /api/blood-pressure/parent/<id>` - 获取血压记录
- `POST /api/blood-pressure` - 添加血压记录
- `GET /api/blood-pressure/analysis/<id>` - 获取血压分析

## 服药流程

1. **起床检测**：系统检测到手环数据，判断父母已起床
2. **AI评估**：AI评估漏服风险
3. **低风险处理**：不发送预警，向保姆推送任务卡片
4. **服药提醒**：服药时间前5分钟，手环震动提醒
5. **微信通知**：服药时间到达，发送微信模板消息
6. **确认服药**：父母自行确认或保姆协助确认
7. **预警升级**：根据漏服时长发送不同级别预警

## 预警等级

- **一级预警**：漏服10分钟，通知管理员子女和保姆
- **二级预警**：漏服25分钟，通知所有子女和保姆
- **紧急预警**：漏服40分钟，启动电话外呼

## 开发计划

- [x] 需求分析
- [x] 系统设计
- [x] 数据库建模
- [x] 后端API开发
- [x] 小程序框架搭建
- [ ] 微信对接配置
- [ ] 预警定时任务
- [ ] 前端页面开发
- [ ] 测试与部署

## 许可证

MIT License

## 联系方式

如有问题，请提交Issue或联系开发团队。
