# GitHub Trending 项目数据采集系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个基于 Python 开发的 CLI 工具，用于自动采集 GitHub 平台上星标增长迅速的热门项目数据，并生成结构化的数据报告。

## ✨ 核心功能

- 📊 **自动采集** - 定期获取 GitHub Trending 项目列表（支持按日/周/月统计）
- 💾 **数据存储** - 将采集数据以 CSV 格式持久化到本地
- 📈 **可视化报告** - 自动生成 HTML 格式的可视化数据报告
- 🔍 **数据分析** - 支持历史数据追踪和趋势分析
- 🎯 **灵活筛选** - 支持按编程语言筛选项目
- 🔌 **API 增强** - 可选使用 GitHub API 获取详细项目信息

## 🚀 快速开始

### 安装

#### 方式一：从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/github-trending.git
cd github-trending

# 安装依赖
pip install -r requirements.txt

# 安装工具
pip install -e .
```

#### 方式二：直接安装

```bash
pip install -r requirements.txt
pip install .
```

### 基础使用

#### 1. 采集数据

采集本周热门项目：

```bash
github-trending fetch --period weekly
```

采集本日热门 Python 项目：

```bash
github-trending fetch --period daily --language python
```

采集并使用 GitHub API 增强数据（需要 API Token）：

```bash
export GITHUB_TOKEN=your_github_token
github-trending fetch --period weekly --enrich
```

#### 2. 生成报告

从已有 CSV 文件生成报告：

```bash
github-trending report -i data/raw/trending_2024-01-15_weekly.csv
```

对比两个时期的数据：

```bash
github-trending report -i current.csv --compare previous.csv
```

#### 3. 查看配置

```bash
github-trending config-info
```

## 📁 项目结构

```
github-trending/
├── src/
│   └── github_trending/
│       ├── __init__.py          # 包初始化
│       ├── cli.py               # CLI 命令接口
│       ├── models.py            # 数据模型
│       ├── config.py            # 配置管理
│       ├── exceptions.py        # 自定义异常
│       ├── collectors/          # 数据采集模块
│       │   ├── trending_scraper.py  # Trending 页面爬虫
│       │   └── github_api.py        # GitHub API 客户端
│       ├── storage/             # 数据存储模块
│       │   └── csv_handler.py       # CSV 文件处理
│       ├── reporters/           # 报告生成模块
│       │   └── html_generator.py    # HTML 报告生成器
│       └── utils/               # 工具模块
│           └── __init__.py          # 日志工具
├── data/                        # 数据目录
│   ├── raw/                     # 原始采集数据
│   ├── merged/                  # 合并的历史数据
│   └── reports/                 # HTML 报告
├── templates/                   # HTML 模板目录
├── logs/                        # 日志文件
├── tests/                       # 测试文件
├── config.yaml.example          # 配置文件示例
├── requirements.txt             # 依赖列表
├── setup.py                     # 安装脚本
└── README.md                    # 项目文档
```

## ⚙️ 配置

### 配置文件

复制示例配置文件：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml` 进行自定义配置：

```yaml
github:
  # GitHub Personal Access Token（可选，提高速率限制）
  api_token: "your_token_here"
  api_base_url: "https://api.github.com"
  timeout: 30

storage:
  data_dir: "./data"
  encoding: "utf-8-sig"

report:
  template_dir: "./templates"
  auto_generate: true

logging:
  level: "INFO"
  file: "logs/app.log"
```

### 环境变量

也可以通过环境变量配置：

```bash
export GITHUB_TOKEN=your_github_token
export DATA_DIR=./my_data
export LOG_LEVEL=DEBUG
```

### 配置优先级

1. 命令行参数（最高优先级）
2. 环境变量
3. 用户配置文件 (`~/.github-trending/config.yaml`)
4. 项目配置文件 (`./config.yaml`)
5. 默认值（最低优先级）

## 📋 CLI 命令详解

### fetch 命令

采集 GitHub Trending 数据。

```bash
github-trending fetch [OPTIONS]
```

**选项：**

- `-p, --period [daily|weekly|monthly]` - 统计周期（默认：weekly）
- `-l, --language TEXT` - 按编程语言筛选
- `-o, --output PATH` - 输出目录
- `-t, --api-token TEXT` - GitHub API Token
- `--no-report` - 仅采集数据，不生成报告
- `-n, --limit INTEGER` - 采集项目数量上限（默认：25）
- `--enrich / --no-enrich` - 是否使用 API 增强数据（默认：true）

**示例：**

```bash
# 采集本周前 50 个热门项目
github-trending fetch --limit 50

# 采集本月热门 JavaScript 项目
github-trending fetch --period monthly --language javascript

# 采集数据但不生成报告
github-trending fetch --no-report
```

