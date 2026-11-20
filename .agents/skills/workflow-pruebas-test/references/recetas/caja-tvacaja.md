# Recetas de TEST: Caja (TVACAJA), solo consulta

**No es de los centros.** La caja es de la Capacidad 11 (Finanzas); los Centros Empresariales son la Capacidad 1 (diseño curricular). Se estudió para saberlo, a pedido del usuario: «lo que no corresponde a centros empresariales… pero tenemos que saber de todo» (C217). Antes, lee las reglas y cómo moverse en [manejo-banner-test.md](../manejo-banner-test.md): **nunca se guarda sin permiso del usuario**. Fuente: instructivo 11.2.2 «Gestionar los pagos», diap. 38 a 60.

### Revisar los cargos de un alumno en la caja (TVACAJA, C217)
1. **TOADEST primero.** Al abrir TVACAJA, TGAUPRF u otra página de cuentas por cobrar en una sesión nueva, Banner manda a **TOADEST** «Inicialización de distribución de cuentas por cobrar» con el aviso *«No se ha completado la configuración requerida»*. Se escribe `DATABASE` en **Facturas**, **Recibos** y **Resumen de alumno** (clic, escribir, Tab, 2 s por campo) y se cierra con la **X** de arriba: Banner vuelve solo a la página pedida. No se guarda (igual que SOADEST, C185).
2. **Bloque clave:** **Periodo** (obligatorio) › Tab › **ID** › Tab (sale el nombre) › **Ir**. Arriba quedan la divisa (`PEN`) y el usuario que cobra.
3. **Bloque «Cajero»:** todos los cargos con saldo del alumno, **de todos sus periodos** aunque arriba se elija uno: descripción, fecha de vigencia, monto, intereses de mora, multa, total, casilla **«Agregar valor total»** y código. Con la rueda a la derecha: monto a pagar, capital, intereses, número de transacción, **Periodo** y plan de estudios. 5 por página.
4. **Bloque «Descuentos»** y **«Total de monto a pagar»**: una fila por medio de pago con **Código de detalle** (obligatorio), monto, número de documento, banco, plaza, cuenta, **Fecha** (Banner pone la de hoy al elegir el código) y texto. Botones **Texto**, **Imprimir recibo** y **Crear documento de ventas**; abajo, «Total a pagar», «Reembolso» y «Número de recibo».
5. **Para cobrar** (no probado, 11.2.2 diap. 41 a 45): marcar los cargos › código de pago y monto › GUARDAR › **OK** en la ventana del monto › sale el número de recibo › «Imprimir recibo». En TSAAREV el cargo y el pago quedan con el mismo recibo.
6. **Salir sin guardar:** si se tocó una fila de pago, quitarla con **–** del bloque y navegar descartando los cambios.

**Ojo con la lista de códigos (TBBDETC):** **Intro** dentro de la lista elige la primera fila (`A023`), como en C164. Para buscar, desplázate o cambia a 50 por página; cierra con **Anular**.

### Códigos de pago (TBBDETC, 138 de tipo P, PEN, 20/11/2026)
- **Medios de pago:** `M001` Efectivo, `M002` Cheque, `M003` Niubiz web, `M004` POS Niubiz, `M005` POS Culqi, `M006` a `M011` BBVA (terminal, banca por internet, Redex, cajero, Saldo Express, banca por teléfono), `M012` a `M023` BCP (banca móvil, Telecrédito, banca por internet, ventanilla, agente y cajero; cada uno en «Mat Pen» y «Ser Prog»), `M024` y `M025` KasNet, `M026` a `M039` depósitos en cuentas del BCP, BBVA, Banco de la Nación, BanBif y Caja Piura.
- **Otros abonos:** `A0xx` autorizaciones y resoluciones, `A076` a `A108` descuentos (pronto pago, cuota puntual, Black Friday, colaborador), `A109` a `A116` y `DEV*` devoluciones, `CN**` condonaciones, `CR**` créditos de repactación, `DEPO`/`DEPP` depósito de preingresante, `PPLP`/`PLAP` plan cronograma cancelado, `Y002` a `Y010` plan de contratos cancelado.
- **Posibles de los centros (por confirmar con Finanzas):** `A085` «Descuento (5%) Pago Contado Ce», `X004` «Descuento Black Friday Ce», `X217` «Descuento Cyber Ce», `Y004` «Plan Contratos Cancelado Ce» y `A102` «Descuento Black Friday Ed.C». «Ce» parece Centros Empresariales y «Ed.C», Educación Continua.

### Quién puede cobrar (TGAUPRF y TGIUPRF, C217)
- **TGAUPRF** › ID de usuario › Ir. Para `DCHUMAN` (el usuario de Dagner): *«ID de usuario no definido, oprima BLOQUE SIGUIENTE para agregar»*, es decir, **sin perfil de cajero**. No se agregó.
- El ••• del ID abre **TGIUPRF** «Consulta de perfil de usuario»: 18 usuarios con perfil, con las casillas Supervisor y Restringido. No se copian sus nombres.
- El perfil (TGAUPRF, 11.2.2 diap. 13 a 18) define qué categorías de códigos puede usar el cajero; con TGACTRL «Imponer restricciones en el perfil de usuario» activo, sin perfil no se cobra (diap. 11).

### Lo que se vio de Arnold Vaca (`S00912438`) en 202754
9 cargos con saldo: dos pensiones `P006` (S/ 5,167.50 y S/ 2,940.00) del periodo **202744** (Medicina), `X228` licencia de Inglés S/ 80.00 y seis cuotas `PPLC` del plan de pagos (S/ 139.99 a 166.67, de mayo a julio de 2027). El `X032` de Basic I (S/ 420, C75) ya no sale con saldo: con el plan de pagos el cargo original se cancela con `PPLP` y se cobra en cuotas `PPLC` (C76, C80).
