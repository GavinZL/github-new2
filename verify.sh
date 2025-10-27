#!/bin/bash

# GitHub Trending 项目验证脚本

echo "================================"
echo "GitHub Trending 项目文件验证"
echo "================================"
echo ""

# 检查核心文件
echo "✓ 检查核心文件..."

files=(
    "README.md"
    "setup.py"
    "requirements.txt"
    "src/github_trending/__init__.py"
    "src/github_trending/cli.py"
    "src/github_trending/models.py"
    "src/github_trending/config.py"
    "src/github_trending/exceptions.py"
    "src/github_trending/collectors/__init__.py"
    "src/github_trending/collectors/trending_scraper.py"
    "src/github_trending/collectors/github_api.py"
    "src/github_trending/storage/__init__.py"
    "src/github_trending/storage/csv_handler.py"
    "src/github_trending/reporters/__init__.py"
    "src/github_trending/reporters/html_generator.py"
    "src/github_trending/utils/__init__.py"
    "tests/__init__.py"
    "tests/test_models.py"
    "tests/test_config.py"
    "tests/test_storage.py"
)

missing=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (缺失)"
        ((missing++))
    fi
done

echo ""
echo "✓ 检查文档文件..."

docs=(
    "README.md"
    "EXAMPLES.md"
    "PROJECT_OVERVIEW.md"
    "IMPLEMENTATION_SUMMARY.md"
    "DELIVERY_CHECKLIST.md"
    "LICENSE"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        size=$(wc -c < "$doc" | tr -d ' ')
        lines=$(wc -l < "$doc" | tr -d ' ')
        echo "  ✓ $doc ($lines 行, $size 字节)"
    else
        echo "  ✗ $doc (缺失)"
        ((missing++))
    fi
done

echo ""
echo "✓ 检查目录结构..."

dirs=(
    "src/github_trending"
    "src/github_trending/collectors"
    "src/github_trending/storage"
    "src/github_trending/reporters"
    "src/github_trending/utils"
    "tests"
    "data/raw"
    "data/merged"
    "data/reports"
    "logs"
    "templates"
)

for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir/"
    else
        echo "  ✗ $dir/ (缺失)"
        ((missing++))
    fi
done

echo ""
echo "================================"

if [ $missing -eq 0 ]; then
    echo "✅ 所有文件检查通过！"
    echo ""
    echo "项目统计:"
    echo "  Python 文件: $(find src -name "*.py" | wc -l)"
    echo "  测试文件: $(find tests -name "*.py" | wc -l)"
    echo "  文档文件: $(ls *.md 2>/dev/null | wc -l)"
    echo ""
    echo "下一步:"
    echo "  1. ./install.sh - 安装系统"
    echo "  2. python3 quick_test.py - 运行测试"
    echo "  3. github-trending --help - 查看帮助"
    exit 0
else
    echo "❌ 发现 $missing 个缺失文件"
    exit 1
fi
