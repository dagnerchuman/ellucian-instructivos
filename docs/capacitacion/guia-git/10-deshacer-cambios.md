# 10. Deshacer cambios

Elija según **dónde** está el cambio que quiere deshacer.

| Situación | Punto |
|---|---|
| Cambié un archivo y no lo he guardado en un *commit* | 10.1 |
| Le hice `git add` por error | 10.2 |
| Quiero apartar mis cambios un momento | 10.3 |
| Hice un *commit* y **no** lo he subido | 10.4 |
| Hice un *commit* y **ya** lo subí | 10.5 |

## 10.1 Descartar los cambios de un archivo (sin commit)

```bash
git restore centros/computacion/datos.json
```

Vuelve al último *commit*. **Lo que cambió se pierde**: revise antes con `git diff`.

## 10.2 Sacar un archivo del add

```bash
git restore --staged centros/computacion/datos.json
```

El cambio se queda en el archivo; solo deja de estar elegido para el *commit*.

## 10.3 Apartar los cambios (stash)

```bash
git stash
```

Para recuperarlos:

```bash
git stash pop
```

## 10.4 Deshacer el último commit que no subió

Deja los cambios en los archivos, listos para corregir y volver a guardar:

```bash
git reset --soft HEAD~1
```

## 10.5 Deshacer un commit que ya subió (revert)

`revert` crea un *commit* nuevo que hace lo contrario; no borra el historial y es seguro en `main`.

1. Busque el código del *commit*:

```bash
git log --oneline -10
```

2. Reviértalo (reemplace `46b92d9` por el código):

```bash
git revert 46b92d9
```

3. Súbalo:

```bash
git push
```

> **No use `git reset --hard` ni `git push --force` en `main`.** Borran trabajo que no se puede recuperar desde GitHub.

## 10.6 Recuperar un archivo de un commit anterior

```bash
git checkout 46b92d9 -- centros/computacion/datos.json
```

Siguiente: [11. Flujo del proyecto](11-flujo-del-proyecto.md)
