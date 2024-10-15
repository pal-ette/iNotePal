from os.path import dirname, basename
from os import listdir

__all__ = [
    f[:-3]
    for f in listdir(dirname(__file__))
    if f.endswith(".py") and not f.endswith(basename(__file__))
]
