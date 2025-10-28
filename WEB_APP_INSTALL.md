# 🚀 GitHub Trending Web应用 - 安装和运行指南

## ⚡ 快速安装

由于系统环境限制，请按照以下步骤创建虚拟环境并安装依赖：

### 步骤 1: 创建虚拟环境

```bash
cd /Users/bigo/Documents/MyProject/gavinZL/github-new2
python3 -m venv venv
```

### 步骤 2: 激活虚拟环境

```bash
source venv/bin/activate
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
pip install flask
```

### 步骤 4: 启动Web应用

```bash
python web_app.py
```

或者使用启动脚本：

```bash
./start_web.sh
```

## 🌐 访问应用

启动成功后，在浏览器中访问：

```
http://localhost:5000
```

## 📋 完整安装命令（一键执行）

如果你想一键完成所有步骤，可以直接运行：

```bash
cd /Users/bigo/Documents/MyProject/gavinZL/github-new2 && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -q --upgrade pip && \
pip install -q -r requirements.txt && \
pip install -q flask && \
python web_app.py
```

## 📱 界面功能

Web界面包含以下功能：

### 左侧控制面板
- 📅 **时间周期选择**: 今日/本周/本月
- 💻 **编程语言选择**: Python, JavaScript, Go等20+语言
- 📊 **项目数量设置**: 5-100个（默认25）
- 🔑 **GitHub Token输入**: 可选，用于获取详细信息
- ✅ **增强数据开关**: 是否调用GitHub API

### 右侧结果展示
- 📈 **统计摘要**: 项目总数、语言数、总Star数
- 🎴 **项目卡片网格**: 精美展示每个项目
- 📊 **完整报告按钮**: 查看详细HTML报告
- 💾 **CSV下载**: 导出原始数据

## 🎯 使用示例

### 示例1: 查看本周Python热门项目

1. 时间周期：选择 "本周热门 (Weekly)"
2. 编程语言：选择 "Python"
3. 项目数量：25
4. 点击 "🔍 开始采集"

### 示例2: 获取详细的JavaScript项目

1. 时间周期：选择 "本周热门 (Weekly)"
2. 编程语言：选择 "JavaScript"
3. 项目数量：50
4. GitHub Token：输入你的token (ghp_...)
5. 勾选 "增强数据 (API详情)"
6. 点击 "🔍 开始采集"

### 示例3: 查看所有语言的月度热门

1. 时间周期：选择 "本月热门 (Monthly)"
2. 编程语言：选择 "All Languages"
3. 项目数量：100
4. 点击 "🔍 开始采集"

## 🔑 获取GitHub Token（可选）

如果你想获取更详细的项目信息，可以创建GitHub Token：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 设置token名称，如 "GitHub Trending Web App"
4. 选择权限（可以不选，或选择 `public_repo`）
5. 点击 "Generate token"
6. 复制生成的token（格式：ghp_xxxxxxxxxxxx）
7. 在Web界面的Token输入框中粘贴

## 📂 数据文件位置

采集的数据会保存在以下位置：

```
data/
├── raw/                    # 原始CSV数据
│   └── trending_2024-10-28_weekly.csv
├── merged/                 # 历史合并数据
└── reports/               # HTML报告
    └── report_2024-10-28_weekly.html
```

## 🎨 界面预览

Web界面特点：

- 🌈 渐变紫色背景
- 🎯 左右分栏布局（控制面板 + 结果展示）
- 🎴 项目卡片网格展示
- 💫 悬停动画效果
- 📱 响应式设计（支持手机、平板）
- 🔄 实时加载动画

## ⚙️ 技术栈

- **后端**: Flask (Python Web框架)
- **前端**: HTML5 + CSS3 + JavaScript
- **数据采集**: BeautifulSoup4 + Requests
- **数据存储**: CSV + HTML报告
- **API集成**: GitHub REST API

## 🆘 故障排除

### 问题1: ModuleNotFoundError: No module named 'flask'

**解决方案**:
```bash
source venv/bin/activate
pip install flask
```

### 问题2: 端口5000已被占用

**解决方案**: 修改 `web_app.py` 最后一行的端口号
```python
app.run(host='0.0.0.0', port=8000, debug=True)  # 改为8000或其他端口
```

### 问题3: 虚拟环境激活失败

**解决方案**: 使用完整路径
```bash
source /Users/bigo/Documents/MyProject/gavinZL/github-new2/venv/bin/activate
```

### 问题4: 采集失败

**可能原因**:
- 网络连接问题
- GitHub服务暂时不可用
- Token无效或过期
- 参数设置错误

**解决方案**:
- 检查网络连接
- 稍后重试
- 检查Token是否正确
- 降低项目数量限制

## 💡 高级用法

### 设置环境变量

创建 `.env` 文件：

```bash
GITHUB_TOKEN=ghp_your_personal_access_token
DATA_DIR=./data
LOG_LEVEL=INFO
```

### API调用

可以通过API endpoint编程调用：

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

### 查看日志

应用日志保存在 `logs/app.log`：

```bash
tail -f logs/app.log
```

## 📚 相关文档

- [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) - 详细使用指南
- [QUICK_START.md](QUICK_START.md) - 命令行工具快速开始
- [README.md](README.md) - 项目完整文档

## ✅ 检查清单

安装前确认：

- ✅ Python 3.8+ 已安装
- ✅ pip 已安装
- ✅ 网络连接正常
- ✅ 5000端口未被占用

## 🎉 开始使用

现在执行以下命令启动应用：

```bash
# 一键安装并启动
./start_web.sh

# 或手动执行
cd /Users/bigo/Documents/MyProject/gavinZL/github-new2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flask
python web_app.py
```

然后访问：**http://localhost:5000**

祝使用愉快！🚀
