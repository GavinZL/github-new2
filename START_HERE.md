# 🎯 GitHub Trending Web应用 - 快速开始

## 🚀 一键启动（推荐）

```bash
cd /Users/bigo/Documents/MyProject/gavinZL/github-new2
./start_web.sh
```

启动脚本会自动：
- ✅ 检查Python环境
- ✅ 创建虚拟环境（如果不存在）
- ✅ 安装所有依赖
- ✅ 启动Web服务

## 🌐 访问应用

启动成功后，在浏览器打开：

```
http://localhost:5000
```

你会看到一个漂亮的Web界面！

## 📱 使用方法

### 三步完成数据采集：

1. **在左侧选择参数**
   - 时间周期（今日/本周/本月）
   - 编程语言（Python、JavaScript等）
   - 项目数量（5-100）

2. **点击"开始采集"按钮**

3. **查看结果**
   - 右侧显示项目卡片
   - 点击"查看完整报告"获取HTML报告
   - 点击"下载CSV数据"获取原始数据

## 🎨 界面预览

```
┌─────────────────────────────────────────────────────────┐
│        🚀 GitHub Trending 数据采集器                     │
├──────────────┬──────────────────────────────────────────┤
│ ⚙️ 参数设置  │  📊 结果展示                              │
│              │                                           │
│ 📅 时间周期  │  ┌──────┐ ┌──────┐ ┌──────┐             │
│ 💻 编程语言  │  │项目1 │ │项目2 │ │项目3 │             │
│ 📊 项目数量  │  └──────┘ └──────┘ └──────┘             │
│ 🔑 Token     │                                           │
│ ✅ 增强数据  │  ┌──────┐ ┌──────┐ ┌──────┐             │
│              │  │项目4 │ │项目5 │ │项目6 │             │
│ [开始采集]   │  └──────┘ └──────┘ └──────┘             │
└──────────────┴──────────────────────────────────────────┘
```

## 🔑 GitHub Token（可选）

获取更详细信息需要Token：

1. 访问 https://github.com/settings/tokens
2. 生成新token
3. 复制并粘贴到Web界面的Token输入框

## 📂 生成的文件

数据会保存在：

```
data/
├── raw/                    # CSV原始数据
└── reports/               # HTML可视化报告
```

## ❓ 遇到问题？

### 无法启动？

运行以下命令手动安装：

```bash
cd /Users/bigo/Documents/MyProject/gavinZL/github-new2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flask
python web_app.py
```

### 端口被占用？

修改 `web_app.py` 最后一行，将5000改为其他端口（如8000）

### 查看详细文档

- [WEB_APP_INSTALL.md](WEB_APP_INSTALL.md) - 详细安装说明
- [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) - 完整使用指南

## ✨ 主要特性

- 🎯 **可视化参数选择** - 无需命令行
- 📊 **实时数据展示** - 动态加载
- 🎨 **精美界面** - 现代化设计
- 💾 **多格式导出** - HTML + CSV
- 🔑 **可选增强** - GitHub API集成

## 🎉 立即开始

```bash
./start_web.sh
```

然后访问 http://localhost:5000

享受吧！🚀
