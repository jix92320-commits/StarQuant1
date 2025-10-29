@echo off
title StarQuant 一键修复并启动
cd /d D:\StarQuant
rem === 1. 修复 ai_memory 路径（喂给旧代码想要的 C:\StarQuant）===
if not exist C:\StarQuant mkdir C:\StarQuant >nul 2>nul
if not exist ai_memory.json echo {}>ai_memory.json
copy /y ai_memory.json C:\StarQuant\ai_memory.json >nul
rem === 2. 解决语音临时文件权限：把 TMP/TEMP 指到本地可写目录 ===
if not exist D:\StarQuant\tmp mkdir D:\StarQuant\tmp >nul 2>nul
set TMP=D:\StarQuant\tmp
set TEMP=D:\StarQuant\tmp
rem === 3. 预热数据：多源重试，最大 1500 条，失败就再来一遍 ===
python starquant_autorun_ai.py --refresh --max=1500
if errorlevel 1 python starquant_autorun_ai.py --refresh --max=1500
rem === 4. 启动主程序 ===
python main_starquant.py
