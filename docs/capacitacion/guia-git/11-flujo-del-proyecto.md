# 11. Flujo del proyecto, de la rama al sitio

El recorrido completo, en el orden en que se hace.

## A. Cuando el cambio lo hace Claude

1. Claude trabaja en su rama (por ejemplo `claude/vibrant-bardeen-26cbjd`), hace el *commit* y el `push`, y avisa en el chat.
2. Usted trae la rama y la revisa en su computadora (archivo 6, punto 6.2), con Live Server si es una página del sitio.
3. Si está bien, la une con `main`: desde la terminal (archivo 7) o con un pull request (archivo 8).
4. Revisa el sitio publicado.

Claude no sube a `main` si usted no se lo pide ([ADR-016](../../../conocimiento/decisiones/ADR-016-confidencialidad-y-publicacion.md)).

## B. Cuando el cambio lo hace usted

1. **Ponga `main` al día:**

```bash
git checkout main
```

```bash
git pull origin main
```

2. **Cree su rama:**

```bash
git checkout -b ajuste-datos-computacion
```

3. **Haga el cambio en la fuente**, no en lo generado:

| Quiere cambiar… | Edite… |
|---|---|
| Un dato de un centro que sale en los diagramas | `centros/<centro>/datos.json` |
| El flujo de un diagrama | `herramientas/diagramas/plantillas.py` |
| Lo confirmado, las dudas (C##, U##…) | `.claude/skills/preguntas-y-dudas-centros/registro.md` |
| Una skill | `.claude/skills/<skill>/SKILL.md` |

4. **Regenere y valide** (requiere Python 3 y Node 18):

```bash
bash herramientas/diagramas/instalar_archify.sh
```

```bash
python3 herramientas/diagramas/generar.py
```

```bash
python3 herramientas/sincronizar_skills.py --desde claude
```

```bash
python3 herramientas/validar_conocimiento.py
```

   El validador debe terminar con **0 errores**.

5. **Revise y guarde:**

```bash
git status
```

```bash
git add -A
```

```bash
git commit -m "Qué cambió (C##)"
```

6. **Suba su rama:**

```bash
git push -u origin ajuste-datos-computacion
```

7. **Únala con `main`** (archivo 7 u 8) y revise el sitio.

## C. Dónde se ve cada cosa

| Qué | Dónde |
|---|---|
| Código y archivos | https://github.com/dagnerchuman/ellucian-instructivos |
| Sitio publicado (rama `main`) | https://centros-empresariales-ellucian.vercel.app |
| Galería de diagramas | https://centros-empresariales-ellucian.vercel.app/centros/index.html |
| Banner TEST (cada uno entra con su cuenta) | https://experience-test.elluciancloud.com/ussipantest |
