"""
血压守护 - 生产环境服务器启动文件
支持Flask + Gunicorn部署
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.config import ProductionConfig

# 创建Flask应用
app = create_app(ProductionConfig)

if __name__ == '__main__':
    # 开发环境运行
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
    
# Gunicorn运行（生产环境推荐）：
# gunicorn -w 4 -b 0.0.0.0:5000 -t 120 --access-logfile logs/access.log --error-logfile logs/error.log app:app
