# GitHub Trending 使用示例

本文档提供了 GitHub Trending 系统的详细使用示例。

## 安装

### 使用安装脚本（推荐）

```bash
chmod +x install.sh
./install.sh
```

### 手动安装

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装工具
pip install -e .
```

## 基础使用示例

### 示例 1: 采集本周热门项目

```bash
# 采集本周 GitHub Trending 项目
github-trending fetch --period weekly

# 输出:
# ✓ Fetched 25 trending projects
# ✓ Saved data to: data/raw/trending_2024-01-15_weekly.csv
# ✓ Generated report: data/reports/report_2024-01-15_weekly.html
# ✅ Success!
```

### 示例 2: 采集特定语言的项目

```bash
# 采集本周热门 Python 项目
github-trending fetch --period weekly --language python

# 采集本日热门 JavaScript 项目
github-trending fetch --period daily --language javascript

# 采集本月热门 Go 项目
github-trending fetch --period monthly --language go
```

### 示例 3: 使用 GitHub API 增强数据

```bash
# 设置 GitHub Token（提高速率限制并获取详细信息）
export GITHUB_TOKEN=ghp_your_token_here

# 采集并增强数据
github-trending fetch --period weekly --enrich

# 数据将包含：
# - 完整的 fork 数量
# - Issue 数量
# - 创建和更新时间
# - Topics 标签
# - 许可证信息
```

### 示例 4: 自定义采集数量

```bash
# 采集前 50 个热门项目
github-trending fetch --period weekly --limit 50

# 采集前 10 个项目
github-trending fetch --period daily --limit 10
```

### 示例 5: 只采集数据，不生成报告

```bash
# 仅保存 CSV 数据
github-trending fetch --period weekly --no-report
```

## 报告生成示例

### 示例 6: 从已有 CSV 生成报告

```bash
# 生成 HTML 报告
github-trending report -i data/raw/trending_2024-01-15_weekly.csv

# 指定输出文件名
github-trending report -i data/raw/trending_2024-01-15_weekly.csv -o my_report.html
```

### 示例 7: 对比两期数据

```bash
# 对比本周和上周的数据
github-trending report \
  -i data/raw/trending_2024-01-15_weekly.csv \
  --compare data/raw/trending_2024-01-08_weekly.csv

# 报告将显示:
# - 新进榜项目数量
# - 退出榜单项目数量
# - 持续在榜项目数量
```

## 配置管理示例

### 示例 8: 查看当前配置

```bash
github-trending config-info

# 输出:
# 📋 Current Configuration:
# 
# GitHub API:
#   Base URL: https://api.github.com
#   Token: ✓ Set
#   Timeout: 30s
# 
# Storage:
#   Data Directory: ./data
#   Encoding: utf-8-sig
# ...
```

### 示例 9: 使用自定义配置文件

```bash
# 创建自定义配置
cat > my_config.yaml << EOF
github:
  api_token: "ghp_your_token"
  timeout: 60

storage:
  data_dir: "./my_data"

logging:
  level: "DEBUG"
EOF

# 使用自定义配置
github-trending --config my_config.yaml fetch --period weekly
```

### 示例 10: 使用环境变量配置

```bash
# 创建 .env 文件
cat > .env << EOF
GITHUB_TOKEN=ghp_your_token_here
DATA_DIR=./custom_data
LOG_LEVEL=DEBUG
EOF

# 环境变量会自动加载
github-trending fetch --period weekly
```

## 高级使用示例

### 示例 11: 定时任务（Cron）

```bash
# 编辑 crontab
crontab -e

# 添加定时任务
# 每周一早上 8 点采集数据
0 8 * * 1 cd /path/to/github-trending && /path/to/venv/bin/github-trending fetch --period weekly

# 每天早上 9 点采集 Python 项目
0 9 * * * cd /path/to/github-trending && /path/to/venv/bin/github-trending fetch --period daily --language python
```

### 示例 12: 批量采集多种语言

```bash
#!/bin/bash
# collect_multiple.sh

LANGUAGES=("python" "javascript" "go" "rust" "typescript")

for lang in "${LANGUAGES[@]}"; do
    echo "Collecting $lang projects..."
    github-trending fetch --period weekly --language "$lang" --limit 20
    sleep 5  # 避免请求过快
done

echo "All done!"
```

### 示例 13: 自定义输出目录

```bash
# 指定输出目录
mkdir -p /tmp/github_data
github-trending fetch --period weekly --output /tmp/github_data

# 数据将保存到: /tmp/github_data/trending_2024-01-15_weekly.csv
```

### 示例 14: 数据分析脚本

```python
#!/usr/bin/env python3
"""分析采集的数据"""

from pathlib import Path
from collections import Counter
from github_trending.storage import CSVHandler

# 加载数据
handler = CSVHandler()
csv_file = Path("data/raw/trending_2024-01-15_weekly.csv")
projects = handler.load_projects(csv_file)

