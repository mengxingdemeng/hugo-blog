@echo off
chcp 65001 >nul
echo ==============================================
echo        Vjudge刷题数据本地一键刷新
echo ==============================================
echo.

echo 正在运行爬虫脚本...
"D:\Python.3.15\python.exe" scripts/crawl_vjudge.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ 执行成功，static/data/vjudge-record.json 已更新
) else (
    echo.
    echo ❌ 爬虫运行出错！
)

echo.
pause