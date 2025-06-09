#!/bin/bash

# Sprawdzenie Pythona
echo "Sprawdzam czy Python jest zainstalowany..."

if command -v python >/dev/null 2>&1; then
    PYTHON="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    echo "Python nie jest zainstalowany lub nie jest w PATH."
    echo "Pobierz i zainstaluj Python: https://www.python.org/downloads/"
    exit 1
fi

echo "Znaleziono Python: $PYTHON"
echo

# Sprawdzenie i instalacja brakujących pakietów
PACKAGES="questionary"

echo "Sprawdzam wymagane pakiety Pythona..."
for P in $PACKAGES; do
    echo "Sprawdzam $P..."
    $PYTHON -c "import $P" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Brak pakietu $P, instaluję..."
        $PYTHON -m pip install "$P"
        if [ $? -ne 0 ]; then
            echo "Nie udało się zainstalować pakietu $P. Sprawdź połączenie internetowe i spróbuj ponownie."
            exit 1
        fi
    else
        echo "Pakiet $P jest zainstalowany."
    fi
done

echo
echo "Wszystkie wymagane pakiety są zainstalowane."

# Wyczyść konsolę przed uruchomieniem Pythona
clear

echo "Uruchamiam skrypt Python..."
$PYTHON assets/ffmpeg.py

read -p "Naciśnij Enter, aby zakończyć..."
