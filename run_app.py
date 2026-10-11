import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    required = ['streamlit', 'matplotlib', 'numpy', 'pandas']
    missing = [pkg for pkg in required if importlib.util.find_spec(pkg) is None]
    if missing:
        print(f"Eksik paketler tespit edildi, yükleniyor: {missing}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

def main():
    print("🧬 TAPC Bilimsel Kontrol Paneli Başlatılıyor...")
    check_dependencies()
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    main()
