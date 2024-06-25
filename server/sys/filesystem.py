from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class CacheDir:
  path: Path = field(init=False, default=None)

  def __post_init__(self) -> None:
    if not self.path:
      self.path = Path(f'~/.cache/{str(Path(__file__).cwd().name).split("/")[-1]}').expanduser()
    try:
      Path.mkdir(self.path, exist_ok=True)
    except Exception as e:
      raise (Exception(f'Error: {e}'))

  def __str__(self) -> Path:
    return str(self.path)

  def __repr__(self) -> Path:
    return f'CacheDir(path={self.path})'
