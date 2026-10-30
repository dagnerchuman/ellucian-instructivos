# 6. Traer cambios (pull)

`pull` baja a su computadora los *commits* que están en GitHub y no tiene: los de otra persona o los que subió Claude.

## 6.1 Antes de empezar a trabajar, siempre

```bash
git checkout main
```

```bash
git pull origin main
```

## 6.2 Traer la rama donde trabajó Claude

Claude avisa en el chat el nombre de su rama (por ejemplo `claude/vibrant-bardeen-26cbjd`). Para verla en su computadora:

```bash
git fetch origin
```

```bash
git checkout claude/vibrant-bardeen-26cbjd
```

```bash
git pull origin claude/vibrant-bardeen-26cbjd
```

Ahora puede abrir los archivos o el sitio con Live Server y revisar el cambio **antes** de llevarlo a `main`.

## 6.3 fetch frente a pull

| Comando | Qué hace |
|---|---|
| `git fetch origin` | Solo baja la información de GitHub; no cambia sus archivos. Sirve para ver qué hay nuevo |
| `git pull origin <rama>` | `fetch` + `merge`: baja y une los cambios con su rama actual |

Para ver cuántos *commits* le faltan o le sobran frente a GitHub:

```bash
git status
```

Dice, por ejemplo, `Your branch is behind 'origin/main' by 2 commits`: le faltan 2, haga `pull`.

## 6.4 Si pull dice que hay cambios locales

`Your local changes would be overwritten by merge`: tiene cambios sin guardar. Guárdelos en un *commit* (archivo 4) o apártelos un momento:

```bash
git stash
```

```bash
git pull origin main
```

```bash
git stash pop
```

Siguiente: [7. Merge a main](07-merge-a-main.md)
