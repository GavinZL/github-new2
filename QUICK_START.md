# 🚀 GitHub Trending 快速开始指南

欢迎使用 GitHub Trending 数据采集系统！本指南将帮助您在 5 分钟内开始使用。

## 📋 前提条件

- Python 3.8 或更高版本
- pip 包管理器
- 互联网连接

## ⚡ 60秒快速开始

### 1. 安装（30秒）

```bash
# 克隆或进入项目目录
cd github-new2

# 运行自动安装脚本
./install.sh
```

### 2. 采集数据（20秒）

```bash
# 采集本周热门项目
github-trending fetch --period weekly
```

### 3. 查看报告（10秒）

```bash
# 报告已自动生成，打开查看
open data/reports/report_*_weekly.html

# 或在浏览器中打开
# Linux: xdg-open data/reports/report_*_weekly.html
# Windows: start data/reports/report_*_weekly.html
```

就这么简单！✅

---

## 📚 基础使用

### 采集不同周期的数据

```bash
# 本日热门
github-trending fetch --period daily

# 本周热门
github-trending fetch --period weekly

# 本月热门
github-trending fetch --period monthly
```

### 按编程语言筛选

```bash
# Python 项目
github-trending fetch --period weekly --language python

# JavaScript 项目
github-trending fetch --period weekly --language javascript

# Go 项目
github-trending fetch --period weekly --language go
```

### 使用 GitHub API 增强数据

```bash
# 1. 设置 GitHub Token（可选，但推荐）
export GITHUB_TOKEN=ghp_your_token_here

# 2. 采集并增强数据
github-trending fetch --period weekly --enrich

# 增强后的数据包含：
# - Fork 数量
# - Issue 数量
# - 项目标签 (topics)
# - 许可证信息
# - 创建和更新时间
```

---

## 🔧 配置（可选）

### 方式 1: 环境变量

```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env 文件
nano .env

# 添加你的 GitHub Token
GITHUB_TOKEN=ghp_your_personal_access_token
```

### 方式 2: 配置文件

```bash
# 创建配置文件
cp config.yaml.example config.yaml

# 编辑配置
nano config.yaml
```

---

## 📊 查看和分析报告

生成的 HTML 报告包含：

- 📈 **TOP 10 项目卡片** - 最热门的项目展示
- 💻 **语言分布统计** - 编程语言使用情况
- 📋 **完整项目列表** - 所有项目的详细表格
- 🔍 **数据统计** - 总项目数、采集时间等

报告位置：`data/reports/`

---

## 🆘 常见问题

### Q: 如何获取 GitHub Token？

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限（不需要任何权限即可，或选择 `public_repo`）
4. 生成并复制 token
5. 设置环境变量或配置文件

### Q: 遇到速率限制怎么办？

```bash
# 使用 GitHub Token 提高限制
export GITHUB_TOKEN=your_token
github-trending fetch --period weekly --enrich
```

### Q: 数据保存在哪里？

```
data/
├── raw/       # 原始 CSV 数据
├── merged/    # 合并的历史数据
└── reports/   # HTML 报告
```

### Q: 如何只采集数据不生成报告？

```bash
github-trending fetch --period weekly --no-report
```

### Q: 如何从已有 CSV 生成报告？

```bash
github-trending report -i data/raw/trending_2024-01-15_weekly.csv
```

---

## 📖 更多资源

- 📘 **完整文档**: 查看 `README.md`
- 💡 **使用示例**: 查看 `EXAMPLES.md`
- 🔍 **项目概览**: 查看 `PROJECT_OVERVIEW.md`
- ❓ **帮助命令**: `github-trending --help`

---

## 🎯 下一步

1. **定时采集**: 设置 cron 任务定期采集
2. **数据分析**: 使用 Python 分析采集的数据
3. **自定义模板**: 创建自己的 HTML 报告模板
4. **多语言采集**: 采集多种编程语言的热门项目

查看 `EXAMPLES.md` 获取更多高级用法！

---

## ✅ 验证安装

```bash
# 运行验证脚本
./verify.sh

# 运行快速测试
python3 quick_test.py

# 查看版本
github-trending version

# 查看帮助
github-trending --help
```

---

**祝使用愉快！** 🎉

如有问题，请查看文档或提交 Issue。
