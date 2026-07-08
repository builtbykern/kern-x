# KERN-Reply con tu Google Chrome

kern-x se engancha a **Google Chrome** (no al browser de Cursor) por CDP. Chrome **permanece abierto** entre ciclos.

## Perfil dedicado (recomendado)

Un Chrome separado con perfil `~/.kern-x-chrome` para @builtbykern. Tu Chrome de uso diario puede seguir abierto en paralelo.

```bash
./scripts/start_kern_reply.sh
```

1. Si es la primera vez, abre Chrome → login @builtbykern → vuelve a ejecutar el script.
2. El daemon corre ciclos cada 60–90 min sin cerrar Chrome (~16–20 pasadas/día si el Mac está encendido; cap diario 32 replies).

## Manual (dos terminales)

**Terminal 1** — deja Chrome abierto:

```bash
./scripts/x_chrome_cdp.sh
```

**Terminal 2** — daemon:

```bash
export X_CDP_URL=http://127.0.0.1:9222
python3 scripts/x_reply_daemon.py
```

## Variables

| Variable | Default |
|----------|---------|
| `X_CDP_URL` | `http://127.0.0.1:9222` |
| `X_CDP_PORT` | `9222` |
| `X_CHROME_PROFILE` | `~/.kern-x-chrome` |
| `X_LOOP_MIN_SEC` | `3600` (60 min) |
| `X_LOOP_MAX_SEC` | `5400` (90 min) |

## Prueba sin publicar

```bash
export X_CDP_URL=http://127.0.0.1:9222
python3 scripts/x_reply_cycle.py --dry-run
```

## launchd

```bash
./scripts/install_launchd.sh
```

Asegura `X_CDP_URL` en `.env` y que Chrome con CDP esté arrancado al login (p. ej. Login Items → `start_kern_reply.sh` una vez, o un segundo agente que solo lance Chrome).

## No usar el Chrome ya abierto sin CDP

macOS no deja que Playwright controle una ventana de Chrome que no se inició con `--remote-debugging-port`. Por eso usamos un perfil kern-x o reiniciar Chrome con ese flag.
