import os
import requests
import zipfile
import io
import shutil
import subprocess
import sys
import Classes
class Updater:
    def __init__(self, repo_url, repo_version_file:str = ""):
        self.repo_url = repo_url
        self.repo_version_file = repo_version_file
        self.repo_zip_url = f"https://github.com/{repo_url}/archive/refs/heads/main.zip"

    def get_repo_version(self):
        """Holt die Version von GitHub aus der Versionsdatei."""
        url = f"https://raw.githubusercontent.com/{self.repo_url}/main/{self.repo_version_file}"
        response = requests.get(url)
        if response.status_code == 200:
            version = response.text.replace("__version__=","")
            version = version.replace("\"","")
            return version.strip()
        else:
            print(f"Error fetching version from GitHub: {response.status_code}")
            return None

    def check_for_update(self):
        """Prüft, ob eine neue Version verfügbar ist."""
        local_version =Classes.__version__
        repo_version = self.get_repo_version()

        if local_version is None:
            print("Keine lokale Version gefunden. Update wird empfohlen.")
            return True
        elif local_version != repo_version:
            print(f"Neue Version verfügbar: {repo_version} (aktuell: {local_version})")
            return True
        else:
            return False

    def download_update(self):
        """Lädt das Repository als ZIP herunter und entpackt es in einen temporären Ordner."""
        response = requests.get(self.repo_zip_url)
        if response.status_code == 200:
            print("Downloading update...")
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))

            # Temporärer Ordner für das Update
            temp_folder = "temp_update"
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
            os.makedirs(temp_folder)

            # Entpacke in den temporären Ordner
            zip_file.extractall(temp_folder)
            print(f"Update erfolgreich heruntergeladen und in {temp_folder} entpackt.")
            return temp_folder
        else:
            print(f"Fehler beim Herunterladen des Updates: {response.status_code}")
            return None

    def apply_update(self, temp_folder):
        """Kopiert die neuen Dateien ins Hauptverzeichnis und löscht den temporären Ordner."""
        print("Kopiere neue Dateien...")
        self.copy_files(temp_folder, ".")
        shutil.rmtree(temp_folder)  # Temporären Ordner löschen
        print("Update abgeschlossen. Temporärer Ordner entfernt.")

    def copy_files(self, src_dir, dest_dir):
        """Kopiert die Dateien vom temporären Ordner ins Zielverzeichnis und ersetzt sie."""
        for root, dirs, files in os.walk(src_dir):
            relative_path = os.path.relpath(root, src_dir)
            target_dir = os.path.join(dest_dir, relative_path)

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dest_file)
                print(f"Updated {dest_file}")

    def trigger_update(self):
        """Startet den Update-Prozess."""
        temp_folder = self.download_update()

        if temp_folder:
            # Schließe das aktuelle Programm, update und starte es neu
            self.apply_update(temp_folder)

            # Starte das Programm neu, aber unabhängig vom aktuellen Prozess
            print("Starte das Programm neu...")

            if os.name == 'nt':  # Windows
                subprocess.Popen([sys.executable] + sys.argv, creationflags=subprocess.DETACHED_PROCESS)
            else:  # Unix-basierte Systeme (Linux, macOS)
                subprocess.Popen([sys.executable] + sys.argv, start_new_session=True)
        sys.exit()

    def main(self):
        self.trigger_update()

if __name__ == "__main__":
    updater = Updater(repo_url="Charmander12345/PersonalPlanner")