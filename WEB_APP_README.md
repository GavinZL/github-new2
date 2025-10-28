# 🌐 GitHub Trending 交互式Web应用

## 📖 项目简介

这是一个基于Flask的交互式Web应用程序，为GitHub Trending数据采集系统提供可视化的用户界面。用户可以通过浏览器手动选择参数（时间周期、编程语言、项目数量等），动态获取GitHub热门项目数据并以精美的方式展示。

## ✨ 核心特性

### 🎯 用户友好
- **无需命令行** - 所有操作通过Web界面完成
- **可视化参数选择** - 下拉菜单、输入框、复选框
- **实时数据展示** - 动态加载和显示结果
- **响应式设计** - 支持桌面、平板、手机访问

### 📊 数据展示
- **项目卡片网格** - 精美展示每个项目的详细信息
- **统计摘要** - 项目总数、语言分布、Star统计
- **完整HTML报告** - 可导出专业的分析报告
- **CSV数据导出** - 原始数据下载

### 🔧 功能丰富
- **多周期支持** - 今日/本周/本月热门
- **语言筛选** - 支持20+种编程语言
- **数量可调** - 5-100个项目
- **可选增强** - GitHub API详细信息集成
- **Token支持** - 获取更多项目元数据

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
./start_web.sh
```

### 方式二：手动启动

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
pip install flask

# 4. 启动应用
python web_app.py
```

### 访问应用

在浏览器中打开：**http://localhost:5000**

## 📱 界面说明

### 主界面布局

```
┌────────────────────────────────────────────────────────────┐
│         🚀 GitHub Trending 数据采集器                       │
│              手动选择参数，动态获取最热门的GitHub项目         │
├─────────────────┬──────────────────────────────────────────┤
│  ⚙️ 采集参数设置 │         📊 结果展示                       │
│                 │                                          │
│  📅 时间周期     │   ╔═══════════╗ ╔═══════════╗           │
│  [本周热门  ▼]  │   ║  项目 1   ║ ║  项目 2   ║           │
│                 │   ║  ⭐12.5K   ║ ║  ⭐8.3K    ║           │
│  💻 编程语言     │   ║  📈+2.1K   ║ ║  📈+1.5K   ║           │
│  [Python    ▼]  │   ╚═══════════╝ ╚═══════════╝           │
│                 │                                          │
│  📊 项目数量     │   ╔═══════════╗ ╔═══════════╗           │
│  [  25      ]   │   ║  项目 3   ║ ║  项目 4   ║           │
│                 │   ║  ⭐15.2K   ║ ║  ⭐9.8K    ║           │
│  🔑 Token        │   ║  📈+3.2K   ║ ║  📈+1.8K   ║           │
│  [ghp_...   ]   │   ╚═══════════╝ ╚═══════════╝           │
│                 │                                          │
│  ☑ 增强数据      │   [📊 查看完整报告] [💾 下载CSV]          │
│                 │                                          │
│  ┌───────────┐  │                                          │
│  │ 🔍 开始采集 │  │                                          │
│  └───────────┘  │                                          │
└─────────────────┴──────────────────────────────────────────┘
```

### 左侧控制面板

#### 📅 时间周期
- **今日热门 (Daily)** - 过去24小时最热门的项目
- **本周热门 (Weekly)** - 过去7天最热门的项目 ⭐ 推荐
- **本月热门 (Monthly)** - 过去30天最热门的项目

#### 💻 编程语言
支持的语言包括：
- All Languages（所有语言）
- Python, JavaScript, TypeScript
- Java, Go, Rust, C++, C, C#
- PHP, Ruby, Swift, Kotlin
- 以及更多...

#### 📊 项目数量
- 范围：5 - 100
- 默认：25
- 步进：5

#### 🔑 GitHub Token（可选）
- 格式：ghp_xxxxxxxxxxxx
- 用途：获取更详细的项目信息
- 获取：https://github.com/settings/tokens

