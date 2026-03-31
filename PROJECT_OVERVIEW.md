# GitHub Trending 项目开发文档

## 项目概览

本项目是一个完整的 GitHub Trending 数据采集系统，按照设计文档实现了以下模块：

### 已实现模块清单

#### ✅ 1. 项目结构 (COMPLETE)
```
github-new2/
├── src/github_trending/         # 主要源代码
│   ├── __init__.py             # 包初始化
│   ├── cli.py                  # CLI 命令接口
│   ├── models.py               # 数据模型
│   ├── config.py               # 配置管理
│   ├── exceptions.py           # 自定义异常
│   ├── collectors/             # 数据采集模块
│   ├── storage/                # 数据存储模块
│   ├── reporters/              # 报告生成模块
│   └── utils/                  # 工具模块
├── tests/                      # 测试文件
├── data/                       # 数据目录
├── templates/                  # HTML 模板
└── logs/                       # 日志文件
```

#### ✅ 2. 数据模型 (models.py)
- **TrendingProject**: 项目数据模型
  - 包含 14 个字段：repository_name, description, language, stars, forks 等
  - 实现 `to_dict()` 和 `from_dict()` 序列化方法
  - 内置数据验证 `validate()` 方法

- **TrendPeriod**: 趋势周期枚举
  - DAILY, WEEKLY, MONTHLY

- **ReportMetadata**: 报告元数据模型
  - 记录报告生成信息

#### ✅ 3. 配置管理 (config.py)
- **多层级配置加载**:
  1. 命令行参数（最高优先级）
  2. 环境变量
  3. 用户配置文件 (~/.github-trending/config.yaml)
  4. 项目配置文件 (./config.yaml)
  5. 默认值

- **配置模块**:
  - GitHubConfig: API 配置
  - StorageConfig: 存储配置
  - ReportConfig: 报告配置
  - LoggingConfig: 日志配置

#### ✅ 4. 异常处理系统 (exceptions.py)
- 自定义异常层次结构：
  - GitHubTrendingError (基础异常)
    - ConfigurationError
    - DataCollectionError
      - NetworkError
      - RateLimitError
      - ParseError
    - StorageError
      - FileIOError
    - ValidationError
    - ReportGenerationError
      - TemplateError

#### ✅ 5. 日志系统 (utils/__init__.py)
- 双输出：文件 + 控制台
- 可配置日志级别
- 格式化日志输出
- 函数：
  - `setup_logging()`: 配置日志系统
  - `get_logger()`: 获取logger实例

#### ✅ 6. 数据采集模块

**6.1 TrendingScraper (collectors/trending_scraper.py)**
- GitHub Trending 页面爬虫
- 功能：
  - 按周期抓取 (daily/weekly/monthly)
  - 按编程语言筛选
  - HTML 解析提取项目信息
  - 指数退避重试机制
  - 上下文管理器支持

**6.2 GitHubAPIClient (collectors/github_api.py)**
- GitHub REST API 客户端
- 功能：
  - 增强项目详细信息
  - API 速率限制处理
  - 自动等待速率重置
  - 批量处理项目数据
  - Token 认证支持

#### ✅ 7. 数据存储模块

**CSVHandler (storage/csv_handler.py)**
- CSV 文件读写处理
- 功能：
  - 保存项目列表到 CSV
  - 从 CSV 加载项目数据
  - 自动生成文件名
  - 合并历史数据
  - 数据去重
  - UTF-8-sig 编码（Excel 兼容）
- 文件组织：
  - raw/: 原始采集数据
  - merged/: 合并的历史数据
  - reports/: HTML 报告

#### ✅ 8. 报告生成模块

**HTMLReportGenerator (reporters/html_generator.py)**
- HTML 报告生成器
- 功能：
  - 从 CSV 生成 HTML 报告
  - 内置响应式 HTML 模板
  - 支持自定义 Jinja2 模板
  - 数据统计分析：
    - TOP 10 项目卡片
    - 语言分布统计
    - 主题标签统计
    - 完整项目表格
  - 可选的历史对比功能

#### ✅ 9. CLI 命令接口 (cli.py)

**主命令**: `github-trending`

**子命令**:

1. **fetch** - 采集数据
   ```bash
   github-trending fetch [OPTIONS]
   ```
   选项：
   - `-p, --period`: 周期 (daily/weekly/monthly)
   - `-l, --language`: 编程语言筛选
   - `-n, --limit`: 数量限制
   - `-t, --api-token`: GitHub Token
   - `--enrich`: 使用 API 增强数据
   - `--no-report`: 跳过报告生成

2. **report** - 生成报告
   ```bash
   github-trending report -i <csv_file> [OPTIONS]
   ```
   选项：
   - `-i, --input`: 输入 CSV 文件
   - `-o, --output`: 输出 HTML 文件
   - `--template`: 自定义模板目录
   - `-c, --compare`: 对比文件

3. **config-info** - 显示配置
   ```bash
   github-trending config-info
   ```

4. **version** - 版本信息
   ```bash
   github-trending version
   ```

#### ✅ 10. 测试套件

**测试文件**:
- `test_models.py`: 数据模型测试
- `test_config.py`: 配置管理测试
- `test_storage.py`: 数据存储测试
- `conftest.py`: pytest 配置和 fixtures

