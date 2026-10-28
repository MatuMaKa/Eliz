import json
from pathlib import Path

class ModuleResolver:
    def __init__(self, project_root: str | Path = ".") -> None:
        self.project_root = Path(project_root).resolve()
        self.source_directory = self.project_root / "src"
        self._load_config()

    def _load_config(self) -> None:
        config_path = self.project_root / "eliz.json"

        if not config_path.exists():
            self.source_directory = self.project_root / "src"
            return

        try:
            with config_path.open("r", encoding="utf-8") as file:
                config = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON is '{config_path}': {error}"
            ) from error

        source = config.get("source", "src")

        if not isinstance(source, str) or not source.strip():
            raise ValueError(
                "The 'source' field in eliz.json must be a non-empty string."
            )

        self.source_directory = (
            self.project_root / source
        ).resolve

        if not self.source_directory.is_relative_to(self.project_root):
            raise ValueError(
                "The source directory must be inside the project root."
            )

    def resolve(self, module_name: str) -> Path:
        parts = module_name.split(".")

        if not parts or any(
            not part.isidentifier() for part in parts
        ):
            raise ValueError(
                f"Invalid module name '{module_name}'."
            )

        source_file = self.source_directory.joinpath(*parts).with_suffix(".eliz")

        if not source_file.is_file():
            raise FileNotFoundError(
                f"Cannot find module '{module_name}'. "
                f"Expected file: {source_file}"
            )

        return source_file

    def load_source(self, module_name: str) -> str:
        source_file = self.resolve(module_name)
        return source_file.read_text(encoding="utf-8")