#### ✅ 增强数据
- 勾选：调用GitHub API获取详细信息
- 需要：有效的GitHub Token
- 包含：Fork数、Issue数、Topics、License等

### 右侧结果展示

#### 统计摘要（顶部）
显示三个关键指标：
- **项目总数** - 成功获取的项目数量
- **编程语言** - 涉及的不同语言数
- **总Star数** - 所有项目的累计Star数

#### 操作按钮
- **📊 查看完整报告** - 在新标签页打开HTML报告
- **💾 下载CSV数据** - 下载原始CSV文件

#### 项目卡片网格
每个项目卡片包含：
- 🥇 **排名徽章** - 圆形数字标识
- 📦 **仓库名称** - 可点击链接到GitHub
- 📝 **项目描述** - 简短说明
- 💻 **编程语言** - 主要使用的语言
- ⭐ **总Star数** - 累计获得的Star
- 📈 **周期增长** - 在选定周期内新增的Star
- 🍴 **Fork数** - 被Fork的次数
- ❗ **Issue数** - 未关闭的Issue（如果有）
- 🏷️ **标签** - 项目相关的topics（最多显示5个）

## 🎯 使用场景

### 场景1：研究Python生态
**目标**：了解Python社区最新趋势

1. 时间周期：本周热门
2. 编程语言：Python
3. 项目数量：50
4. 增强数据：开启（提供Token）
5. 开始采集

**结果**：获取50个最热门的Python项目，包含详细的Star增长、Fork数、相关Topics等信息

### 场景2：跟踪前端技术
**目标**：追踪JavaScript/TypeScript热门项目

1. 时间周期：今日热门
2. 编程语言：JavaScript
3. 项目数量：25
4. 开始采集

**结果**：快速查看今日最热门的前端项目

### 场景3：全语言月度观察
**目标**：了解整个开发者社区的月度趋势

1. 时间周期：本月热门
2. 编程语言：All Languages
3. 项目数量：100
4. 增强数据：开启
5. 开始采集

**结果**：获取100个跨语言的热门项目，分析技术趋势

### 场景4：竞品分析
**目标**：研究某个领域的热门项目

1. 时间周期：本周热门
2. 编程语言：选择目标语言
3. 项目数量：50
4. 增强数据：开启
5. 查看完整报告
6. 下载CSV进行深入分析

## 📂 文件结构

```
github-new2/
├── web_app.py                  # Flask Web应用主程序
├── start_web.sh                # 启动脚本
├── test_web_api.py             # API测试脚本
├── templates/
│   └── index.html              # Web界面HTML模板
├── data/
│   ├── raw/                    # CSV原始数据
│   │   └── trending_*.csv
│   ├── merged/                 # 历史合并数据
│   └── reports/                # HTML报告
│       └── report_*.html
├── logs/
│   └── app.log                 # 应用日志
└── docs/
    ├── WEB_APP_README.md       # 本文档
    ├── WEB_APP_INSTALL.md      # 安装指南
    ├── WEB_APP_GUIDE.md        # 使用指南
    └── START_HERE.md           # 快速开始
```

## 🔧 技术架构

### 后端技术栈
- **Flask** - Python Web微框架
- **Requests** - HTTP客户端
- **BeautifulSoup4** - HTML解析
- **Jinja2** - 模板引擎
- **PyYAML** - 配置管理

### 前端技术栈
- **HTML5** - 语义化标记
- **CSS3** - 渐变、动画、Grid布局
- **JavaScript (Vanilla)** - 无依赖的纯JS
- **Fetch API** - 异步HTTP请求

### API设计

#### GET /
- **描述**：主页面
- **返回**：HTML界面

#### POST /api/fetch
- **描述**：获取trending数据
- **请求体**：
  ```json
  {
    "period": "weekly",
    "language": "python",
    "limit": 25,
    "enrich": true,
    "github_token": "ghp_..."
  }
  ```
