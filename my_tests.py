import os
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent
a = "media"
b = "media/"
c = "/media"
d = "/media/"


print(os.path.join(BASE_DIR, a))
print(os.path.join(BASE_DIR, b))
print(os.path.join(BASE_DIR, c))
print(os.path.join(BASE_DIR, d))
