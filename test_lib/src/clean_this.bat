@echo off

setlocal

del /s /f /q dist
rmdir dist

del /s /f /q sogeti_test_lib.egg-info
rmdir sogeti_test_lib.egg-info

endlocal
