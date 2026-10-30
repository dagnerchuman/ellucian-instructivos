# 7. Merge a main (unir una rama y publicar)

Hacer **merge** es llevar los *commits* de una rama a otra. En este proyecto se hace de la rama de trabajo a `main`, y **eso publica el sitio**.

> Antes del merge, revise la rama (archivo 6, punto 6.2). Lo que llega a `main` se ve en https://centros-empresariales-ellucian.vercel.app. La carpeta `docs/propuesta-usuarios-finales/` no va a `main` mientras sea borrador ([ADR-016](../../../conocimiento/decisiones/ADR-016-confidencialidad-y-publicacion.md)).

## 7.1 Paso a paso desde la terminal

1. Póngase en `main`:

```bash
git checkout main
```

2. Tráigalo al día:

```bash
git pull origin main
```

3. Traiga la rama que va a unir:

```bash
git fetch origin
```

4. Una la rama con `main`:

```bash
git merge origin/claude/vibrant-bardeen-26cbjd
```

   - Si se abre un editor para el mensaje del merge, guarde y cierre (en `vim`: escriba `:wq` y Enter).
   - Si dice `CONFLICT`, vaya al archivo 9.

5. Suba `main` a GitHub:

```bash
git push origin main
```

6. Espere uno o dos minutos y abra el sitio. Si no ve el cambio, recargue sin caché (Mac: Cmd + Shift + R; Windows: Ctrl + F5).

## 7.2 Ver qué trae la rama antes de unirla

Los *commits* que están en la rama y no en `main`:

```bash
git log --oneline main..origin/claude/vibrant-bardeen-26cbjd
```

Los archivos que cambian:

```bash
git diff --stat main...origin/claude/vibrant-bardeen-26cbjd
```

## 7.3 Si se arrepiente justo después del merge (sin haber hecho push)

```bash
git merge --abort
```

sirve **mientras el merge está a medias** (con conflictos). Si el merge ya terminó pero no lo subió, vea el archivo 10, punto 10.4. Si ya lo subió, use `git revert` (archivo 10, punto 10.5), nunca `--force`.

Siguiente: [8. Pull request en GitHub](08-pull-request-en-github.md)
