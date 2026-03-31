#!/bin/bash

# GitHub Trending Web Application Startup Script
# 启动GitHub Trending交互式网页应用

echo "🚀 GitHub Trending Web Application"
echo "===================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "⚠️  Flask not found, installing..."
    pip install -q flask>=2.3.0
fi

echo "✓ All dependencies installed"

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p data/raw data/merged data/reports logs templates

echo "✓ Directories ready"

# Check for GitHub token
echo ""
if [ -z "$GITHUB_TOKEN" ]; then
    echo "💡 提示: 未设置 GITHUB_TOKEN 环境变量"
    echo "   您可以在网页中输入Token，或通过以下方式设置:"
    echo "   export GITHUB_TOKEN=ghp_your_token_here"
else
    echo "✓ GitHub Token 已配置"
fi

# Start the web application
echo ""
echo "======================================"
echo "🌐 启动Web应用..."
echo "======================================"
echo ""
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""
echo "--------------------------------------"
echo ""

python3 web_app.py
