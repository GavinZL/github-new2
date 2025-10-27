#!/bin/bash

# GitHub Trending 快速安装脚本

set -e

echo "📦 开始安装 GitHub Trending 数据采集系统..."

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ 检测到 Python 版本: $PYTHON_VERSION"

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境? (推荐) [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
fi

# 安装依赖
echo "📦 安装依赖包..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 安装工具
echo "🔧 安装 GitHub Trending 工具..."
python3 -m pip install -e .

# 创建配置文件
if [ ! -f config.yaml ]; then
    echo "📝 创建配置文件..."
    cp config.yaml.example config.yaml
    echo "✓ 已创建 config.yaml，请根据需要修改"
fi

# 创建环境变量文件
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ 已创建 .env 文件，请添加您的 GitHub Token"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用说明："
echo "  1. 编辑 config.yaml 或 .env 文件，添加 GitHub API Token（可选）"
echo "  2. 运行: github-trending fetch --period weekly"
echo "  3. 查看生成的报告: data/reports/"
echo ""
echo "💡 更多命令:"
echo "  github-trending --help        查看所有命令"
echo "  github-trending fetch --help  查看 fetch 命令帮助"
echo "  github-trending config-info   查看当前配置"
echo ""
