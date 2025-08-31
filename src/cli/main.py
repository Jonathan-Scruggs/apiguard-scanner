"""
APiGuard - API Security Scanner
Entry point for CLI with enhanced visual experience
"""
import click
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn # Later For Actual Scan progress
from rich.text import Text
from rich.syntax import Syntax
from rich.align import Align

from core.engine.engine import SecurityScanner
from core.parsers.openapi_parser import OpenAPIParser
console = Console()

LOGO = """
 █████╗ ██████╗ ██╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██║██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
███████║██████╔╝██║██║  ███╗██║   ██║███████║██████╔╝██║  ██║
██╔══██║██╔═══╝ ██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
██║  ██║██║     ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
"""

def print_banner():
    """Display the APiGuard banner with styling"""
    
    console.clear()
    console.print()

    logo_text = Text(LOGO)
    logo_text.stylize("bold cyan")
    console.print(Align.left(logo_text))
    
    subtitle = Text("API Security Scanner")
    subtitle.stylize("bold magenta")
    console.print(Align.left(subtitle))
    
    version_text = Text("v0.1.0-alpha")
    version_text.stylize("bold yellow")
    console.print(Align.left(version_text))
    
    tagline = Text("Secure your APIs with confidence")
    tagline.stylize("dim italic")
    console.print(Align.left(tagline))
    
    console.print()
    console.print(Align.left("─" * 60), style="dim cyan")
    console.print()
def print_status(message, status="info", verbose=False):
    """Enhanced status messages with icons and colors"""
    if not verbose:
        return
    
    styles = {
        "success": ("✅", "bold green"),
        "error": ("❌", "bold red"), 
        "warning": ("⚠️ ", "bold yellow"),
        "info": ("ℹ️ ", "bold blue"),
        "scanning": ("🔍", "bold cyan"),
        "loading": ("⏳", "bold purple"),
        "security": ("🔒", "bold red"),
        "found": ("🎯", "bold yellow")
    }
    
    icon, style = styles.get(status, ("•", "white"))
    console.print(f"{icon} {message}", style=style)
    
   
def show_scan_summary(spec_file, target, output_format, concurrent, timeout):
    """Displays scan configuration summary"""

    table = Table(title="🔍 Scan Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="cyan", width=15)
    table.add_column("Value", style="white")
    
    table.add_row("Spec File", str(spec_file))
    table.add_row("Target URL", target)
    table.add_row("Output Format", output_format.upper())
    table.add_row("Concurrent Requests", str(concurrent))
    table.add_row("Timeout", f"{timeout}s")
    
    console.print(table)
    console.print()

@click.command()
@click.argument('spec_path', type=click.Path(exists=True))
@click.option('--target', '-t', required=True, help='Target API base URL (e.g., https://api.example.com)')
@click.option('--output', '-o', type=click.Path(), help='Output file for results (JSON format)')
@click.option('--format', '-f', type=click.Choice(['json', 'text', 'html']), default='text', help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output with detailed progress') 
@click.option('--timeout', default=30, help='Request timeout in seconds')
@click.option('--concurrent', '-c', default=10, help='Max concurrent requests')

async def scan(spec_path, target, output, format, verbose, timeout, concurrent):
    """
    Scans an API for security vulnerabilities. 

    \b
    SPEC_PATH: Path to your OpenAPI/Swagger specification file
    \b
    Examples:
      apiguard api-spec.yaml --target https://api.example.com
      apiguard api.yaml -t https://api.com -c 20 --timeout 60 --verbose
    """
        
    # Validate inputs
    spec_file = Path(spec_path)
    if not spec_file.exists():
        print_status(f"Specification file not found: {spec_path}", "error", True)
        sys.exit(1)
    
    # Showing the users selected configuration 
    if verbose:
        show_scan_summary(spec_file, target, format, concurrent, timeout)
    
  
  
    if not click.confirm("Start the security scan?"):
        print_status("Scan cancelled by user", "warning", True)
        return
    
    print_status("Starting APiGuard security scan...", "loading", verbose)
    
    

    open_api_parser = OpenAPIParser(file_path=spec_path, base_url=target)
    api_spec = open_api_parser.parse()
    
    print_status("Security scan completed successfully!", "success", True)
    
    
        
    
    # TODO 
    output_file = output or f"apiguard-report.{format}"
    print_status(f"Report saved to: {output_file}", "success", True)


# Create a command group for multiple subcommands
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """APiGuard - API Security Scanner"""
    print_banner()
    if ctx.invoked_subcommand is None:
        # Show interactive menu or help
        console.print(ctx.get_help())
cli.add_command(scan)

if __name__ == '__main__':
    cli(ctx={'max_content_width': 120})