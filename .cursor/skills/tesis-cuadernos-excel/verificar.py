"""Cruce mecánico de los cuadernos. Uso: python verificar.py (desde la raíz del repo). Requiere openpyxl.

Imprime OK o FALLA por regla y sale con código 1 si algo falla. No edita nada.
Las fórmulas sin valor guardado se leen como texto; por eso la diferencia de la sesión 11 se recalcula aquí.
"""
import re
import sys
from pathlib import Path

import openpyxl

RETIROS = {"GU-TDH-015", "GU-TDH-033", "GU-TDH-053"}
COD = re.compile(r"^GU-TDH-\d{3}$")
I = Path("instrumentos")
fallas = 0


def check(nombre, ok, detalle=""):
    global fallas
    fallas += not ok
    print(("OK    " if ok else "FALLA ") + nombre + (f" — {detalle}" if detalle and not ok else ""))


def filas(archivo, hoja, fila_titulos=4):
    ws = openpyxl.load_workbook(I / archivo, data_only=True)[hoja]
    rows = list(ws.iter_rows(min_row=fila_titulos, values_only=True))
    tit = [str(t).strip() if t else "" for t in rows[0]]
    return [dict(zip(tit, r)) for r in rows[1:] if r[0] and str(r[0]).startswith("GU-TDH")]


def codigos(archivo, hoja):
    ws = openpyxl.load_workbook(I / archivo, data_only=True)[hoja]
    return {str(r[0]) for r in ws.iter_rows(values_only=True) if r[0] and str(r[0]).startswith("GU-TDH")}


pre = codigos("sesion-03/Sesion 3.xlsx", "1. Base del pretest")
check("S3: 108 códigos en la base del pretest", len(pre) == 108, f"hay {len(pre)}")
check("S3: códigos con formato GU-TDH-###", all(COD.match(c) for c in pre))
check("S3: GU-TDH-001 no entra", "GU-TDH-001" not in pre)

s9 = filas("sesion-09/Sesion 9.xlsx", "5_Consolidada")
inc9 = {r["ID"] for r in s9 if r["INCLUIR"] == 1}
check("S9: mismos 108 códigos que S3", {r["ID"] for r in s9} == pre)
check("S9: INCLUIR = 1 en 105", len(inc9) == 105, f"hay {len(inc9)}")
check("S9: los retiros tienen INCLUIR = 0", not (inc9 & RETIROS))

s10 = filas("sesion-10/Sesion 10.xlsx", "1_Base_v1")
inc10 = {r["CODIGO"] for r in s10 if r["INCLUIR"] == 1}
check("S10: INCLUIR = 1 en los mismos 105 de S9", inc10 == inc9, f"sobran {sorted(inc10 - inc9)[:5]}, faltan {sorted(inc9 - inc10)[:5]}")

s11 = filas("sesion-11/Sesion 11.xlsx", "1_Base_v1")
check("S11: mismos 105 códigos que S10", {r["CODIGO"] for r in s11} == inc10)
check("S11: los retiros no aparecen", not ({r["CODIGO"] for r in s11} & RETIROS))
b10 = {r["CODIGO"]: r for r in s10}
vars_ = ["SUS_PRE", "SUS_POST", "TAM_PRE", "TAM_POST", "TIEMPO_PRE", "TIEMPO_POST", "CLICS_PRE", "CLICS_POST"]
dif = [(r["CODIGO"], v) for r in s11 for v in vars_ if r["CODIGO"] in b10 and r[v] != b10[r["CODIGO"]][v]]
check("S11: SUS, TAM, tiempo y clics iguales a S10, número a número", not dif, f"{len(dif)} celdas, p. ej. {dif[:3]}")

ws11 = openpyxl.load_workbook(I / "sesion-11/Sesion 11.xlsx")["1_Base_v1"]
mal = [c.coordinate for row in ws11.iter_rows(min_row=5, min_col=10, max_col=13) for c in row
       if c.value is not None and not re.fullmatch(r"=([CEGI])(\d+)-([BDFH])\2", str(c.value))]
check("S11: DIF = postest − pretest de la misma fila", not mal, f"celdas {mal[:5]}")


wsn = openpyxl.load_workbook(I / "sesion-11/Sesion 11.xlsx")["3_Normalidad"]
desfase = [c.coordinate for fila, col in zip(range(5, 9), "JKLM") for c in wsn[fila]
           if isinstance(c.value, str) and "1_Base_v1" in c.value
           and set(re.findall(r"!\$?([A-Z]+)\$?\d+:\$?([A-Z]+)", c.value)) != {(col, col)}]
check("S11 3_Normalidad: SUS, TAM, tiempo y clics leen DIF_SUS, DIF_TAM, DIF_TIEMPO y DIF_CLICS", not desfase,
      f"celdas {desfase[:5]}")


def textos(archivo):
    wb = openpyxl.load_workbook(I / archivo)
    return [(ws.title, c.coordinate, c.value) for ws in wb for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and not c.value.startswith("=")]


t10 = [x for x in textos("sesion-10/Sesion 10.xlsx") if re.search(r"\bsignificativ|se demuestra", x[2], re.I)]
check("S10: no dice «significativo» ni «se demuestra»", not t10, str(t10[:2]))
# Las celdas que nombran estas pruebas para descartarlas («no Shapiro-Wilk», «no corresponden») no cuentan.
t11 = [x for x in textos("sesion-11/Sesion 11.xlsx") if re.search(r"Mann|χ²|chi.cuadrado|Fisher|Shapiro", x[2], re.I)
       and not re.search(r"\bno\b|\bnunca\b", x[2], re.I)]
check("S11: sin Mann-Whitney, χ², Fisher ni Shapiro-Wilk como prueba elegida", not t11, str(t11[:2]))

sys.exit(1 if fallas else 0)
