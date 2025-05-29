@echo off
setlocal EnableDelayedExpansion

:: Sprawdzenie Pythona
echo Sprawdzam czy Python jest zainstalowany...

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    python3 --version >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Python nie jest zainstalowany lub nie jest w PATH.
        echo Pobierz i zainstaluj Python: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON=python3
    )
) else (
    set PYTHON=python
)

echo Znaleziono Python: %PYTHON%
echo.

:: Sprawdzenie i instalacja brakujacego pakietu
set PACKAGES=questionary

echo Sprawdzam wymagane pakiety Pythona...
for %%P in (%PACKAGES%) do (
    echo Sprawdzam %%P...
    %PYTHON% -c "import %%P" 2>nul
    if !ERRORLEVEL! neq 0 (
        echo Brak pakietu %%P, instaluję...
        %PYTHON% -m pip install %%P
        if !ERRORLEVEL! neq 0 (
            echo Nie udało się zainstalować pakietu %%P. Sprawdź połączenie internetowe i spróbuj ponownie.
            pause
            exit /b 1
        )
    ) else (
        echo Pakiet %%P jest zainstalowany.
    )
)

echo.
echo.
echo Wszystkie wymagane pakiety są zainstalowane.

:: Wyczyść konsolę przed uruchomieniem Pythona
cls

echo Uruchamiam skrypt Python...
%PYTHON% assets/ffmpeg.py

pause

