# 12. Comandos rápidos

| Quiero… | Comando |
|---|---|
| Bajar el proyecto (una vez) | `git clone https://github.com/dagnerchuman/ellucian-instructivos.git` |
| Ver en qué rama estoy y qué cambió | `git status` |
| Ver todas las ramas | `git fetch origin` y luego `git branch -a` |
| Cambiarme a una rama | `git checkout <rama>` (o `git switch <rama>`) |
| Crear una rama nueva | `git checkout -b <rama>` (o `git switch -c <rama>`) |
| Ver los cambios línea por línea | `git diff` |
| Elegir todo para el commit | `git add -A` |
| Guardar un commit | `git commit -m "mensaje (C##)"` |
| Subir mi rama la primera vez | `git push -u origin <rama>` |
| Subir otra vez | `git push` |
| Bajar lo nuevo de main | `git checkout main` y luego `git pull origin main` |
| Ver qué trae una rama frente a main | `git log --oneline main..origin/<rama>` |
| Unir una rama con main | `git checkout main`, `git pull origin main`, `git merge origin/<rama>`, `git push origin main` |
| Cancelar un merge con conflictos | `git merge --abort` |
| Descartar cambios de un archivo | `git restore <archivo>` |
| Sacar un archivo del add | `git restore --staged <archivo>` |
| Apartar mis cambios | `git stash` (recuperar: `git stash pop`) |
| Deshacer el último commit no subido | `git reset --soft HEAD~1` |
| Deshacer un commit ya subido | `git revert <código>` y luego `git push` |
| Ver el historial corto | `git log --oneline -10` |

**Nunca en `main`:** `git push --force` ni `git reset --hard`.
