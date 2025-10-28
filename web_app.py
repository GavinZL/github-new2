"""Interactive Web Application for GitHub Trending.

A Flask-based web application that allows users to manually select parameters
and dynamically fetch GitHub trending projects.
"""

from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
from datetime import datetime
import json

from src.github_trending.models import TrendPeriod
from src.github_trending.collectors import TrendingScraper, GitHubAPIClient
from src.github_trending.storage import CSVHandler
from src.github_trending.reporters import HTMLReportGenerator
from src.github_trending.config import get_config
from src.github_trending.utils import setup_logging, get_logger


# Initialize Flask app
app = Flask(__name__)
setup_logging()
logger = get_logger('web_app')

# Load configuration
config = get_config()


# Language options for the dropdown
LANGUAGE_OPTIONS = [
    {'value': '', 'label': 'All Languages'},
    {'value': 'python', 'label': 'Python'},
    {'value': 'javascript', 'label': 'JavaScript'},
    {'value': 'typescript', 'label': 'TypeScript'},
    {'value': 'java', 'label': 'Java'},
    {'value': 'go', 'label': 'Go'},
    {'value': 'rust', 'label': 'Rust'},
    {'value': 'c++', 'label': 'C++'},
    {'value': 'c', 'label': 'C'},
    {'value': 'c#', 'label': 'C#'},
    {'value': 'php', 'label': 'PHP'},
    {'value': 'ruby', 'label': 'Ruby'},
    {'value': 'swift', 'label': 'Swift'},
    {'value': 'kotlin', 'label': 'Kotlin'},
    {'value': 'scala', 'label': 'Scala'},
    {'value': 'dart', 'label': 'Dart'},
    {'value': 'r', 'label': 'R'},
    {'value': 'shell', 'label': 'Shell'},
    {'value': 'vue', 'label': 'Vue'},
    {'value': 'react', 'label': 'React'},
]


@app.route('/')
def index():
    """Render the main page with selection form."""
    return render_template('index.html', languages=LANGUAGE_OPTIONS)


@app.route('/api/fetch', methods=['POST'])
def fetch_trending():
    """API endpoint to fetch trending projects based on user selection.
    
    Request JSON:
        {
            "period": "daily|weekly|monthly",
            "language": "language_name",
            "limit": 25,
            "enrich": true|false,
            "github_token": "optional_token"
        }
    
    Response JSON:
        {
            "success": true,
            "data": {
                "projects": [...],
                "count": 25,
                "csv_file": "path/to/file.csv",
                "report_file": "path/to/report.html"
            }
        }
    """
    try:
        # Parse request parameters
        params = request.get_json()
        period = params.get('period', 'weekly')
        language = params.get('language', '')
        limit = int(params.get('limit', 25))
        enrich = params.get('enrich', False)
        github_token = params.get('github_token', '') or config.github.api_token
        
        logger.info(f"Fetching trending: period={period}, language={language}, limit={limit}")
        
        # Convert period to enum
        trend_period = TrendPeriod(period)
        
        # Fetch trending projects
        with TrendingScraper() as scraper:
            projects = scraper.fetch_trending(
                period=trend_period,
                language=language if language else None,
                limit=limit
            )
        
        if not projects:
            return jsonify({
                'success': False,
                'error': 'No projects found'
            }), 404
        
        logger.info(f"Fetched {len(projects)} projects")
        
        # Enrich with GitHub API if requested and token available
        if enrich and github_token:
            try:
                logger.info("Enriching projects with GitHub API data...")
                with GitHubAPIClient(api_token=github_token) as api_client:
                    projects = api_client.enrich_projects_batch(projects)
                logger.info("Enrichment completed")
            except Exception as e:
                logger.warning(f"Enrichment failed: {e}")
                # Continue without enrichment
        
        # Save to CSV
        csv_handler = CSVHandler()
        csv_file = csv_handler.save_projects(projects)
        
        # Generate HTML report
        report_generator = HTMLReportGenerator()
        report_file = report_generator.generate_report(csv_file)
        
        # Convert projects to JSON-serializable format
        projects_data = []
        for project in projects:
            projects_data.append({
                'repository_name': project.repository_name,
                'description': project.description,
                'language': project.language,
                'stars_total': project.stars_total,
                'stars_period': project.stars_period,
                'forks': project.forks,
                'open_issues': project.open_issues,
                'url': project.url,
                'topics': project.topics,
                'license': project.license,
                'created_at': project.created_at.isoformat() if project.created_at else None,
                'updated_at': project.updated_at.isoformat() if project.updated_at else None,
            })
        
        return jsonify({
            'success': True,
            'data': {
                'projects': projects_data,
                'count': len(projects),
                'csv_file': str(csv_file),
                'report_file': str(report_file),
                'period': period,
                'language': language or 'all'
            }
        })
        
    except Exception as e:
        logger.exception(f"Error fetching trending: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/report/<path:filename>')
def get_report(filename):
    """Serve generated HTML report."""
    try:
        report_path = config.storage.reports_dir / filename
        if not report_path.exists():
            return jsonify({'error': 'Report not found'}), 404
        
        return send_file(report_path, mimetype='text/html')
    except Exception as e:
        logger.exception(f"Error serving report: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat()
    })


def main():
    """Run the Flask application."""
    print("🚀 Starting GitHub Trending Web Application...")
    print(f"📂 Data directory: {config.storage.data_dir}")
    print(f"🔑 GitHub Token: {'✓ Configured' if config.github.api_token else '✗ Not configured'}")
    print("\n💡 Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
