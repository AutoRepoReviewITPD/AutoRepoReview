import typer

app = typer.Typer()


@app.command()
def summary(start_commit: str, end_commit: str) -> None:
    changes = [
        "Add mypy to the project",
        "Remove old Docker Compose configuration",
        "Add feature of multiplying 2 numbers"
    ]

    print(f"Start commit: {start_commit}")
    print(f"End commit: {end_commit}\n")

    print("Summary of changes:")
    for change_index, change in enumerate(changes):
        print(f"{change_index+1}. {change}")


if __name__ == "__main__":
    app()

