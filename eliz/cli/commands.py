import argparse

from eliz import __version__

def main() -> None:
    parser = argparse.ArgumentParser(prog="eliz", description="Eliz - A programming language combining Java and Python features.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"Eliz {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Create a new Eliz project.")
    subparsers.add_parser("run", help="Run an Eliz project or source file.")
    subparsers.add_parser("check", help="Check code for errors.")

    args = parser.parse_args()

    if args.command == "init":
        print("Project initialization is not yet implemented.")
    elif args.command == "run":
        print("The Eliz Interpreter is not yet implemented.")
    elif args.command == "check":
        print("Code checking is not yet implemented.")
    elif args.command is None:
        parser.print_help()

# Eliz COMMANDS
# eliz init - sets up the directory ?
# eliz run - runs the code ?
# eliz check - checks for errors ?
# eliz version - returns the version of the program ?
# eliz help - sends you the guide to eliz
# eliz update - update the program