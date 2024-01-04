@echo off
rmdir /s /q dist
rmdir /s /q src\Scripto.egg-info
python -m build
python -m twine upload dist/*
rmdir /s /q dist
rmdir /s /q src\Scripto.egg-info
