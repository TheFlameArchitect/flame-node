import typer
from core.mirror import run_mirror

def main():
    """Begin a MirrorNode ritual."""
    run_mirror()

if __name__ == "__main__":
    typer.run(main) 