# WebRecon

Script de reconocimiento web automatizado en Python.

Lee el target desde el archivo .env y ejecuta:

- Resolucion DNS
- Escaneo de puertos multihilo
- Analisis de cabeceras HTTP
- Comprobacion de rutas comunes
- Generacion de informe en JSON y Markdown

## Instalacion

git clone https://github.com/TU_USUARIO/web-recon.git
cd web-recon
pip install -r requirements.txt
copy .env.example .env

Edita .env con tu target.

## Uso

python recon.py

El informe se guarda en la carpeta reports/.

## Ejemplo de salida

Target: scanme.nmap.org
Resolviendo DNS... IP: 45.33.32.156
Escaneando puertos...
  Puerto 22 abierto (SSH)
  Puerto 80 abierto (HTTP)
Analizando http://scanme.nmap.org...
  admin -> 403
Informe JSON: reports/scanme.nmap.org_XXXXXX.json

## Aviso legal

Usa este script SOLO en sistemas que tengas autorizacion explicita para auditar.
