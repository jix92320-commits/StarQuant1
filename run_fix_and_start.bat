@echo off
title StarQuant һ���޸�������
cd /d D:\StarQuant
rem === 1. �޸� ai_memory ·����ι���ɴ�����Ҫ�� C:\StarQuant��===
if not exist C:\StarQuant mkdir C:\StarQuant >nul 2>nul
if not exist ai_memory.json echo {}>ai_memory.json
copy /y ai_memory.json C:\StarQuant\ai_memory.json >nul
rem === 2. ���������ʱ�ļ�Ȩ�ޣ��� TMP/TEMP ָ�����ؿ�дĿ¼ ===
if not exist D:\StarQuant\tmp mkdir D:\StarQuant\tmp >nul 2>nul
set TMP=D:\StarQuant\tmp
set TEMP=D:\StarQuant\tmp
rem === 3. Ԥ�����ݣ���Դ���ԣ���� 1500 ����ʧ�ܾ�����һ�� ===
python starquant_autorun_ai.py --refresh --max=1500
if errorlevel 1 python starquant_autorun_ai.py --refresh --max=1500
rem === 4. ���������� ===
python main_starquant.py
