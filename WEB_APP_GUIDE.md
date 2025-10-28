# 🌐 GitHub Trending Web应用使用指南

## 📝 简介

这是一个交互式的Web应用程序，允许你通过浏览器界面手动选择参数来动态获取GitHub Trending项目数据。无需使用命令行，所有操作都可以在网页中完成。

## ✨ 功能特性

- 🎯 **可视化参数选择** - 通过下拉菜单和输入框选择采集参数
- 📊 **实时数据展示** - 动态显示获取的项目数据
- 🎨 **精美卡片布局** - 以卡片形式展示每个项目的详细信息
- 📈 **统计概览** - 显示项目总数、语言分布、Star统计等
- 💾 **数据导出** - 支持查看HTML报告和下载CSV数据
- 🔑 **可选Token增强** - 支持使用GitHub Token获取更详细的数据

## 🚀 快速开始

### 1. 启动Web应用

**方式一：使用启动脚本（推荐）**

```bash
./start_web.sh
```

**方式二：手动启动**

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果还没安装）
pip install -r requirements.txt

# 启动应用
python3 web_app.py
```

### 2. 访问Web界面

启动成功后，在浏览器中打开：

```
http://localhost:5000
```

### 3. 选择参数并采集

在左侧控制面板中：

1. **选择时间周期**：今日/本周/本月
2. **选择编程语言**：Python、JavaScript等，或选择"全部语言"
3. **设置项目数量**：5-100个项目
4. **（可选）输入GitHub Token**：获取更详细的项目信息
5. **选择是否增强数据**：勾选后会调用GitHub API获取更多信息
6. 点击"**🔍 开始采集**"按钮

### 4. 查看结果

采集完成后，你将看到：

- ✅ 成功提示和统计摘要
- 📊 项目卡片网格展示
- 🔗 每个项目的详细信息（仓库名、描述、语言、Star等）
- 🏷️ 项目标签（topics）
- 📈 完整HTML报告链接

## 🎛️ 参数说明

### 时间周期 (Period)

- **今日热门 (Daily)** - 当天最热门的项目
- **本周热门 (Weekly)** - 本周最热门的项目 ⭐ 推荐
- **本月热门 (Monthly)** - 本月最热门的项目

### 编程语言 (Language)

支持的语言包括：

- Python, JavaScript, TypeScript
- Java, Go, Rust, C++, C, C#
- PHP, Ruby, Swift, Kotlin, Scala
- Dart, R, Shell, Vue, React
- 以及更多...

选择"全部语言"可以获取所有语言的热门项目。

### 项目数量 (Limit)

- 最小值：5
- 最大值：100
- 推荐值：25（默认）
- 步进值：5

### GitHub Token（可选）

如果你有GitHub Personal Access Token，可以输入来获取：

- Fork数量
- Issue数量
- 项目标签（topics）
- 许可证信息
- 创建和更新时间

**如何获取Token：**

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限（不需要任何权限，或选择 `public_repo`）
4. 生成并复制token
5. 在网页的Token输入框中粘贴

### 增强数据选项

- ✅ **勾选**：使用GitHub API获取详细信息（需要Token）
- ☐ **不勾选**：仅从Trending页面抓取基本信息（无需Token）

## 📊 数据展示

### 统计摘要

顶部会显示：
- 项目总数
- 编程语言种类数
- 总Star数

### 项目卡片

每个项目卡片包含：

- 🥇 **排名徽章** - 显示项目在列表中的位置
- 📦 **仓库名称** - 可点击跳转到GitHub
- 📝 **项目描述** - 简短介绍
- 💻 **编程语言** - 主要使用的语言
- ⭐ **总Star数** - 累计获得的Star
- 📈 **周期增长** - 在选定周期内新增的Star
- 🍴 **Fork数** - 被Fork的次数
- ❗ **Issue数** - 未关闭的Issue数量
- 🏷️ **标签** - 项目相关的topics（最多显示5个）

## 💾 数据导出

### 查看完整报告

点击"📊 查看完整报告"按钮，会在新标签页打开一个格式化的HTML报告，包含：

- TOP 10项目详细展示
- 语言分布统计图
- 完整项目列表表格
- 数据统计信息

报告文件保存在：`data/reports/report_*.html`

### 下载CSV数据

点击"💾 下载CSV数据"按钮，可以下载原始数据文件。

CSV文件保存在：`data/raw/trending_*.csv`

## 🔧 配置选项

### 环境变量

你可以通过环境变量预设GitHub Token：

```bash
export GITHUB_TOKEN=ghp_your_token_here
./start_web.sh
```

### 配置文件

创建 `.env` 文件：

```bash
GITHUB_TOKEN=ghp_your_personal_access_token
DATA_DIR=./data
LOG_LEVEL=INFO
```

## 📁 文件结构

```
github-new2/
├── web_app.py              # Flask Web应用主程序
├── start_web.sh            # Web应用启动脚本
├── templates/
│   └── index.html          # Web界面模板
├── data/
│   ├── raw/                # 原始CSV数据
│   ├── merged/             # 合并的历史数据
│   └── reports/            # 生成的HTML报告
└── logs/                   # 应用日志
```

## 🎨 界面特性

- 📱 **响应式设计** - 支持桌面、平板、手机访问
- 🌈 **渐变色背景** - 现代化的视觉设计
- 🎯 **固定控制面板** - 左侧参数面板保持可见
- ⚡ **实时加载动画** - 采集过程显示加载状态
- 🔄 **动画效果** - 卡片悬停、按钮点击等交互动画

## 🔍 使用场景

### 场景1：查看本周Python热门项目

1. 时间周期：选择"本周热门"
2. 编程语言：选择"Python"
3. 项目数量：25
4. 点击"开始采集"

### 场景2：获取详细的JavaScript项目信息

1. 时间周期：选择"本周热门"
2. 编程语言：选择"JavaScript"
3. 项目数量：50
4. 输入GitHub Token
5. 勾选"增强数据"
6. 点击"开始采集"

### 场景3：对比不同语言的热度

1. 先采集Python项目，查看统计
2. 再采集JavaScript项目，查看统计
3. 对比两者的Star增长、项目数量等

## ⚠️ 注意事项

1. **速率限制**
   - 不使用Token：每小时60次请求
   - 使用Token：每小时5000次请求

2. **采集时间**
   - 不增强数据：约5-10秒
   - 增强数据：约10-30秒（取决于项目数量）

3. **数据时效性**
   - GitHub Trending数据每小时更新
   - 建议不要过于频繁采集

4. **浏览器兼容性**
   - 推荐使用Chrome、Firefox、Safari最新版本
   - 需要启用JavaScript

## 🆘 常见问题

### Q: 启动失败怎么办？

**A:** 检查：
1. Python版本 >= 3.8
2. 是否安装了所有依赖：`pip install -r requirements.txt`
3. 5000端口是否被占用：`lsof -i :5000`

### Q: 采集失败显示错误？

**A:** 可能原因：
1. 网络连接问题
2. GitHub服务暂时不可用
3. Token无效或过期
4. 参数设置错误（如数量过大）

### Q: Token在哪里输入？

**A:** 
- 在网页左侧控制面板的"GitHub Token"输入框中
- 或通过环境变量 `GITHUB_TOKEN` 设置

### Q: 如何查看历史采集数据？

**A:** 
- CSV文件：`data/raw/` 目录
- HTML报告：`data/reports/` 目录
- 可以使用 `github-trending report` 命令重新生成报告

### Q: 可以修改界面样式吗？

**A:** 
可以！编辑 `templates/index.html` 文件中的CSS部分。

### Q: 数据保存在哪里？

**A:** 
- 原始数据：`data/raw/trending_YYYY-MM-DD_period.csv`
- 报告文件：`data/reports/report_YYYY-MM-DD_period.html`

## 🔐 安全性

- Token仅在内存中使用，不会被保存到文件
- 网页使用POST请求提交数据
- 可以通过环境变量安全地配置Token

## 🌟 高级用法

### 集成到CI/CD

你可以使用API endpoint在自动化流程中调用：

```bash
curl -X POST http://localhost:5000/api/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "period": "weekly",
    "language": "python",
    "limit": 25,
    "enrich": true,
    "github_token": "ghp_..."
  }'
```

### 定制化开发

基于现有代码，你可以：
- 添加新的筛选条件
- 自定义数据展示方式
- 集成到其他系统
- 添加数据分析功能

## 📚 相关文档

- [快速开始](QUICK_START.md) - 命令行工具使用指南
- [项目概览](PROJECT_OVERVIEW.md) - 系统架构说明
- [使用示例](EXAMPLES.md) - 更多使用案例

## 🎉 开始使用

现在就启动Web应用，探索GitHub上最热门的项目吧！

```bash
./start_web.sh
```

然后在浏览器中访问：http://localhost:5000

祝使用愉快！🚀
