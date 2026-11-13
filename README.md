# Mi compañero de vida

Compañero personal de escritorio con voz, memoria, planificación y asistencia mediante OpenAI.

## Objetivo

El proyecto busca crear un compañero que viva en la computadora, escuche reuniones cuando el usuario lo autorice, organice entregables, priorice tareas, ayude a redactar mensajes y controle integraciones como calendario, correo y Spotify.

## Estado actual

La primera base incluye:

- API local en Python con FastAPI.
- Memoria local en SQLite.
- CRUD inicial de tareas.
- Endpoint de conversación conectado a OpenAI Responses API.
- Protección para que claves, grabaciones y datos personales no entren a Git.

La aplicación visual del dragón y el modo de voz se incorporarán sobre esta base.

## Desarrollo local

Requiere Python 3.9 o superior.

Instalación automática:

```bash
./scripts/setup.sh
./scripts/configure-openai-key.sh
./scripts/start.sh
```

`configure-openai-key.sh` solicita la clave sin mostrarla en pantalla y la guarda
únicamente en el archivo local `.env`, que Git ignora.

En macOS también puedes abrir `Configurar OpenAI.command` con doble clic para
iniciar el mismo configurador seguro.

Instalación manual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp .env.example .env
```

Configura `OPENAI_API_KEY` en `.env` y ejecuta:

```bash
uvicorn backend.app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`.

## Seguridad y privacidad

- Las claves nunca se guardan en Git.
- La base SQLite se mantiene fuera del repositorio.
- Las acciones externas requerirán permisos explícitos.
- El audio de reuniones no se conservará por defecto.

Consulta [docs/architecture.md](docs/architecture.md) para la arquitectura inicial.

