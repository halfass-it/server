from pathlib import Path

class CacheDir:
  def __init__(self, cache_dir: Path = None) -> None:
    if not self.cache_dir:
      self.cache_dir = Path(f'~/.cache/{str(Path(__file__).cwd().name).split("/")[-1]}').expanduser()
    Path.mkdir(self.cache_dir, exist_ok=True)

  def __str__(self) -> Path:
    return self.cache_dir

  def __repr__(self) -> Path:
    return self.cache_dir

