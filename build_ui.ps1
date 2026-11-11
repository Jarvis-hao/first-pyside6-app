# 修改 mainwindow.ui 后运行本脚本，重新生成 ui_mainwindow.py
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$uic = "D:\Envs\pyside\.venv\Scripts\pyside6-uic.exe"

& $uic "$root\mainwindow.ui" -o "$root\ui_mainwindow.py"
Write-Host "已重新生成 ui_mainwindow.py" -ForegroundColor Green
