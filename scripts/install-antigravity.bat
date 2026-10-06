@echo off
setlocal enabledelayedexpansion

set "ROOT=%~dp0.."
pushd "%ROOT%"
set "ROOT=%CD%"
popd

if defined AGY_SKILLS_DIR (
    set "DEST=%AGY_SKILLS_DIR%"
) else (
    set "DEST=%USERPROFILE%\.gemini\config\skills"
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY=python"
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY=py -3"
    ) else (
        echo Error: python was not found in PATH.
        exit /b 1
    )
)

%PY% "%ROOT%\scripts\sync-antigravity.py"
if %errorlevel% neq 0 exit /b %errorlevel%

if not exist "%DEST%" mkdir "%DEST%"

for /d %%D in ("%ROOT%\.agents\skills\*") do (
    set "NAME=%%~nxD"
    if exist "%DEST%\!NAME!" rmdir /s /q "%DEST%\!NAME!"
    xcopy "%%D" "%DEST%\!NAME!\" /e /i /y >nul
)

echo [OK] Antigravity workspace skills synchronized in %ROOT%\.agents\skills
echo [OK] Antigravity global skills installed to %DEST%
echo Note: Antigravity IDE and agy CLI will automatically discover project skills in .agents\
