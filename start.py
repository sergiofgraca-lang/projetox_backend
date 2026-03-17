import os
import sys
import webbrowser
import threading

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:8000")

def main():
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    os.chdir(base_dir)

    threading.Timer(2, abrir_navegador).start()

    os.system("python manage.py runserver")

if __name__ == "__main__":
    main()