# 2. Clonar el repositorio (bajar el proyecto)

*Clonar* es bajar a su computadora una copia completa del proyecto, con su historial. Se hace una sola vez.

## 2.1 Elegir dónde guardarlo

Vaya a la carpeta donde quiere el proyecto (por ejemplo, Documentos):

```bash
cd ~/Documents
```

## 2.2 Clonar

```bash
git clone https://github.com/dagnerchuman/ellucian-instructivos.git
```

Se crea la carpeta `ellucian-instructivos`. Entre en ella; todos los demás comandos se escriben desde aquí:

```bash
cd ellucian-instructivos
```

## 2.3 Comprobar

```bash
git status
```

Debe decir `On branch main` y `nothing to commit, working tree clean`: tiene la copia de `main` sin cambios.

## 2.4 Abrir el sitio en su computadora (opcional)

Con la extensión **Live Server** de Visual Studio Code, abra la carpeta y elija «Open with Live Server» sobre `centros/index.html`. Queda en una dirección como `http://127.0.0.1:5500/centros/index.html`. Así se ve un cambio antes de subirlo.

Siguiente: [3. Ramas y checkout](03-ramas-y-checkout.md)
