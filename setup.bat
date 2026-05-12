@echo off
:: One-command setup for Berean Bible Bots notebooks (Windows).
:: Usage (from the project root): setup.bat

echo.
echo === Berean Bible Bots -- Notebook Setup ===
echo.

:: ── 1. Locate Python 3.11+ ──────────────────────────────────────────────────
set PYTHON=
for %%P in (python3.13 python3.12 python3.11 python3 python) do (
    where %%P >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=*" %%V in ('%%P -c "import sys; print(sys.version_info >= (3,11))"') do (
            if "%%V"=="True" (
                set PYTHON=%%P
                goto :found_python
            )
        )
    )
)

echo ERROR: Python 3.11 or later is required but was not found.
echo Download it from https://www.python.org/downloads/ and re-run this script.
exit /b 1

:found_python
for /f "tokens=*" %%V in ('%PYTHON% --version') do echo Using %%V

:: ── 2. Create virtual environment ───────────────────────────────────────────
if not exist ".venv\" (
    echo Creating virtual environment ^(.venv^)...
    %PYTHON% -m venv .venv
) else (
    echo Virtual environment already exists -- skipping creation.
)

:: ── 3. Activate ─────────────────────────────────────────────────────────────
call .venv\Scripts\activate.bat
echo Virtual environment activated.

:: ── 4. Upgrade pip ──────────────────────────────────────────────────────────
pip install --upgrade pip --quiet

:: ── 5. Install dependencies ──────────────────────────────────────────────────
echo Installing dependencies ^(this may take a few minutes the first time^)...
pip install -r requirements-notebooks.txt --quiet

:: ── 6. Register Jupyter kernel ───────────────────────────────────────────────
echo Registering Jupyter kernel...
python -m ipykernel install --user --name berean-bible-bots --display-name "Berean Bible Bots"

:: ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo === Setup complete! ===
echo.
echo Next steps:
echo   1. Open VS Code and install the Jupyter extension if you haven't
echo      ^(search 'Jupyter' in the Extensions panel^).
echo   2. Open any notebook in notebooks/ -- e.g. notebooks\ot\verbs\qal.ipynb
echo   3. Click 'Select Kernel' ^(top-right^) -^> Jupyter Kernel -^> Berean Bible Bots
echo   4. Click 'Run All'.
echo.
echo If you open a new terminal later, activate the venv first:
echo   .venv\Scripts\activate
echo.
