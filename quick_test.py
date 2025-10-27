#!/usr/bin/env python3
"""
快速测试脚本 - 验证系统各模块是否正常工作
"""

import sys
from pathlib import Path

# 添加 src 到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """测试所有模块是否可以正常导入"""
    print("测试模块导入...")
    try:
        from github_trending import __version__
        from github_trending.models import TrendingProject, TrendPeriod
        from github_trending.config import Config, get_config
        from github_trending.exceptions import GitHubTrendingError
        from github_trending.collectors import TrendingScraper, GitHubAPIClient
        from github_trending.storage import CSVHandler
        from github_trending.reporters import HTMLReportGenerator
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False


def test_config():
    """测试配置系统"""
    print("\n测试配置系统...")
    try:
        from github_trending.config import Config
        
        config = Config()
        assert config.github.api_base_url == "https://api.github.com"
        assert config.github.timeout == 30
        assert config.storage.data_dir == "./data"
        
        print("✓ 配置系统正常")
        return True
    except Exception as e:
        print(f"✗ 配置系统测试失败: {e}")
        return False


def test_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    try:
        from github_trending.models import TrendingProject, TrendPeriod
        from datetime import datetime
        
        # 创建项目实例
        project = TrendingProject(
            repository_name="test/repo",
            url="https://github.com/test/repo",
            stars_total=1000,
            stars_period=100,
            captured_at=datetime.utcnow(),
            trend_period=TrendPeriod.WEEKLY
        )
        
        # 测试验证
        assert project.validate() is True
        
        # 测试序列化
        data = project.to_dict()
        assert data['repository_name'] == "test/repo"
        assert data['trend_period'] == "weekly"
        
        # 测试反序列化
        project2 = TrendingProject.from_dict(data)
        assert project2.repository_name == project.repository_name
        
        print("✓ 数据模型正常")
        return True
    except Exception as e:
        print(f"✗ 数据模型测试失败: {e}")
        return False


def test_csv_handler():
    """测试 CSV 处理"""
    print("\n测试 CSV 处理...")
    try:
        from github_trending.storage import CSVHandler
        from github_trending.models import TrendingProject, TrendPeriod
        from datetime import datetime
        import tempfile
        
        # 创建测试数据
        projects = [
            TrendingProject(
                repository_name="test/repo1",
                url="https://github.com/test/repo1",
                stars_total=1000,
                stars_period=100,
                captured_at=datetime.utcnow(),
                trend_period=TrendPeriod.WEEKLY
            )
        ]
        
        # 测试保存和加载
        handler = CSVHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            csv_file = handler.save_projects(projects, output_dir=output_dir)
            
            assert csv_file.exists()
            
            loaded_projects = handler.load_projects(csv_file)
            assert len(loaded_projects) == 1
            assert loaded_projects[0].repository_name == "test/repo1"
        
        print("✓ CSV 处理正常")
        return True
    except Exception as e:
        print(f"✗ CSV 处理测试失败: {e}")
        return False


def test_exceptions():
    """测试异常系统"""
    print("\n测试异常系统...")
    try:
        from github_trending.exceptions import (
            GitHubTrendingError,
            NetworkError,
            ValidationError
        )
        
        # 测试异常继承
        assert issubclass(NetworkError, GitHubTrendingError)
        assert issubclass(ValidationError, GitHubTrendingError)
        
        # 测试异常抛出和捕获
        try:
            raise ValidationError("Test error")
        except GitHubTrendingError as e:
            assert str(e) == "Test error"
        
        print("✓ 异常系统正常")
        return True
    except Exception as e:
        print(f"✗ 异常系统测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("GitHub Trending 系统快速测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_models,
        test_csv_handler,
        test_exceptions,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"测试结果: {sum(results)}/{len(results)} 通过")
    
    if all(results):
        print("✅ 所有测试通过！系统可以正常使用。")
        print("\n下一步:")
        print("  1. 运行: python3 -m pip install -e .")
        print("  2. 配置: cp .env.example .env")
        print("  3. 使用: github-trending fetch --period weekly")
        return 0
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
