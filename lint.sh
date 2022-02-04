flake8 app --max-line-length=120
pylint --attr-naming-style=any app
#pylint --attr-naming-style=any --disable=C0116,W0511,R0201,R0903 app
mypy app
black app