- **响应**：
  ```json
  {
    "success": true,
    "data": {
      "projects": [...],
      "count": 25,
      "csv_file": "path/to/file.csv",
      "report_file": "path/to/report.html"
    }
  }
  ```

#### GET /api/report/<filename>
- **描述**：获取HTML报告
- **返回**：HTML文件

#### GET /api/health
- **描述**：健康检查
- **返回**：
  ```json
  {
    "status": "ok",
    "timestamp": "2024-10-28T12:00:00"
  }
  ```

## 💡 高级功能

### 1. 环境变量配置

创建 `.env` 文件：

```bash
GITHUB_TOKEN=ghp_your_personal_access_token
DATA_DIR=./data
LOG_LEVEL=INFO
```

### 2. API编程调用

使用curl测试API：

```bash
curl -X POST http://localhost:5000/api/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "period": "weekly",
    "language": "python",
    "limit": 25,
    "enrich": true
  }'
```

使用Python调用：

```python
import requests

response = requests.post('http://localhost:5000/api/fetch', json={
    'period': 'weekly',
    'language': 'python',
    'limit': 25,
    'enrich': False
})

data = response.json()
if data['success']:
    projects = data['data']['projects']
    for project in projects:
        print(f"{project['repository_name']}: {project['stars_total']} stars")
```

### 3. 自定义端口

修改 `web_app.py` 最后一行：

```python
app.run(host='0.0.0.0', port=8000, debug=True)  # 使用8000端口
```

### 4. 生产环境部署

使用Gunicorn：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## 🎨 界面定制

### 修改颜色主题

编辑 `templates/index.html` 中的CSS变量：

```css
/* 修改主色调 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 改为其他颜色 */
background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
```

### 调整布局

修改网格列数：

```css
.project-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    /* 改为固定2列 */
    grid-template-columns: repeat(2, 1fr);
}
```

## 🆘 故障排除

### 问题：无法启动 - ModuleNotFoundError: No module named 'flask'

**解决方案**：
```bash
source venv/bin/activate
pip install flask
```

### 问题：端口5000已被占用

**解决方案**：
```bash
# 查看占用端口的进程
lsof -i :5000

# 修改端口或杀死进程
kill -9 <PID>
```

### 问题：采集失败 - 网络错误

**解决方案**：
- 检查网络连接
- 检查GitHub是否可访问
- 尝试使用代理
- 降低项目数量

### 问题：Token无效

**解决方案**：
- 重新生成Token
- 确保Token格式正确（ghp_...）
- 检查Token是否过期

### 问题：页面加载慢

**解决方案**：
- 减少项目数量
- 关闭数据增强功能
- 检查服务器资源

## 📊 性能优化

- **缓存策略**：相同参数的请求可以缓存结果
- **异步加载**：大量数据分批加载
- **数据库存储**：使用SQLite存储历史数据
- **CDN加速**：静态资源使用CDN

## 🔐 安全建议

- ✅ 不在代码中硬编码Token
- ✅ 使用环境变量管理敏感信息
- ✅ 限制API请求频率
- ✅ 验证用户输入
- ✅ 使用HTTPS（生产环境）

## 📚 相关文档

- [START_HERE.md](START_HERE.md) - 快速开始指南
- [WEB_APP_INSTALL.md](WEB_APP_INSTALL.md) - 详细安装说明
- [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) - 完整使用教程
- [QUICK_START.md](QUICK_START.md) - 命令行工具指南
- [README.md](README.md) - 项目总览

## 🎯 未来规划

- [ ] 数据可视化图表（Chart.js）
- [ ] 用户登录和收藏功能
- [ ] 历史数据对比分析
- [ ] 邮件订阅提醒
- [ ] RESTful API完善
- [ ] Docker容器化部署
- [ ] 多语言界面支持

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🎉 开始使用

```bash
# 一键启动
./start_web.sh

# 访问应用
open http://localhost:5000
```

享受探索GitHub热门项目的乐趣！🚀
