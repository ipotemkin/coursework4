flake8 app run.py --max-line-length=120
pylint --attr-naming-style=any app run.py
#pylint --attr-naming-style=any --disable=C0116,W0511,R0201,R0903 app
mypy app run.py
black app run.py
