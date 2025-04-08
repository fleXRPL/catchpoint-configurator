"""
Command-line interface for Catchpoint Configurator.
"""

import logging
from typing import Optional

import click
from click import Context

from .core import CatchpointConfigurator

logger = logging.getLogger(__name__)


def get_client(ctx: Context) -> CatchpointConfigurator:
    """Get a CatchpointConfigurator instance from context.

    Args:
        ctx: Click context

    Returns:
        CatchpointConfigurator instance
    """
    return ctx.ensure_object(CatchpointConfigurator)


@click.group()
@click.option(
    "--client-id",
    envvar="CATCHPOINT_CLIENT_ID",
    help="Catchpoint API client ID",
    required=True,
)
@click.option(
    "--client-secret",
    envvar="CATCHPOINT_CLIENT_SECRET",
    help="Catchpoint API client secret",
    required=True,
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug logging",
)
@click.option(
    "--timeout",
    type=int,
    default=30,
    help="API request timeout in seconds",
)
@click.pass_context
def cli(
    ctx: Context,
    client_id: str,
    client_secret: str,
    debug: bool,
    timeout: int,
) -> None:
    """Catchpoint Configurator CLI."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    ctx.obj = CatchpointConfigurator(
        client_id=client_id,
        client_secret=client_secret,
        debug=debug,
        timeout=timeout,
    )


@cli.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="Validate but don't deploy",
)
@click.option(
    "--force/--no-force",
    default=False,
    help="Overwrite existing configurations",
)
@click.pass_context
def deploy(
    ctx: Context,
    config_path: str,
    dry_run: bool,
    force: bool,
) -> None:
    """Deploy a configuration to Catchpoint."""
    try:
        result = get_client(ctx).deploy(
            config_path=config_path,
            dry_run=dry_run,
            force=force,
        )
        click.echo(f"Deployment result: {result}")
    except Exception as e:
        raise click.ClickException(f"Deployment failed: {e}")


@cli.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.pass_context
def validate(ctx: Context, config_path: str) -> None:
    """Validate a configuration file."""
    try:
        get_client(ctx).validate(config_path)
        click.echo("Configuration is valid")
    except Exception as e:
        raise click.ClickException(f"Validation failed: {e}")


@cli.command()
@click.option(
    "--type",
    help="Filter by configuration type",
)
@click.pass_context
def list(ctx: Context, type: Optional[str]) -> None:
    """List existing configurations."""
    try:
        configs = get_client(ctx).list(config_type=type)
        for config in configs:
            click.echo(f"- {config['name']} ({config['type']})")
    except Exception as e:
        raise click.ClickException(f"Failed to list configurations: {e}")


@cli.command()
@click.argument("template_name")
@click.argument("variables", type=click.Path(exists=True))
@click.option(
    "--output",
    help="Path to save the rendered configuration",
)
@click.pass_context
def apply_template(
    ctx: Context,
    template_name: str,
    variables: str,
    output: Optional[str],
) -> None:
    """Apply a template with variables."""
    try:
        result = get_client(ctx).apply_template(
            template_name=template_name,
            variables=variables,
            output_path=output,
        )
        if not output:
            click.echo(result)
    except Exception as e:
        raise click.ClickException(f"Template application failed: {e}")


@cli.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.argument("updates", type=click.Path(exists=True))
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="Show what would be updated",
)
@click.pass_context
def update(
    ctx: Context,
    config_path: str,
    updates: str,
    dry_run: bool,
) -> None:
    """Update an existing configuration."""
    try:
        result = get_client(ctx).update(
            config_path=config_path,
            updates=updates,
            dry_run=dry_run,
        )
        click.echo(f"Update result: {result}")
    except Exception as e:
        raise click.ClickException(f"Update failed: {e}")


@cli.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="Show what would be deleted",
)
@click.pass_context
def delete(
    ctx: Context,
    config_path: str,
    dry_run: bool,
) -> None:
    """Delete a configuration."""
    try:
        result = get_client(ctx).delete(
            config_path=config_path,
            dry_run=dry_run,
        )
        click.echo(f"Deletion result: {result}")
    except Exception as e:
        raise click.ClickException(f"Deletion failed: {e}")


@cli.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "--output",
    help="Path to save the export",
)
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Export format",
)
@click.pass_context
def export(
    ctx: Context,
    config_path: str,
    output: Optional[str],
    format: str,
) -> None:
    """Export a configuration."""
    try:
        result = get_client(ctx).export(
            config_path=config_path,
            output_path=output,
            format=format,
        )
        if not output:
            click.echo(result)
    except Exception as e:
        raise click.ClickException(f"Export failed: {e}")


@cli.command()
@click.argument("import_path", type=click.Path(exists=True))
@click.option(
    "--output",
    help="Path to save the imported configuration",
)
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Import format",
)
@click.pass_context
def import_config(
    ctx: Context,
    import_path: str,
    output: Optional[str],
    format: str,
) -> None:
    """Import a configuration."""
    try:
        result = get_client(ctx).import_config(
            import_path=import_path,
            output_path=output,
            format=format,
        )
        if not output:
            click.echo(result)
    except Exception as e:
        raise click.ClickException(f"Import failed: {e}")


def main() -> None:
    """Entry point for the CLI."""
    cli(obj={})
