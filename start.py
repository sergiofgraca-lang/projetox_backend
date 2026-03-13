import subprocess
import webbrowser
import time

# inicia o servidor Django
subprocess.Popen(["python", "manage.py", "runserver"])

# espera o servidor iniciar
time.sleep(3)

# abre o sistema no navegador
webbrowser.open("http://127.0.0.1:8000")