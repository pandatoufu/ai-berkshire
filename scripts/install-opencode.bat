@echo off
setlocal

for %%I in ("%~dp0..") do set "ROOT=%%~fI"

if defined OPENCODE_CONFIG_DIR (
  set "DEST=%OPENCODE_CONFIG_DIR%"
) else (
  set "DEST=%USERPROFILE%\.config\opencode"
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

%PY% "%ROOT%\scripts\sync-opencode.py"
if errorlevel 1 exit /b %ERRORLEVEL%

if not exist "%DEST%\commands" mkdir "%DEST%\commands"
if errorlevel 1 exit /b %ERRORLEVEL%
if not exist "%DEST%\skills" mkdir "%DEST%\skills"
if errorlevel 1 exit /b %ERRORLEVEL%

copy /Y "%ROOT%\.opencode\commands\*.md" "%DEST%\commands\" >nul
if errorlevel 1 exit /b %ERRORLEVEL%

for /d %%D in ("%ROOT%\.opencode\skills\*") do (
  if exist "%DEST%\skills\%%~nxD" rmdir /s /q "%DEST%\skills\%%~nxD"
  if errorlevel 1 exit /b 1
  xcopy "%%~fD" "%DEST%\skills\%%~nxD\" /E /I /Y >nul
  if errorlevel 1 exit /b 1
)

echo Installed opencode commands to %DEST%\commands
echo Installed opencode skills to %DEST%\skills
echo Restart opencode to pick up new commands and skills.
