"""Command-line interface for GitHub Trending tool."""

import sys
from pathlib import Path
import click

from .models import TrendPeriod
from .config import get_config
from .collectors import TrendingScraper, GitHubAPIClient
from .storage import CSVHandler
from .reporters import HTMLReportGenerator
from .utils import setup_logging, get_logger
from .exceptions import GitHubTrendingError


@click.group()
@click.option('--config', type=click.Path(exists=True), help='Path to configuration file')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), help='Log level')
@click.pass_context
def cli(ctx, config, log_level):
    """GitHub Trending Data Collection System.
    
    A CLI tool to collect and analyze GitHub trending projects.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Load configuration
    ctx.obj['config'] = get_config(config)
    
    # Setup logging
    setup_logging(log_level=log_level)


@cli.command()
@click.option('-p', '--period', type=click.Choice(['daily', 'weekly', 'monthly']), 
              default='weekly', help='Trend period')
@click.option('-l', '--language', type=str, help='Filter by programming language')
@click.option('-o', '--output', type=click.Path(), help='Output directory')
@click.option('-t', '--api-token', type=str, envvar='GITHUB_TOKEN', 
              help='GitHub API token (or set GITHUB_TOKEN env var)')
@click.option('--no-report', is_flag=True, help='Skip report generation')
@click.option('-n', '--limit', type=int, default=25, help='Maximum number of projects to fetch')
@click.option('--enrich', is_flag=True, default=True, help='Enrich data with GitHub API')
@click.pass_context
def fetch(ctx, period, language, output, api_token, no_report, limit, enrich):
    """Fetch and store GitHub Trending data.
    
    Examples:
        github-trending fetch --period weekly
        github-trending fetch --period daily --language python
        github-trending fetch --limit 50 --no-report
    """
    logger = get_logger('cli.fetch')
    
    try:
        # Convert period string to enum
        trend_period = TrendPeriod(period)
        
        logger.info(f"Fetching {period} trending projects...")
        if language:
            logger.info(f"Filtering by language: {language}")
        
        # Fetch trending projects
        with TrendingScraper() as scraper:
            projects = scraper.fetch_trending(
                period=trend_period,
                language=language,
                limit=limit
            )
        
        if not projects:
            click.echo("⚠️  No projects found.", err=True)
            sys.exit(1)
        
        click.echo(f"✓ Fetched {len(projects)} trending projects")
        
        # Enrich with API data if requested
        if enrich and api_token:
            logger.info("Enriching projects with GitHub API data...")
            with GitHubAPIClient(api_token=api_token) as api_client:
                projects = api_client.enrich_projects_batch(projects)
            click.echo(f"✓ Enriched projects with detailed information")
        
        # Save to CSV
        csv_handler = CSVHandler()
        output_dir = Path(output) if output else None
        csv_file = csv_handler.save_projects(projects, output_dir=output_dir)
        
        click.echo(f"✓ Saved data to: {csv_file}")
        
        # Generate report unless disabled
        if not no_report:
            logger.info("Generating HTML report...")
            report_generator = HTMLReportGenerator()
            report_file = report_generator.generate_report(csv_file)
            click.echo(f"✓ Generated report: {report_file}")
        
        click.echo("\n✅ Success!")
        
    except GitHubTrendingError as e:
        logger.error(f"Error: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('-i', '--input', 'input_file', required=True, type=click.Path(exists=True),
              help='Input CSV file path')
@click.option('-o', '--output', type=click.Path(), help='Output HTML file path')
@click.option('--template', type=click.Path(exists=True), help='Custom HTML template directory')
@click.option('-c', '--compare', type=click.Path(exists=True), 
              help='Compare with another CSV file')
@click.pass_context
def report(ctx, input_file, output, template, compare):
    """Generate HTML report from CSV data.
    
    Examples:
        github-trending report -i data/raw/trending_2024-01-15_weekly.csv
        github-trending report -i data.csv -o report.html
        github-trending report -i current.csv --compare previous.csv
    """
    logger = get_logger('cli.report')
    
    try:
        csv_file = Path(input_file)
        output_file = Path(output) if output else None
        compare_file = Path(compare) if compare else None
        
        logger.info(f"Generating report from {csv_file}")
        
        report_generator = HTMLReportGenerator(template_dir=template)
        report_path = report_generator.generate_report(
            csv_file=csv_file,
            output_file=output_file,
            compare_file=compare_file
        )
        
        click.echo(f"✓ Report generated: {report_path}")
        click.echo("✅ Success!")
        
    except GitHubTrendingError as e:
        logger.error(f"Error: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def config_info(ctx):
    """Display current configuration."""
    config = ctx.obj['config']
    
    click.echo("\n📋 Current Configuration:\n")
    
    click.echo("GitHub API:")
    click.echo(f"  Base URL: {config.github.api_base_url}")
    click.echo(f"  Token: {'✓ Set' if config.github.api_token else '✗ Not set'}")
    click.echo(f"  Timeout: {config.github.timeout}s")
    
    click.echo("\nStorage:")
    click.echo(f"  Data Directory: {config.storage.data_dir}")
    click.echo(f"  Encoding: {config.storage.encoding}")
    
    click.echo("\nReport:")
    click.echo(f"  Template Directory: {config.report.template_dir}")
    click.echo(f"  Auto Generate: {config.report.auto_generate}")
    
    click.echo("\nLogging:")
    click.echo(f"  Level: {config.logging.level}")
    click.echo(f"  File: {config.logging.file}")
    
    click.echo()


@cli.command()
@click.pass_context
def version(ctx):
    """Display version information."""
    from . import __version__
    click.echo(f"GitHub Trending v{__version__}")


def main():
    """Main entry point."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Interrupted by user", err=True)
        sys.exit(130)


if __name__ == '__main__':
    main()
