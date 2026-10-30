# 1. Preparar Git (una sola vez por computadora)

## 1.1 Comprobar si Git está instalado

```bash
git --version
```

- Si responde algo como `git version 2.x`, ya está instalado: pase al punto 1.2.
- **Mac:** si no está, el sistema ofrece instalar las «herramientas de línea de comandos». Acepte, o escriba:

```bash
xcode-select --install
```

- **Windows:** descargue «Git for Windows» desde https://git-scm.com y use **Git Bash** para los comandos de esta guía.

## 1.2 Poner su nombre y correo

Git firma cada *commit* con estos datos. Use el mismo correo de su cuenta de GitHub. Reemplace el texto entre comillas por el suyo:

```bash
git config --global user.name "Nombre Apellido"
```

```bash
git config --global user.email "su-correo@ejemplo.com"
```

Para revisar lo que quedó:

```bash
git config --global --list
```

## 1.3 Entrar a GitHub desde la computadora

Elija **una** de estas formas:

| Forma | Cómo |
|---|---|
| **GitHub CLI** (recomendada) | Instale `gh` (https://cli.github.com), escriba `gh auth login`, elija *GitHub.com* › *HTTPS* › *Login with a web browser* y siga el código que aparece |
| **GitHub Desktop** | Instale la aplicación, entre con su cuenta y clone desde ahí. Los comandos de esta guía siguen funcionando en la Terminal |
| **Token personal** | GitHub › Settings › Developer settings › Personal access tokens. El token se pega cuando Git pide la contraseña. **No lo guarde en ningún archivo del proyecto** |

GitHub ya no acepta la contraseña de la cuenta para `git push`: hace falta una de estas tres formas.

## 1.4 Permiso para subir

Para hacer `push` al repositorio `dagnerchuman/ellucian-instructivos` su cuenta tiene que estar invitada como colaborador. Si al subir aparece `Permission denied` o `403`, pida la invitación al responsable del repositorio.

Siguiente: [2. Clonar el repositorio](02-clonar-el-repositorio.md)
