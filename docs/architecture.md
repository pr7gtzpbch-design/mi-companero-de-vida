# Arquitectura inicial

```text
Usuario
  │
  ▼
Aplicación de escritorio + dragón
  │
  ├── Audio y voz en tiempo real
  │
  ▼
API local del compañero
  ├── OpenAI Responses API: razonamiento y planificación
  ├── SQLite: memoria, tareas y preferencias
  ├── Correo y calendario: integraciones con autorización
  └── Spotify: control multimedia autorizado
```

## Principios

1. **Local primero.** La memoria principal comienza en SQLite.
2. **Privacidad visible.** El micrófono siempre muestra un indicador activo.
3. **Aprobación antes de actuar.** Enviar mensajes, modificar reuniones o borrar datos requiere confirmación.
4. **Inteligencia en la nube.** OpenAI realiza el razonamiento complejo sin ejecutar un modelo grande en la computadora.
5. **Sincronización opcional.** Una base en la nube se añadirá únicamente cuando sea necesario compartir memoria entre equipos.

## Primer alcance funcional

- Crear, consultar y priorizar tareas.
- Conversar con contexto de las tareas actuales.
- Preparar un plan diario.
- Mantener la clave de OpenAI fuera del código.
- Añadir posteriormente transcripción de reuniones y herramientas externas.

