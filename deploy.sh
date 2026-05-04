#!/bin/bash
# 血压守护 - 生产环境部署脚本
# 适用于 Ubuntu 20.04 / CentOS 7+

set -e

# ==================== 配置变量 ====================
APP_NAME="blood-pressure-guardian"
APP_DIR="/var/www/${APP_NAME}"
PYTHON_VENV="${APP_DIR}/venv"
APP_USER="bpuser"
APP_GROUP="www-data"
APP_PORT=5000
DB_NAME="bp_guardian"
DB_USER="bp_user"
DB_PASSWORD="your_secure_password_here"  # 请修改为强密码

echo "========================================="
echo "血压守护 - 生产环境部署"
echo "========================================="

# ==================== 1. 系统准备 ====================
echo "[1/8] 更新系统..."
apt-get update && apt-get upgrade -y

echo "[2/8] 安装依赖..."
apt-get install -y \
    python3-pip \
    python3-venv \
    nginx \
    mysql-server \
    supervisor \
    git \
    certbot \
    python3-certbot-nginx

# ==================== 2. 创建用户和目录 ====================
echo "[3/8] 创建应用目录和用户..."
mkdir -p ${APP_DIR}
mkdir -p ${APP_DIR}/logs
mkdir -p ${APP_DIR}/uploads

useradd -r -s /bin/false ${APP_USER} 2>/dev/null || true
chown -R ${APP_USER}:${APP_GROUP} ${APP_DIR}

# ==================== 3. 配置MySQL数据库 ====================
echo "[4/8] 配置MySQL数据库..."
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# ==================== 4. 部署应用代码 ====================
echo "[5/8] 部署应用代码..."
# 方式1: 从Git仓库拉取
# cd ${APP_DIR} && git clone <your-repo-url> .

# 方式2: 从本地上传（手动）
# scp -r backend/* user@server:${APP_DIR}/

# 创建虚拟环境
cd ${APP_DIR}
python3 -m venv ${PYTHON_VENV}
source ${PYTHON_VENV}/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements-production.txt

# ==================== 5. 配置环境变量 ====================
echo "[6/8] 配置环境变量..."
cat > ${APP_DIR}/.env <<EOF
# 应用配置
FLASK_ENV=production
SECRET_KEY=$(openssl rand -base64 32)
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@localhost/${DB_NAME}

# 微信配置（按需填写）
WECHAT_APP_ID=
WECHAT_APP_SECRET=

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=${APP_DIR}/logs/production.log

# 文件上传
UPLOAD_FOLDER=${APP_DIR}/uploads
EOF

# ==================== 6. 初始化数据库 ====================
echo "[7/8] 初始化数据库..."
cd ${APP_DIR}
source ${PYTHON_VENV}/bin/activate
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('数据库初始化完成')"

# ==================== 7. 配置Nginx ====================
echo "[8/8] 配置Nginx..."
cat > /etc/nginx/sites-available/${APP_NAME} <<EOF
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名
    
    client_max_body_size 16M;
    
    location /static {
        alias ${APP_DIR}/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://127.0.0.1:${APP_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 120s;
        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
    }
    
    location ~ /\. {
        deny all;
    }
}
EOF

ln -sf /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# ==================== 8. 配置Supervisor ====================
echo "配置Supervisor..."
cat > /etc/supervisor/conf.d/${APP_NAME}.conf <<EOF
[program:${APP_NAME}]
command=${PYTHON_VENV}/bin/gunicorn -w 4 -b 127.0.0.1:${APP_PORT} -t 120 --access-logfile ${APP_DIR}/logs/access.log --error-logfile ${APP_DIR}/logs/error.log wsgi:app
directory=${APP_DIR}
user=${APP_USER}
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=${APP_DIR}/logs/supervisor-error.log
stdout_logfile=${APP_DIR}/logs/supervisor-stdout.log
EOF

supervisorctl reread
supervisorctl update
supervisorctl start ${APP_NAME}

# ==================== 完成 ====================
echo ""
echo "========================================="
echo "部署完成！"
echo "========================================="
echo "应用地址: http://your-domain.com"
echo "日志目录: ${APP_DIR}/logs"
echo ""
echo "下一步："
echo "1. 配置HTTPS: certbot --nginx -d your-domain.com"
echo "2. 修改Nginx配置中的域名"
echo "3. 填写微信服务号配置（.env文件）"
echo "4. 测试访问: curl http://localhost:${APP_PORT}"
echo ""
echo "管理命令："
echo "  查看状态: supervisorctl status ${APP_NAME}"
echo "  重启应用: supervisorctl restart ${APP_NAME}"
echo "  查看日志: tail -f ${APP_DIR}/logs/production.log"
echo "========================================="
