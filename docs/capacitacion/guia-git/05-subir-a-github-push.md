# 5. Subir a GitHub (push)

`push` sube sus *commits* de la rama actual a GitHub.

## 5.1 La primera vez que sube una rama

```bash
git push -u origin ajuste-guia-computacion
```

`-u` deja enlazada la rama local con la de GitHub. Desde entonces, en esa rama basta con:

```bash
git push
```

## 5.2 Comprobar en GitHub

Abra https://github.com/dagnerchuman/ellucian-instructivos, elija la rama en el selector de ramas (arriba a la izquierda) y revise que estén sus archivos y su *commit*.

## 5.3 Errores frecuentes

| Mensaje | Qué pasa | Qué hacer |
|---|---|---|
| `rejected ... (fetch first)` o `non-fast-forward` | En GitHub hay *commits* que usted no tiene | Baje primero los cambios (`git pull`, archivo 6) y vuelva a hacer `push` |
| `Permission denied` o `403` | Su cuenta no tiene permiso en el repositorio | Pida la invitación como colaborador (archivo 1, punto 1.4) |
| `Authentication failed` | GitHub no reconoce su acceso | Vuelva a entrar con `gh auth login` o con un token nuevo (archivo 1, punto 1.3) |
| `src refspec ... does not match any` | El nombre de la rama está mal escrito o la rama no tiene *commits* | Revise con `git branch` |

> **No use `git push --force` en `main`.** Borra en GitHub los *commits* que usted no tenga y puede tumbar el sitio.

Siguiente: [6. Traer cambios (pull)](06-traer-cambios-pull.md)
