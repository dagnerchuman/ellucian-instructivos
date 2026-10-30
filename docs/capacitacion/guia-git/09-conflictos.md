# 9. Conflictos (cuando Git no puede unir dos cambios)

Un **conflicto** ocurre cuando dos ramas cambiaron las mismas líneas de un archivo y Git no sabe con cuál quedarse. Pasa en un `merge` o en un `pull`.

## 9.1 Cómo se ve

```bash
git status
```

Los archivos en conflicto salen como `both modified`. Dentro del archivo, Git marca las dos versiones:

```text
<<<<<<< HEAD
lo que tenía su rama
=======
lo que trae la otra rama
>>>>>>> origin/claude/vibrant-bardeen-26cbjd
```

## 9.2 Resolver un archivo de texto (.md, .json, .py)

1. Abra el archivo (Visual Studio Code muestra botones «Accept Current», «Accept Incoming» y «Accept Both»).
2. Deje el texto correcto y **borre las tres marcas** (`<<<<<<<`, `=======`, `>>>>>>>`).
3. En un `.json`, compruebe que siga siendo válido:

```bash
python3 -m json.tool centros/computacion/datos.json > /dev/null && echo "JSON válido"
```

4. Márquelo como resuelto:

```bash
git add centros/computacion/datos.json
```

5. Cuando no quede ninguno en `git status`, termine el merge:

```bash
git commit
```

## 9.3 Resolver los diagramas (HTML, PNG, SVG) y el asistente

Estos archivos se **generan**: no los arregle a mano. Resuelva primero `datos.json` (o la plantilla) y regenere:

```bash
python3 herramientas/diagramas/generar.py
```

Después:

```bash
git add -A
```

```bash
git commit
```

## 9.4 Cancelar el merge y volver a como estaba

```bash
git merge --abort
```

## 9.5 Cómo evitarlos

- Haga `git pull origin main` antes de empezar a trabajar.
- Una persona por archivo a la vez, sobre todo en `datos.json` y `registro.md`.
- Una las ramas pronto: cuanto más tiempo pasan separadas, más conflictos.

Siguiente: [10. Deshacer cambios](10-deshacer-cambios.md)
