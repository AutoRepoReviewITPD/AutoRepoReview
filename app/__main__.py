import getpass

import typer
from opentelemetry import trace

from .config import config
from .services.git_service import GitService
from .services.summarize_service import SummarizeService
from .telemetry import setup_telemetry

# Initialize telemetry
setup_telemetry()

tracer = trace.get_tracer(__name__)

app = typer.Typer()

git_service = GitService()


@app.command()
def summary(path: str, start_commit: str, end_commit: str) -> None:
    """Creates a summary of changes between two commits."""
    with tracer.start_as_current_span("summary_command") as span:
        span.set_attribute("path", path)
        span.set_attribute("start_commit", start_commit)
        span.set_attribute("end_commit", end_commit)

        summarize_service = SummarizeService()
        try:
            with tracer.start_as_current_span("get_diff"):
                diff = git_service.get_diff(path, start_commit, end_commit)

            with tracer.start_as_current_span("summarize"):
                result = summarize_service.summarize(diff)
                print(result)
                span.set_attribute("summary_length", len(result))
        except ValueError as e:
            typer.echo(f"Configuration error: {e}", err=True)
            raise typer.Exit(1)
        except ConnectionError as e:
            typer.echo(f"Connection error: {e}", err=True)
            raise typer.Exit(1)
        except RuntimeError as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1)
        except Exception as e:
            typer.echo(f"Unexpected error: {e}", err=True)
            raise typer.Exit(1)


@app.command()
def configure(
    api_url: str = typer.Option(
        ...,
        prompt="API URL",
        help="API URL (e.g., https://api.openai.com/v1)",
    ),
    model_name: str = typer.Option(
        "",
        prompt="Model name (optional)",
        help="Specific model name (e.g., gpt-4)",
    ),
) -> None:
    """Configures the API model and securely saves the key."""
    api_key = getpass.getpass("Enter API key: ")

    if not api_key:
        typer.echo("Error: API key cannot be empty", err=True)
        raise typer.Exit(1)

    try:
        config.set_model_config(api_url, api_key, model_name)
        typer.echo("Configuration saved successfully!")
    except Exception as e:
        typer.echo(f"Error saving configuration: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def show_config() -> None:
    """Shows the current model configuration."""
    model_config = config.get_model_config()
    if model_config is None:
        typer.echo("Model is not configured. Use the 'configure' command to set up.")
        return

    typer.echo(f"API URL: {model_config['api_url']}")
    if model_config.get("model_name"):
        typer.echo(f"Model name: {model_config['model_name']}")


if __name__ == "__main__":
    app()