### report 命令

从 CSV 数据生成 HTML 报告。

```bash
github-trending report [OPTIONS]
```

**选项：**

- `-i, --input PATH` - 输入 CSV 文件路径（必需）
- `-o, --output PATH` - 输出 HTML 文件路径
- `--template PATH` - 自定义模板目录
- `-c, --compare PATH` - 对比的历史 CSV 文件

**示例：**

```bash
# 基础报告生成
github-trending report -i data/raw/trending_2024-01-15_weekly.csv

# 指定输出路径
github-trending report -i data.csv -o my_report.html

# 对比两期数据
github-trending report -i current.csv --compare previous.csv
```

### config-info 命令

显示当前配置信息。

```bash
github-trending config-info
```

### version 命令

显示版本信息。

```bash
github-trending version
```

## 📊 数据格式

### CSV 文件格式

生成的 CSV 文件包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| repository_name | 字符串 | 仓库全名 (owner/repo) |
| description | 字符串 | 项目描述 |
| language | 字符串 | 主要编程语言 |
| stars_total | 整数 | 总星标数 |
| stars_period | 整数 | 周期内新增星标数 |
| forks | 整数 | Fork 数量 |
| open_issues | 整数 | 开放 Issue 数 |
| created_at | 日期时间 | 仓库创建时间 |
| updated_at | 日期时间 | 最后更新时间 |
| url | 字符串 | 仓库 URL |
| topics | 列表 | 项目标签 |
| license | 字符串 | 许可证类型 |
| captured_at | 日期时间 | 数据采集时间 |
| trend_period | 枚举 | 统计周期 (daily/weekly/monthly) |

### HTML 报告内容

生成的 HTML 报告包含：

- **报告元数据** - 生成时间、数据周期、项目总数
- **TOP 10 项目卡片** - 展示热度最高的前 10 个项目
- **语言分布统计** - 编程语言使用情况分析
- **完整项目表格** - 所有项目的详细信息
- **对比分析**（可选）- 与历史数据的对比

## 🔧 高级用法

### 自定义 HTML 模板

1. 创建模板目录：

```bash
mkdir -p templates
```

2. 创建 `templates/report.html` 文件，使用 Jinja2 语法：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Custom Report</title>
</head>
<body>
    <h1>{{ metadata.period.value|title }} Trending</h1>
    {% for project in top_projects %}
        <div>{{ project.repository_name }}</div>
    {% endfor %}
</body>
</html>
```

3. 使用自定义模板生成报告：

```bash
github-trending report -i data.csv --template ./templates
```

### 定时采集

使用 cron 定时任务：

```bash
# 编辑 crontab
crontab -e

# 每周一早上 8 点执行采集
0 8 * * 1 cd /path/to/github-trending && /usr/bin/github-trending fetch --period weekly
```

### 数据分析示例

使用 Python 分析采集的数据：

```python
from github_trending.storage import CSVHandler
from pathlib import Path

# 加载数据
handler = CSVHandler()
projects = handler.load_projects(Path("data/raw/trending_2024-01-15_weekly.csv"))

# 分析语言分布
languages = {}
for p in projects:
    if p.language:
        languages[p.language] = languages.get(p.language, 0) + 1

# 输出前 5 名
for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{lang}: {count}")
```

## 🧪 测试

运行测试套件：

```bash
pytest tests/
```

运行测试并生成覆盖率报告：

```bash
pytest --cov=github_trending --cov-report=html tests/
```

## 🐛 故障排除

### API 速率限制

如果遇到 GitHub API 速率限制：

1. 设置 GitHub Personal Access Token：

```bash
export GITHUB_TOKEN=your_token_here
```

2. 或在 `config.yaml` 中配置：

```yaml
github:
  api_token: "your_token_here"
```

### 网络连接问题

如果遇到网络连接失败：

- 检查网络连接
- 增加超时时间（在 config.yaml 中设置 `github.timeout`）
- 使用代理（设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量）

### 编码问题

如果 CSV 文件在 Excel 中显示乱码：

- 确保配置使用 `utf-8-sig` 编码
- 或使用支持 UTF-8 的编辑器打开 CSV 文件

## 🤝 贡献

欢迎贡献代码、报告问题或提出功能建议！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [GitHub](https://github.com) - 数据来源
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [Click](https://click.palletsprojects.com/) - CLI 框架
- [Jinja2](https://jinja.palletsprojects.com/) - 模板引擎

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue：[GitHub Issues](https://github.com/yourusername/github-trending/issues)
- 邮件：team@example.com

---

⭐ 如果这个项目对你有帮助，欢迎给个 Star！
