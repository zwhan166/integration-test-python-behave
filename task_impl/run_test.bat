@echo off

setlocal

set curr_dir=%~dp0
set work_dir=%curr_dir%\sogeti_test
set venv_dir=%work_dir%\venv
set src_dir=%curr_dir%\test_src
set dst_dir=%work_dir%\work
set lib_file=%curr_dir%\sogeti_test_lib-0.0.1.tar.gz

echo.
echo [ INFO ] Create working directory...
if exist %work_dir% (
	del /s /f /q %work_dir%
	rd /s /q %work_dir%
)
mkdir %work_dir%

echo.
echo [ INFO ] Create virtual environment...
python -m venv %venv_dir%

echo.
echo [ INFO ] Activate the virtual environment...
call %venv_dir%\Scripts\activate

echo.
echo [ INFO ] Install the custom test library...
%venv_dir%\Scripts\pip install %lib_file%
echo import sogeti >>  %venv_dir%\Lib\site-packages\behave\__init__.py

echo.
echo [ INFO ] Copy test source files...
mkdir %dst_dir%
xcopy /s /e %src_dir% %dst_dir%

echo.
echo [ INFO ] Run the test...
cd /d %dst_dir%
..\venv\Scripts\behave.exe --no-capture features
cd /d %curr_dir%

echo.
echo [ INFO ] Deactivate the virtual environment...
call %venv_dir%\Scripts\deactivate.bat

echo.

endlocal
