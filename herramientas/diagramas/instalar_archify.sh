#!/usr/bin/env bash
# Descarga el motor Archify (MIT, https://github.com/tt-a1i/archify) en una versión fija.
# Queda en herramientas/diagramas/.archify/, que está en .gitignore: no se sube al repositorio.
#
# Uso:  bash herramientas/diagramas/instalar_archify.sh
set -euo pipefail

REPO="https://github.com/tt-a1i/archify.git"
COMMIT="d5a1333d7447c866a765adac7d4d062f2f02e4d2"   # v3.0.1 (30/09/2026)
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="$AQUI/.archify"

if [ -f "$DESTINO/archify/bin/archify.mjs" ] && [ "$(cat "$DESTINO/COMMIT" 2>/dev/null)" = "$COMMIT" ]; then
  echo "Archify ya está instalado en $DESTINO ($COMMIT)."
  exit 0
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --quiet --filter=blob:none "$REPO" "$TMP/archify"
git -C "$TMP/archify" checkout --quiet "$COMMIT"

rm -rf "$DESTINO"
mkdir -p "$DESTINO"
cp -R "$TMP/archify/archify" "$DESTINO/archify"
echo "$COMMIT" > "$DESTINO/COMMIT"
node "$DESTINO/archify/bin/archify.mjs" doctor | tail -1
echo "Archify instalado en $DESTINO"
