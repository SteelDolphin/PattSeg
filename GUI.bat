chcp 65001
@echo off
REM 设置 pyuic5 工具路径
set PYUIC5_PATH=D:\envs\conda\DIMG\Scripts\pyuic5.exe

REM 检查 pyuic5 是否存在
if not exist "%PYUIC5_PATH%" (
    echo pyuic5 工具未找到: %PYUIC5_PATH%
    exit /b 1
)

REM 设置 UI 文件路径和输出的 Python 文件路径
set INPUT_UI=.\ui\main_window.ui
set OUTPUT_PY=.\src\ui_main_window.py

REM 生成 Python 文件
"%PYUIC5_PATH%" -o "%OUTPUT_PY%" "%INPUT_UI%"

REM 检查生成是否成功
if %ERRORLEVEL% neq 0 (
    echo 生成失败！
    exit /b 1
)

echo 生成成功：%OUTPUT_PY%
