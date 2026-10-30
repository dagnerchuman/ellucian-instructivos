# 3. Ramas y checkout (cambiar de rama)

Una **rama** es una línea de trabajo. `main` es la oficial (la del sitio). Claude trabaja en ramas `claude/...`, por ejemplo `claude/vibrant-bardeen-26cbjd`.

## 3.1 Ver en qué rama está

```bash
git branch
```

La rama actual lleva un asterisco (`*`).

## 3.2 Actualizar la lista de ramas de GitHub

Las ramas nuevas que se suben a GitHub no aparecen solas en su computadora. Primero tráigalas:

```bash
git fetch origin
```

Y véalas todas, locales y remotas:

```bash
git branch -a
```

Las remotas salen como `remotes/origin/<nombre>`.

## 3.3 Cambiarse a otra rama (checkout)

```bash
git checkout claude/vibrant-bardeen-26cbjd
```

Si la rama solo existe en GitHub, Git crea la copia local y la enlaza con la remota. El comando nuevo equivalente es:

```bash
git switch claude/vibrant-bardeen-26cbjd
```

Para volver a `main`:

```bash
git checkout main
```

> **Antes de cambiar de rama, guarde o descarte sus cambios** (archivos 4 y 10). Si Git dice `Your local changes would be overwritten by checkout`, tiene cambios sin guardar.

## 3.4 Crear una rama nueva

Parta siempre de un `main` al día:

```bash
git checkout main
```

```bash
git pull origin main
```

Cree la rama y cámbiese a ella en un solo paso (use un nombre corto, sin espacios ni tildes):

```bash
git checkout -b ajuste-guia-computacion
```

Equivalente con `switch`:

```bash
git switch -c ajuste-guia-computacion
```

## 3.5 Borrar una rama que ya se unió a main

```bash
git branch -d ajuste-guia-computacion
```

`-d` solo la borra si ya está unida; así no se pierde trabajo.

Siguiente: [4. Guardar cambios (commit)](04-guardar-cambios-commit.md)
