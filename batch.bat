@echo off
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Set UAC for privilege escalation...
    echo Running batch file as Administrator...
    PowerShell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
setx OPENAI_API_KEY sk-123 /m
