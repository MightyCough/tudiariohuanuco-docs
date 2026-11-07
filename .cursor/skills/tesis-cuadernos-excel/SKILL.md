---
name: tesis-cuadernos-excel
description: >-
  Reglas y procedimiento para llenar, corregir o revisar los cuadernos Excel del
  Seminario de Tesis III (Tu Diario Huánuco): Sesion 1.xlsx a Sesion 11.xlsx,
  códigos GU-TDH, pretest, intervención, postest, muestra n = 108, pares 105,
  descriptivos, normalidad, elección de prueba o rúbricas de esos cuadernos.
---

# Cuadernos Excel — Seminario de Tesis III

1. Lee [REGLAS.md](REGLAS.md) antes de tocar una celda. Ahí están n, códigos, calendario y pruebas; no los repitas en otro archivo.
2. Corre el cruce desde la raíz del repo: `python .cursor/skills/tesis-cuadernos-excel/verificar.py` (necesita `openpyxl`). Si algo sale FALLA, arréglalo o dilo antes de seguir.
3. Edita solo celdas amarillas y vuelve a correr el cruce.

## Cómo editar un .xlsx sin romperlo

- `openpyxl` al guardar borra los gráficos y las imágenes. Las sesiones 5, 6 y 7 tienen gráficos. Para cambiar un texto, reemplaza dentro del XML del zip (`xl/worksheets/sheetN.xml` o `xl/sharedStrings.xml`) y deja intactas las demás entradas.
- En el XML los acentos y guiones pueden venir como entidades (`&#233;`, `&#8211;`). Busca con la forma que tiene el archivo y exige una sola coincidencia.
- Con `data_only=True` las fórmulas que Excel no recalculó salen como `None`. No las tomes por vacías.
- Cuenta las fórmulas antes y después de editar; el número tiene que ser el mismo.

## Al terminar

- Si cambiaste un dato que fija una regla (fecha, n, código), actualiza `REGLAS.md` y el README de la sesión.
- Separa en commits distintos los cuadernos y el PDT. No subas el libro de códigos.
