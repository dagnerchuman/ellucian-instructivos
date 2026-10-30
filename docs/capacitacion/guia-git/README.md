# Guía de Git y GitHub para el proyecto

Pasos para trabajar con el repositorio **`dagnerchuman/ellucian-instructivos`**: bajarlo, cambiar de rama, guardar cambios, subirlos a GitHub y llevarlos a `main`, que es lo que se publica en el sitio. Cada tema está en su propio archivo; léalos en orden la primera vez.

| N.º | Archivo | Para qué sirve |
|---|---|---|
| 1 | [01-preparar-git.md](01-preparar-git.md) | Instalar Git, poner su nombre y entrar a GitHub (una sola vez por computadora) |
| 2 | [02-clonar-el-repositorio.md](02-clonar-el-repositorio.md) | Bajar el proyecto a su computadora (una sola vez) |
| 3 | [03-ramas-y-checkout.md](03-ramas-y-checkout.md) | Ver las ramas, cambiarse a otra (`checkout`) y crear una nueva |
| 4 | [04-guardar-cambios-commit.md](04-guardar-cambios-commit.md) | Revisar qué cambió y guardarlo en un *commit* |
| 5 | [05-subir-a-github-push.md](05-subir-a-github-push.md) | Subir los *commits* a GitHub (`push`) |
| 6 | [06-traer-cambios-pull.md](06-traer-cambios-pull.md) | Bajar lo que otros (o Claude) subieron (`pull`) |
| 7 | [07-merge-a-main.md](07-merge-a-main.md) | Unir una rama con `main` desde la terminal (`merge`) y publicar |
| 8 | [08-pull-request-en-github.md](08-pull-request-en-github.md) | Hacer lo mismo desde la página de GitHub, sin terminal |
| 9 | [09-conflictos.md](09-conflictos.md) | Qué hacer si Git no puede unir dos cambios |
| 10 | [10-deshacer-cambios.md](10-deshacer-cambios.md) | Volver atrás un archivo o un *commit* sin perder trabajo |
| 11 | [11-flujo-del-proyecto.md](11-flujo-del-proyecto.md) | El recorrido completo de este proyecto, de la rama al sitio publicado |
| 12 | [12-comandos-rapidos.md](12-comandos-rapidos.md) | Hoja de consulta con todos los comandos |

## Cinco palabras que hay que conocer

| Palabra | Qué es |
|---|---|
| **Repositorio** | La carpeta del proyecto con todo su historial. Hay una copia en GitHub (*remoto*, se llama `origin`) y otra en su computadora (*local*) |
| **Rama** (*branch*) | Una línea de trabajo. `main` es la oficial; las demás (por ejemplo `claude/vibrant-bardeen-26cbjd`) sirven para trabajar sin tocar `main` |
| **Commit** | Una foto de los cambios, con un mensaje que dice qué se hizo |
| **Push / Pull** | `push` sube sus *commits* a GitHub; `pull` baja los de GitHub a su computadora |
| **Merge** | Une los *commits* de una rama con otra; aquí, de la rama de trabajo a `main` |

## Lo más importante de este proyecto

- **`main` es el sitio publicado.** Lo que llega a `main` aparece en https://centros-empresariales-ellucian.vercel.app en uno o dos minutos. Se trabaja en una rama y a `main` se lleva solo lo que el responsable aprueba ([ADR-016](../../../conocimiento/decisiones/ADR-016-confidencialidad-y-publicacion.md)).
- **Claude sube su trabajo a su propia rama** (`claude/...`), nunca a `main`. Usted revisa y hace el *merge* (archivos 7 u 8).
- **Los diagramas no se editan a mano:** se cambia `centros/<centro>/datos.json` y se regeneran (archivo 11).
- **Nunca escriba contraseñas, tokens ni datos de alumnos** en los archivos ni en los mensajes de *commit*.

Los comandos se escriben en la **Terminal** (Mac: Aplicaciones › Utilidades › Terminal) o en **Git Bash** (Windows), dentro de la carpeta del proyecto.