**测试覆盖**:
- 数据模型验证
- 配置加载优先级
- CSV 读写操作
- 数据序列化/反序列化

#### ✅ 11. 文档

- **README.md**: 项目介绍和使用说明
- **EXAMPLES.md**: 详细使用示例
- **config.yaml.example**: 配置文件示例
- **.env.example**: 环境变量示例
- **install.sh**: 自动安装脚本

## 核心设计特点

### 1. 模块化设计
- 清晰的模块划分
- 低耦合高内聚
- 易于扩展和维护

### 2. 配置灵活性
- 多种配置方式
- 配置优先级明确
- 环境变量支持

### 3. 错误处理
- 完整的异常体系
- 重试机制
- 友好的错误提示

### 4. 数据流程
```
GitHub Trending → Scraper → Projects → API Client → Enriched Data
                                                           ↓
                                                      CSV Handler
                                                           ↓
                                               ┌─────────────────┐
                                               │  CSV Files      │
                                               │  Merged Data    │
                                               └─────────────────┘
                                                           ↓
                                                  HTML Generator
                                                           ↓
                                                   HTML Reports
```

### 5. 扩展点
- 数据源：可添加其他平台（GitLab, Gitee）
- 存储格式：可支持 JSON, SQLite, 数据库
- 报告模板：完全可定制
- 通知方式：邮件、Slack、Webhook

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.8+ |
| CLI 框架 | Click |
| HTTP 请求 | Requests |
| HTML 解析 | BeautifulSoup4 + lxml |
| 模板引擎 | Jinja2 |
| 配置文件 | PyYAML |
| 环境变量 | python-dotenv |
| 测试框架 | pytest |

## 文件统计

```
核心模块文件:
- cli.py              203 行
- models.py           130 行
- config.py           209 行
- exceptions.py        60 行
- trending_scraper.py 261 行
- github_api.py       231 行
- csv_handler.py      273 行
- html_generator.py   605 行

测试文件:
- test_models.py      137 行
- test_config.py       52 行
- test_storage.py     117 行

文档:
- README.md           425 行
- EXAMPLES.md         402 行

总计: ~3000+ 行代码
```

## 依赖包

```
requests>=2.28.0       # HTTP 请求
beautifulsoup4>=4.11.0 # HTML 解析
lxml>=4.9.0            # XML/HTML 解析器
pyyaml>=6.0            # YAML 配置
jinja2>=3.1.0          # 模板引擎
click>=8.1.0           # CLI 框架
python-dotenv>=0.20.0  # 环境变量
pytest>=7.0.0          # 测试框架
pytest-cov>=3.0.0      # 测试覆盖率
```

## 数据格式

### CSV 字段
```
repository_name    - 仓库全名 (owner/repo)
description        - 项目描述
language          - 主要编程语言
stars_total       - 总星标数
stars_period      - 周期内新增星标
forks             - Fork 数量
open_issues       - 开放 Issue 数
created_at        - 创建时间
updated_at        - 更新时间
url               - 仓库 URL
topics            - 项目标签
license           - 许可证
captured_at       - 采集时间
trend_period      - 统计周期
```

### 文件命名规范
```
CSV: trending_{日期}_{周期}.csv
     例: trending_2024-01-15_weekly.csv

HTML: report_{日期}_{周期}.html
      例: report_2024-01-15_weekly.html
```

## 使用流程

### 基础流程
```bash
# 1. 安装
./install.sh

# 2. 配置（可选）
cp .env.example .env
# 编辑 .env 添加 GITHUB_TOKEN

# 3. 采集数据
github-trending fetch --period weekly

# 4. 查看报告
open data/reports/report_*_weekly.html
```

### 高级流程
```bash
# 采集特定语言并增强数据
export GITHUB_TOKEN=your_token
github-trending fetch --period weekly --language python --enrich --limit 50

# 生成对比报告
github-trending report -i current.csv --compare previous.csv

# 自定义配置
github-trending --config my_config.yaml fetch
```

## 性能特点

- **采集速度**: 25 个项目约 30-60 秒
- **API 增强**: 可选，每个项目约 0.5-1 秒
- **CSV 生成**: < 2 秒
- **HTML 生成**: < 5 秒
- **内存占用**: < 100 MB

## 最佳实践

1. **使用 GitHub Token**
   - 提高 API 速率限制
   - 获取完整项目信息

2. **定时采集**
   - 使用 cron 定时任务
   - 推荐每周采集一次

3. **数据备份**
   - 定期备份 CSV 文件
   - 使用版本控制管理配置

4. **日志监控**
   - 定期检查日志文件
   - 关注错误和警告信息

## 未来扩展方向

根据设计文档中的扩展性规划：

### V2 功能
- 数据库存储
- 定时任务调度
- 邮件/Slack 通知
- 多语言并行采集

### V3 功能
- Web 仪表板
- RESTful API
- 趋势预测（机器学习）
- 多平台支持（GitLab, Gitee）

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 编写代码和测试
4. 提交 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件

## 联系方式

- GitHub Issues: https://github.com/yourusername/github-trending/issues
- Email: team@example.com

---

**项目状态**: ✅ 所有核心功能已完成实现

**版本**: v1.0.0

**最后更新**: 2024-01-15
