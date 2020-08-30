@echo off

setlocal

if exist dist (
	clean_this.bat
	python setup.py sdist
) else (
	python setup.py sdist
)

endlocal
