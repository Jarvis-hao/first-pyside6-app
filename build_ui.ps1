# 修改 mainwindow.ui 后运行本脚本，重新生成 ui_mainwindow.py
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$uic = Join-Path $root ".venv\Scripts\pyside6-uic.exe"

if (-not (Test-Path $uic)) {
    Write-Host "找不到 $uic，请先在项目目录创建 .venv 并安装 PySide6" -ForegroundColor Red
    exit 1
}

& $uic "$root\mainwindow.ui" -o "$root\ui_mainwindow.py"
Write-Host "已重新生成 ui_mainwindow.py" -ForegroundColor Green
