"""HTML report generator for trending data."""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import Counter
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from ..models import TrendingProject, ReportMetadata, TrendPeriod
from ..storage import CSVHandler
from ..exceptions import ReportGenerationError, TemplateError
from ..config import get_config
from ..utils import get_logger


logger = get_logger('reporters.html_generator')


class HTMLReportGenerator:
    """Generator for HTML reports from trending data."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """Initialize the report generator.
        
        Args:
            template_dir: Directory containing templates
        """
        config = get_config()
        self.template_dir = Path(template_dir or config.report.template_dir)
        self.storage_config = config.storage
        
        # Setup Jinja2 environment
        if self.template_dir.exists():
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=select_autoescape(['html', 'xml'])
            )
        else:
            self.env = None
            logger.warning(f"Template directory not found: {self.template_dir}, will use built-in template")
    
    def generate_report(
        self,
        csv_file: Path,
        output_file: Optional[Path] = None,
        compare_file: Optional[Path] = None
    ) -> Path:
        """Generate HTML report from CSV data.
        
        Args:
            csv_file: Input CSV file path
            output_file: Output HTML file path (auto-generated if not provided)
            compare_file: Optional CSV file for comparison
            
        Returns:
            Path to generated HTML report
            
        Raises:
            ReportGenerationError: If report generation fails
        """
        logger.info(f"Generating report from {csv_file}")
        
        try:
            # Load projects
            csv_handler = CSVHandler()
            projects = csv_handler.load_projects(csv_file)
            
            if not projects:
                raise ReportGenerationError("No projects found in CSV file")
            
            # Load comparison data if provided
            compare_projects = None
            if compare_file and compare_file.exists():
                compare_projects = csv_handler.load_projects(compare_file)
            
            # Generate report metadata
            metadata = self._create_metadata(projects, str(csv_file))
            
            # Prepare report data
            report_data = self._prepare_report_data(projects, compare_projects)
            
            # Render template
            html_content = self._render_template(metadata, report_data)
            
            # Determine output path
            if not output_file:
                output_file = self._generate_output_path(csv_file)
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write HTML file
            output_file.write_text(html_content, encoding='utf-8')
            
            logger.info(f"Report generated successfully: {output_file}")
            return output_file
            
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate report: {e}") from e
    
    def _create_metadata(self, projects: List[TrendingProject], source_file: str) -> ReportMetadata:
        """Create report metadata.
        
        Args:
            projects: List of projects
            source_file: Source CSV file path
            
        Returns:
            ReportMetadata instance
        """
        dates = [p.captured_at for p in projects if p.captured_at]
        
        return ReportMetadata(
            generated_at=datetime.utcnow(),
            period=projects[0].trend_period if projects else TrendPeriod.WEEKLY,
            total_projects=len(projects),
            data_source=source_file,
            date_range_start=min(dates) if dates else None,
            date_range_end=max(dates) if dates else None
        )
    
    def _prepare_report_data(
        self,
        projects: List[TrendingProject],
        compare_projects: Optional[List[TrendingProject]] = None
    ) -> Dict[str, Any]:
        """Prepare data for report template.
        
        Args:
            projects: List of projects
            compare_projects: Optional list for comparison
            
        Returns:
            Dictionary of report data
        """
        # Sort projects by stars in period (descending)
        sorted_projects = sorted(projects, key=lambda p: p.stars_period, reverse=True)
        
        # Get top 10 projects
        top_projects = sorted_projects[:10]
        
        # Calculate language statistics
        language_stats = self._calculate_language_stats(projects)
        
        # Calculate topic statistics
        topic_stats = self._calculate_topic_stats(projects)
        
        # Prepare comparison data if available
        comparison = None
        if compare_projects:
            comparison = self._prepare_comparison(projects, compare_projects)
        
        return {
            'all_projects': sorted_projects,
            'top_projects': top_projects,
            'language_stats': language_stats,
            'topic_stats': topic_stats,
            'comparison': comparison
        }
    
    def _calculate_language_stats(self, projects: List[TrendingProject]) -> List[Dict[str, Any]]:
        """Calculate language distribution statistics.
        
        Args:
            projects: List of projects
            
        Returns:
            List of language statistics
        """
        languages = [p.language for p in projects if p.language]
        counter = Counter(languages)
        
        total = len(languages)
        stats = []
        
        for language, count in counter.most_common(10):
            percentage = (count / total * 100) if total > 0 else 0
            stats.append({
                'name': language,
                'count': count,
                'percentage': round(percentage, 1)
            })
        
        return stats
    
    def _calculate_topic_stats(self, projects: List[TrendingProject]) -> List[Dict[str, Any]]:
        """Calculate topic statistics.
        
        Args:
            projects: List of projects
            
        Returns:
            List of topic statistics
        """
        all_topics = []
        for project in projects:
            if project.topics:  # Check if topics is not None or empty
                all_topics.extend(project.topics)
        
        counter = Counter(all_topics)
        
        stats = []
        for topic, count in counter.most_common(15):
            stats.append({
                'name': topic,
                'count': count
            })
        
        return stats
    
    def _prepare_comparison(
        self,
        current_projects: List[TrendingProject],
        previous_projects: List[TrendingProject]
    ) -> Dict[str, Any]:
        """Prepare comparison data.
        
        Args:
            current_projects: Current period projects
            previous_projects: Previous period projects
            
        Returns:
            Comparison data dictionary
        """
        current_repos = {p.repository_name for p in current_projects}
        previous_repos = {p.repository_name for p in previous_projects}
        
        new_entries = current_repos - previous_repos
        dropped = previous_repos - current_repos
        
        return {
            'new_entries': len(new_entries),
            'dropped': len(dropped),
            'continued': len(current_repos & previous_repos)
        }
    
    def _render_template(self, metadata: ReportMetadata, data: Dict[str, Any]) -> str:
        """Render HTML template with data.
        
        Args:
            metadata: Report metadata
            data: Report data
            
        Returns:
            Rendered HTML string
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            # Try to load custom template
            if self.env:
                try:
                    template = self.env.get_template('report.html')
                    return template.render(metadata=metadata, **data)
                except Exception as e:
                    logger.warning(f"Failed to load custom template: {e}, using built-in")
            
            # Use built-in template
            template = Template(self._get_builtin_template())
            return template.render(metadata=metadata, **data)
            
        except Exception as e:
            raise TemplateError(f"Template rendering failed: {e}") from e
    
    def _generate_output_path(self, csv_file: Path) -> Path:
        """Generate output file path based on CSV file.
        
        Args:
            csv_file: Source CSV file
            
        Returns:
            Output HTML file path
        """
        # Extract date and period from filename
        # Format: trending_2024-01-15_weekly.csv
        stem = csv_file.stem  # trending_2024-01-15_weekly
        html_name = f"report_{stem.replace('trending_', '')}.html"
        
        return self.storage_config.reports_dir / html_name
    
    def _get_builtin_template(self) -> str:
        """Get built-in HTML template.
        
        Returns:
            HTML template string
        """
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending Report - {{ metadata.period.value|title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background: #f6f8fa;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        header {
            border-bottom: 2px solid #e1e4e8;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #0366d6;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .meta-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
            padding: 20px;
            background: #f6f8fa;
            border-radius: 6px;
        }
        
        .meta-item {
            padding: 10px;
        }
        
        .meta-label {
            font-weight: bold;
            color: #586069;
            font-size: 0.9em;
        }
        
        .meta-value {
            color: #24292e;
            font-size: 1.1em;
            margin-top: 5px;
        }
        
        h2 {
            color: #24292e;
            font-size: 1.8em;
            margin: 30px 0 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e1e4e8;
        }
        
        .project-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .project-card {
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 20px;
            transition: box-shadow 0.2s;
        }
        
        .project-card:hover {
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        }
        
        .project-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .project-title a {
            color: #0366d6;
            text-decoration: none;
        }
        
        .project-title a:hover {
            text-decoration: underline;
        }
        
        .project-desc {
            color: #586069;
            font-size: 0.95em;
            margin: 10px 0;
            line-height: 1.5;
        }
        
        .project-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 15px;
            font-size: 0.9em;
        }
        
        .meta-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 8px;
            background: #f6f8fa;
            border-radius: 3px;
            color: #586069;
        }
        
        .language-badge {
            background: #0366d6;
            color: white;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-card {
            padding: 15px;
            background: #f6f8fa;
            border-radius: 6px;
            border-left: 4px solid #0366d6;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #0366d6;
        }
        
        .stat-label {
            color: #586069;
            margin-top: 5px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        thead {
            background: #f6f8fa;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e1e4e8;
        }
        
        th {
            font-weight: 600;
            color: #24292e;
        }
        
        tbody tr:hover {
            background: #f6f8fa;
        }
        
        .table-number {
            text-align: right;
            font-family: 'Courier New', monospace;
        }
        
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e1e4e8;
            color: #586069;
            text-align: center;
            font-size: 0.9em;
        }
        
        @media print {
            body {
                background: white;
            }
            .container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 GitHub Trending Report</h1>
            <p style="color: #586069; font-size: 1.1em;">
                {{ metadata.period.value|title }} Period Analysis
            </p>
        </header>
        
        <div class="meta-info">
            <div class="meta-item">
                <div class="meta-label">Generated At</div>
                <div class="meta-value">{{ metadata.generated_at.strftime('%Y-%m-%d %H:%M UTC') }}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Total Projects</div>
                <div class="meta-value">{{ metadata.total_projects }}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Period</div>
                <div class="meta-value">{{ metadata.period.value|title }}</div>
            </div>
            {% if metadata.date_range_start %}
            <div class="meta-item">
                <div class="meta-label">Data Range</div>
                <div class="meta-value">{{ metadata.date_range_start.strftime('%Y-%m-%d') }}</div>
            </div>
            {% endif %}
        </div>
        
        <section>
            <h2>🏆 Top 10 Trending Projects</h2>
            <div class="project-grid">
                {% for project in top_projects %}
                <div class="project-card">
                    <div class="project-title">
                        <a href="{{ project.url }}" target="_blank">{{ project.repository_name }}</a>
                    </div>
                    {% if project.description %}
                    <div class="project-desc">{{ project.description }}</div>
                    {% endif %}
                    <div class="project-meta">
                        {% if project.language %}
                        <span class="meta-badge language-badge">{{ project.language }}</span>
                        {% endif %}
                        <span class="meta-badge">⭐ {{ project.stars_total }}</span>
                        <span class="meta-badge">📈 +{{ project.stars_period }} this {{ metadata.period.value }}</span>
                        <span class="meta-badge">🍴 {{ project.forks }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
        
        {% if language_stats %}
        <section>
            <h2>💻 Language Distribution</h2>
            <div class="stats-grid">
                {% for stat in language_stats[:5] %}
                <div class="stat-card">
                    <div class="stat-value">{{ stat.count }}</div>
                    <div class="stat-label">{{ stat.name }} ({{ stat.percentage }}%)</div>
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}
        
        <section>
            <h2>📋 Complete Project List</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Repository</th>
                        <th>Language</th>
                        <th class="table-number">Stars</th>
                        <th class="table-number">Period +</th>
                        <th class="table-number">Forks</th>
                    </tr>
                </thead>
                <tbody>
                    {% for project in all_projects %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>
                            <a href="{{ project.url }}" target="_blank">{{ project.repository_name }}</a>
                        </td>
                        <td>{{ project.language or '-' }}</td>
                        <td class="table-number">{{ project.stars_total }}</td>
                        <td class="table-number">{{ project.stars_period }}</td>
                        <td class="table-number">{{ project.forks }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        
        <footer>
            <p>Generated by GitHub Trending Data Collection System</p>
            <p>Data Source: {{ metadata.data_source }}</p>
        </footer>
    </div>
</body>
</html>"""