# 语言统计
languages = Counter(p.language for p in projects if p.language)
print("\n语言分布:")
for lang, count in languages.most_common(5):
    print(f"  {lang}: {count}")

# 星标统计
total_stars = sum(p.stars_period for p in projects)
avg_stars = total_stars / len(projects)
print(f"\n平均新增星标: {avg_stars:.0f}")

# Top 3 项目
print("\nTop 3 项目:")
for i, p in enumerate(sorted(projects, key=lambda x: x.stars_period, reverse=True)[:3], 1):
    print(f"  {i}. {p.repository_name}: +{p.stars_period} ⭐")
```

### 示例 15: 使用自定义 HTML 模板

```bash
# 创建模板目录
mkdir -p templates

# 创建自定义模板 templates/report.html
cat > templates/report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Custom Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .project { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>GitHub Trending - {{ metadata.period.value }}</h1>
    <p>Generated: {{ metadata.generated_at.strftime('%Y-%m-%d %H:%M') }}</p>
    
    {% for project in top_projects %}
    <div class="project">
        <h2><a href="{{ project.url }}">{{ project.repository_name }}</a></h2>
        <p>{{ project.description }}</p>
        <p>Stars: {{ project.stars_total }} (+{{ project.stars_period }})</p>
        <p>Language: {{ project.language }}</p>
    </div>
    {% endfor %}
</body>
</html>
EOF

# 使用自定义模板生成报告
github-trending report -i data/raw/trending_2024-01-15_weekly.csv --template ./templates
```

## 故障排除示例

### 问题 1: API 速率限制

```bash
# 症状: "API rate limit exceeded"

# 解决方案: 添加 GitHub Token
export GITHUB_TOKEN=ghp_your_personal_access_token

# 或在 config.yaml 中配置
github:
  api_token: "ghp_your_token"

# Token 可以在这里生成: https://github.com/settings/tokens
# 权限: 只需要 public_repo 或不勾选任何权限
```

### 问题 2: 网络连接超时

```bash
# 症状: "Connection timeout"

# 解决方案: 增加超时时间
cat > config.yaml << EOF
github:
  timeout: 120  # 增加到 120 秒
EOF

# 或使用代理
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
github-trending fetch --period weekly
```

### 问题 3: CSV 文件乱码

```bash
# 症状: Excel 打开 CSV 显示乱码

# 解决方案: 配置使用 utf-8-sig 编码
cat > config.yaml << EOF
storage:
  encoding: "utf-8-sig"  # Excel 兼容的编码
EOF

# 或使用专业的 CSV 编辑器
# 推荐: LibreOffice Calc, VS Code with CSV extension
```

## 完整工作流示例

### 每周数据采集和分析流程

```bash
#!/bin/bash
# weekly_workflow.sh

set -e

echo "开始每周 GitHub Trending 数据采集..."

# 1. 采集数据
echo "步骤 1/4: 采集数据"
github-trending fetch --period weekly --limit 50

# 2. 获取最新 CSV 文件
LATEST_CSV=$(ls -t data/raw/trending_*_weekly.csv | head -1)
echo "最新数据: $LATEST_CSV"

# 3. 生成报告
echo "步骤 2/4: 生成报告"
github-trending report -i "$LATEST_CSV"

# 4. 如果有上周数据，生成对比报告
PREVIOUS_CSV=$(ls -t data/raw/trending_*_weekly.csv | head -2 | tail -1)
if [ "$LATEST_CSV" != "$PREVIOUS_CSV" ]; then
    echo "步骤 3/4: 生成对比报告"
    github-trending report -i "$LATEST_CSV" --compare "$PREVIOUS_CSV" -o data/reports/comparison.html
fi

# 5. 汇总统计
echo "步骤 4/4: 数据统计"
python3 << EOF
from pathlib import Path
from github_trending.storage import CSVHandler

handler = CSVHandler()
projects = handler.load_projects(Path("$LATEST_CSV"))

print(f"\n📊 本周统计:")
print(f"  总项目数: {len(projects)}")
print(f"  平均星标: {sum(p.stars_period for p in projects) / len(projects):.0f}")
print(f"  语言数量: {len(set(p.language for p in projects if p.language))}")
print(f"\n🏆 Top 3 项目:")
for i, p in enumerate(sorted(projects, key=lambda x: x.stars_period, reverse=True)[:3], 1):
    print(f"  {i}. {p.repository_name}")
    print(f"     +{p.stars_period} ⭐ | {p.language or 'N/A'}")
EOF

echo ""
echo "✅ 工作流完成！"
echo "📄 查看报告: data/reports/"
```

使用方法：

```bash
chmod +x weekly_workflow.sh
./weekly_workflow.sh
```

## 更多资源

- 查看帮助: `github-trending --help`
- 查看子命令帮助: `github-trending fetch --help`
- 查看版本: `github-trending version`
- 项目仓库: https://github.com/yourusername/github-trending
