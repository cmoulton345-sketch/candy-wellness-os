@echo off
title Flowstate AI Voice Engine - Candy
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File kill_speak.ps1 >nul 2>&1
if exist .speak_active del /f /q .speak_active
if exist stop.flag del /f /q stop.flag
if exist .speaking del /f /q .speaking
"C:\Users\Admin\AppData\Local\Python\pythoncore-3.14-64\python.exe" voice_system.py
