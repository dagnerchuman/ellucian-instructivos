# 8. Pull request en GitHub (merge sin terminal)

Un **pull request** (PR) es una solicitud para unir una rama con `main` desde la página de GitHub. Permite revisar los cambios, comentarlos y unirlos con un botón. Hace lo mismo que el archivo 7.

## 8.1 Crear el pull request

1. Abra https://github.com/dagnerchuman/ellucian-instructivos.
2. Si la rama se subió hace poco, aparece una franja amarilla con el botón **«Compare & pull request»**: púlselo. Si no aparece, vaya a la pestaña **Pull requests** › **New pull request**.
3. Revise arriba: **base: `main`** ← **compare: `claude/vibrant-bardeen-26cbjd`** (la rama que quiere unir).
4. Escriba un título corto y, en la descripción, qué cambia y su referencia (C##).
5. Pulse **«Create pull request»**.

## 8.2 Revisar

- Pestaña **Commits:** los *commits* que trae.
- Pestaña **Files changed:** cada archivo, con lo agregado en verde y lo quitado en rojo. Los HTML de los diagramas cambian en una sola línea muy larga: es normal, se regeneran.
- Si algo no está bien, deje un comentario en la línea; Claude u otra persona lo corrige en la misma rama y el PR se actualiza solo.

## 8.3 Unir (merge)

1. Al final de la pestaña **Conversation**, pulse **«Merge pull request»** › **«Confirm merge»**.
2. GitHub ofrece **«Delete branch»**. Bórrela solo si ya no se va a seguir trabajando en ella.
3. En uno o dos minutos el cambio está en el sitio.

## 8.4 Si GitHub dice «This branch has conflicts»

El botón de merge queda gris. Use **«Resolve conflicts»** en la página si son pocos y de texto, o resuélvalos en su computadora (archivo 9) y suba la rama otra vez.

## 8.5 Después del merge, en su computadora

```bash
git checkout main
```

```bash
git pull origin main
```

Siguiente: [9. Conflictos](09-conflictos.md)
