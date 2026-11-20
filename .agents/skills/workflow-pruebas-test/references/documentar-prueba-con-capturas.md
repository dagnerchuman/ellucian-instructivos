# Documentar una prueba con capturas para el sitio

Parte de la skill `workflow-pruebas-test` (el mapa está en su `SKILL.md`).

## 7. Documentar una prueba con capturas para el sitio (C181, C192–C195)
Así se documentó la prueba del NRC 10045; sirve para cualquier prueba nueva.
1. **Ventana de 800 × 670** en el navegador (las capturas quedan de 800 px de ancho) y **una captura por pantalla**: el bloque clave escrito **antes de pulsar Ir**, cada bloque que se llena, el aviso de Banner y la comprobación al reabrir. Todo lo que muestre una lámina del instructivo de ese paso debe tener su captura (C194).
2. Se guarda como `NN-tema.png`, `NN-tema-b.png`… en la carpeta del ejemplo, junto al HTML de la demostración (`sips -s format png` desde la captura del navegador).
3. En `datos.json › demostraciones › ejemplo_prueba_2 › pasos`, cada paso lleva `tabla` (Campo, Valor, Quién lo pone, Nota), `resultado`, `cita`, `capturas` en el orden de las láminas, `laminas` y `etiqueta`; las `fases` agrupan los pasos en filas del flujo (C192).
4. **Cuadros y números** (C195): cada captura lleva `cuadros` `{n, caja}`, donde `n` es la fila de la tabla del paso. Para ubicarlos, usa el OCR de `herramientas/diagramas/ocr_capturas.swift` y revisa una hoja de contacto por paso antes de subir. `generar.py` dibuja las copias en `anotadas/`.
5. Regenera con `python3 herramientas/diagramas/generar.py` y abre el paso en el modal de «Prueba en TEST»: las capturas cargan, «Ver sin cuadros» alterna y los números de «Su guía» coinciden con los de la imagen.
6. Solo consulta en las capturas de complemento: no se guarda nada en Banner sin que el usuario lo pida (sección 1 de `manejo-banner-test.md`).
