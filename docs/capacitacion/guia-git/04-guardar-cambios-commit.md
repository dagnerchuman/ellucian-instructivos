# 4. Guardar cambios (commit)

Un **commit** es una foto de los cambios con un mensaje. Se hace en tres pasos: revisar, elegir y guardar.

## 4.1 Revisar qué cambió

```bash
git status
```

- **Modified:** archivos que ya existían y cambiaron.
- **Untracked:** archivos nuevos que Git todavía no sigue.

Para ver el detalle línea por línea (salga con la tecla `q`):

```bash
git diff
```

## 4.2 Elegir qué entra en el commit (add)

Un archivo:

```bash
git add centros/computacion/datos.json
```

Una carpeta completa:

```bash
git add docs/capacitacion/guia-git
```

Todo lo que cambió:

```bash
git add -A
```

> Revise `git status` antes de `git add -A`: no suba archivos de prueba, copias personales ni nada con contraseñas o datos de alumnos.

## 4.3 Guardar (commit)

```bash
git commit -m "Guía de la Demostración 1: filas de la diap. 33 (C177)"
```

**Un buen mensaje** dice qué cambió y, si existe, cita la referencia del registro (C##, U##, ADR-0##). Ejemplos del proyecto:

- `Malla en la Demostración 1 (C176): paso SMAAREA en el diagrama y la tabla «Antes del NRC»`
- `Corrección C175: Computación I, II y III son el Plan Tradicional, no rutas XP`

## 4.4 Ver el historial

```bash
git log --oneline -10
```

Muestra los últimos 10 *commits*, del más nuevo al más antiguo.

## 4.5 Lo que no se sube

El archivo `.gitignore` ya excluye lo que no debe ir a GitHub: `node_modules/`, el motor Archify (`herramientas/diagramas/.archify/`), los archivos `.DS_Store` de Mac y los recibos temporales de los diagramas.

Siguiente: [5. Subir a GitHub (push)](05-subir-a-github-push.md)
