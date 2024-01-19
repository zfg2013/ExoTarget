#__init__.py

import tomli
import pathlib

path = pathlib.Path(__file__).parent / "config.toml"
with path.open(mode="rb") as fp:
    config = tomli.load(fp)