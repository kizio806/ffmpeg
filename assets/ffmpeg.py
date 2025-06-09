import os
import subprocess
import sys
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

# Ścieżka do ffmpeg.exe zakładana względem tego skryptu
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_PATH = os.path.join(SCRIPT_DIR, "..", "bin", "ffmpeg.exe")

def get_video_file():
    while True:
        path = questionary.path("Wprowadź ścieżkę do pliku MP4:").ask()
        if path and os.path.isfile(path) and path.lower().endswith(".mp4"):
            return path
        console.print("[red]❌ Niepoprawna ścieżka lub plik nie jest MP4.[/red]")

def get_segment_time():
    return questionary.text(
        "Podaj długość segmentu w sekundach (np. 180 dla 3 minut):", 
        default="180"
    ).ask()

def get_output_pattern():
    return questionary.text(
        "Podaj wzór nazwy plików wynikowych (np. output_%03d.mp4):", 
        default="output_%03d.mp4"
    ).ask()

def get_mode():
    return questionary.select(
        "Wybierz tryb dzielenia:",
        choices=[
            "Szybki (bez reenkodowania -c copy)",
            "Dokładny (z reenkodowaniem i keyframes)"
        ]
    ).ask()

def get_output_directory():
    while True:
        folder = questionary.path("Wybierz folder docelowy dla pociętych plików:").ask()
        if folder and os.path.isdir(folder):
            return folder
        console.print("[red]❌ To nie jest poprawny folder.[/red]")

def build_command(input_file, segment_time, output_pattern, mode):
    if mode.startswith("Szybki"):
        return [
            FFMPEG_PATH,
            "-i", input_file,
            "-c", "copy",
            "-map", "0",
            "-f", "segment",
            "-segment_time", segment_time,
            output_pattern
        ]
    else:
        return [
            FFMPEG_PATH,
            "-i", input_file,
            "-force_key_frames", f"expr:gte(t,n_forced*{segment_time})",
            "-f", "segment",
            "-segment_time", segment_time,
            "-reset_timestamps", "1",
            output_pattern
        ]

from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.clear()
    console.print(Panel.fit("""
[bold cyan]
  ╔══════════════════════════════════════════╗
  ║ FFFFF  FFFFF  M   M  PPPP   EEEEE  GGGG  ║
  ║ F      F      MM MM  P   P  E      G     ║
  ║ FFF    FFF    M M M  PPPP   EEEE   G GG  ║
  ║ F      F      M   M  P      E      G   G ║
  ║ F      F      M   M  P      EEEEE  GGGG  ║
  ╚══════════════════════════════════════════╝
[/bold cyan]

[bold cyan]FFmpeg Video Splitter[/bold cyan]
""", title="[bold magenta]Witaj![/bold magenta]", subtitle="Autor: kizio"))


    input_file = get_video_file()
    if not input_file:
        console.print("[red]Nie wybrano pliku. Koniec.[/red]")
        return

    segment_time = get_segment_time()
    output_pattern = get_output_pattern()
    output_dir = get_output_directory()
    output_path = os.path.join(output_dir, output_pattern)  # Pełna ścieżka wynikowa

    mode = get_mode()

    command = build_command(input_file, segment_time, output_path, mode)

    console.print("\n[bold green]Uruchamianie komendy FFmpeg:[/bold green]")
    console.print(" ".join(command))

    try:
        subprocess.run(command, check=True)
        console.print("\n[bold green]Proces zakończony pomyślnie![/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"\n[bold red]Błąd podczas uruchamiania FFmpeg: {e}[/bold red]")

if __name__ == "__main__":
    main()
