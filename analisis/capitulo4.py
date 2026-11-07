"""Salidas del Capítulo IV (Sesión 12) a partir de los cuadernos. Datos simulados del seminario.

Uso, desde la raíz del repo: python analisis/capitulo4.py
Requiere openpyxl, numpy, scipy, statsmodels y matplotlib.
Escribe analisis/salidas/capitulo4.txt y analisis/salidas/figura-4-1.png. No edita los cuadernos.

Fuentes: sesión 3 (ítems del pretest, n = 108), sesión 7 hoja 6b (ítems del postest, 105 pares)
y sesión 10 hoja 1_Base_v1 (totales). El script comprueba que los totales que recalcula
coinciden con los de la sesión 10 y que el Lilliefors coincide con la sesión 11.
"""
from pathlib import Path

import numpy as np
import openpyxl
from scipy import stats
from statsmodels.stats.diagnostic import lilliefors

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

I = Path("instrumentos")
OUT = Path("analisis/salidas")
OUT.mkdir(parents=True, exist_ok=True)
lineas = []


def p(*a):
    lineas.append(" ".join(str(x) for x in a))


def hoja(archivo, nombre, fila_titulos=4):
    ws = openpyxl.load_workbook(I / archivo, data_only=True)[nombre]
    rows = list(ws.iter_rows(min_row=fila_titulos, values_only=True))
    tit = [str(t).strip() if t else "" for t in rows[0]]
    return {str(r[0]): dict(zip(tit, r)) for r in rows[1:] if r[0] and str(r[0]).startswith("GU-TDH")}


pre = hoja("sesion-03/Sesion 3.xlsx", "1. Base del pretest")
post = hoja("sesion-07/Sesion 7.xlsx", "6b_Base_Completa")
s10 = hoja("sesion-10/Sesion 10.xlsx", "1_Base_v1")
pares = sorted(c for c, r in s10.items() if r["INCLUIR"] == 1)
assert len(pre) == 108 and len(pares) == 105 and set(pares) <= set(post)


def sus(items):  # Brooke (1996): impares − 1, pares 5 − x, suma × 2.5
    return 2.5 * sum((x - 1) if i % 2 else (5 - x) for i, x in enumerate(items, 1))


def sus_factores(items):  # Lewis y Sauro (2009): Usability = 8 ítems × 3.125; Learnability = 4 y 10 × 12.5
    c = [(x - 1) if i % 2 else (5 - x) for i, x in enumerate(items, 1)]
    return sum(c[j] for j in (0, 1, 2, 4, 5, 6, 7, 8)) * 3.125, (c[3] + c[9]) * 12.5


def items(r, pref, suf, n):
    return [float(r[f"{pref}{k:02d}{suf}"]) for k in range(1, n + 1)]


V = {}  # indicador -> (pretest, postest) sobre los 105 pares
for m, src, suf in (("PRE", pre, ""), ("POST", post, "_post")):
    S = [items(src[c], "sus", suf, 10) for c in pares]
    T = [items(src[c], "tam", suf, 8) for c in pares]
    V.setdefault("SUS", []).append(np.array([sus(x) for x in S]))
    V.setdefault("SUS Usability", []).append(np.array([sus_factores(x)[0] for x in S]))
    V.setdefault("SUS Learnability", []).append(np.array([sus_factores(x)[1] for x in S]))
    V.setdefault("TAM", []).append(np.array([sum(x) for x in T]))
    V.setdefault("TAM 3.1 satisfacción general", []).append(np.array([sum(x[:6]) for x in T]))
    V.setdefault("TAM 3.2 intención de reutilización", []).append(np.array([sum(x[6:]) for x in T]))
    V.setdefault("Tiempo (s)", []).append(np.array([float(s10[c][f"TIEMPO_{m}"]) for c in pares]))
    V.setdefault("Clics", []).append(np.array([float(s10[c][f"CLICS_{m}"]) for c in pares]))

# Control: los totales recalculados desde los ítems son los de la sesión 10.
for k, col in (("SUS", "SUS"), ("TAM", "TAM")):
    for j, m in enumerate(("PRE", "POST")):
        assert np.allclose(V[k][j], [float(s10[c][f"{col}_{m}"]) for c in pares]), (k, m)

p("CAPÍTULO IV — SALIDAS. DATOS SIMULADOS DEL SEMINARIO, NO SON MEDICIÓN DE CAMPO.")
p("Fuentes: S3 (pretest), S7 hoja 6b (postest), S10 hoja 1_Base_v1. Pares: 105. Retiros: GU-TDH-015, 033, 053.\n")

# 4.1 Caracterización (n = 108)
b = [s10[c] for c in sorted(s10)]
edad = np.array([float(r["EDAD"]) for r in b])
frec = np.array([float(r["FREC_SEM"]) for r in b])
p("== Tabla 4.1 Caracterización (n = 108)")
for nom, val, cat in (("Zona", "ZONA", {1: "Urbana", 2: "Periurbana"}),
                      ("Red", "RED", {1: "3G", 2: "4G", 3: "5G", 4: "Wi-Fi"})):
    for k, et in cat.items():
        f = sum(1 for r in b if int(r[val]) == k)
        p(f"{nom} | {et} | {f} | {f / 108 * 100:.1f}")
for et, lo, hi in (("18–29", 18, 29), ("30–44", 30, 44), ("45–59", 45, 59), ("60 o más", 60, 999)):
    f = int(((edad >= lo) & (edad <= hi)).sum())
    p(f"Edad | {et} | {f} | {f / 108 * 100:.1f}")
for et, lo, hi in (("3–6", 3, 6), ("7–11", 7, 11), ("12 o más", 12, 999)):
    f = int(((frec >= lo) & (frec <= hi)).sum())
    p(f"Lectura semanal | {et} | {f} | {f / 108 * 100:.1f}")
p(f"Edad M (DE) = {edad.mean():.2f} ({edad.std(ddof=1):.2f}); Me = {np.median(edad):.1f}; rango {edad.min():.0f}–{edad.max():.0f}")
p(f"Frecuencia semanal M (DE) = {frec.mean():.2f} ({frec.std(ddof=1):.2f})\n")

# 4.1 Descriptivos por indicador
p("== Tabla 4.2 Descriptivos por indicador y momento (n = 105)")
p("Indicador | Momento | M | DE | Me | Q1 | Q3 | Mín | Máx | Asimetría")
for k, (a, z) in V.items():
    for m, x in (("Pretest", a), ("Postest", z)):
        q1, q3 = np.percentile(x, [25, 75])
        p(f"{k} | {m} | {x.mean():.2f} | {x.std(ddof=1):.2f} | {np.median(x):.2f} | {q1:.2f} | {q3:.2f} | "
          f"{x.min():.2f} | {x.max():.2f} | {stats.skew(x, bias=False):.2f}")

p("\n== Tabla 4.3 Niveles (cortes a priori de la sesión 10)")
for k, cortes in (("SUS", (33, 66)), ("TAM", (18, 29))):
    for m, x in zip(("Pretest", "Postest"), V[k]):
        f = [int((x <= cortes[0]).sum()), int(((x > cortes[0]) & (x <= cortes[1])).sum()), int((x > cortes[1]).sum())]
        p(f"{k} {m}: Bajo {f[0]} ({f[0] / 1.05:.1f} %), Medio {f[1]} ({f[1] / 1.05:.1f} %), Alto {f[2]} ({f[2] / 1.05:.1f} %)")
for m, x in zip(("Pretest", "Postest"), V["SUS"]):
    f = int((x >= 68).sum())
    p(f"SUS ≥ 68 (umbral de aceptabilidad) {m}: {f} ({f / 1.05:.1f} %)")

p("\n== Tabla 4.4 Diferencia postest − pretest")
p("Indicador | M pre | M post | Dif. M | % cambio | Me dif | Mín dif | Máx dif | Mejoraron")
for k, (a, z) in V.items():
    d = z - a
    mejor = int((d < 0).sum() if k in ("Tiempo (s)", "Clics") else (d > 0).sum())
    p(f"{k} | {a.mean():.2f} | {z.mean():.2f} | {d.mean():.2f} | {d.mean() / a.mean() * 100:.1f} | {np.median(d):.2f} | "
      f"{d.min():.2f} | {d.max():.2f} | {mejor} ({mejor / 1.05:.1f} %)")

# 4.2 Supuestos
P = {"He1 SUS": "SUS", "He2 tiempo": "Tiempo (s)", "He3 TAM": "TAM", "Complementaria clics": "Clics"}
S11 = {"SUS": (0.0924, 0.0272), "TAM": (0.07, 0.2301), "Tiempo (s)": (0.0466, 0.841), "Clics": (0.0706, 0.221)}
p("\n== Tabla 4.5 Normalidad de la diferencia: K-S con corrección de Lilliefors (n = 105)")
p("Diferencia | M | DE | Asimetría | Curtosis | D | p | Decisión | S11 (D; p)")
normal = {}
for h, k in P.items():
    d = V[k][1] - V[k][0]
    D, pv = lilliefors(d, dist="norm", pvalmethod="approx")
    normal[k] = pv >= 0.05
    p(f"DIF {k} | {d.mean():.2f} | {d.std(ddof=1):.2f} | {stats.skew(d, bias=False):.2f} | "
      f"{stats.kurtosis(d, bias=False):.2f} | {D:.4f} | {pv:.4f} | {'normal' if normal[k] else 'no normal'} | "
      f"{S11[k][0]}; {S11[k][1]}")
    assert normal[k] == (S11[k][1] >= 0.05), f"La decisión de normalidad de {k} no coincide con la sesión 11"
p("Levene: no aplica (muestras relacionadas, sin grupo de comparación).")


def hodges_lehmann(d, conf=0.95):
    w = np.sort(np.add.outer(d, d)[np.triu_indices(len(d))] / 2)  # promedios de Walsh
    n = len(d)
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    k = int(np.floor(n * (n + 1) / 4 - z * np.sqrt(n * (n + 1) * (2 * n + 1) / 24)))
    return np.median(w), w[k], w[len(w) - k - 1]


def wilcoxon_z(d):  # aproximación normal con corrección por empates, sin corrección de continuidad (como SPSS)
    d = d[d != 0]
    n = len(d)
    r = stats.rankdata(np.abs(d))
    wp = r[d > 0].sum()
    _, cnt = np.unique(np.abs(d), return_counts=True)
    var = n * (n + 1) * (2 * n + 1) / 24 - (cnt ** 3 - cnt).sum() / 48
    zval = (wp - n * (n + 1) / 4) / np.sqrt(var)
    return wp, r[d < 0].sum(), n, zval, 2 * stats.norm.sf(abs(zval))


p("\n== Tablas 4.6 a 4.9 Contrastación (α = .05, bilateral; d = postest − pretest)")
res = {}
for h, k in P.items():
    a, z = V[k]
    d = z - a
    n = len(d)
    if normal[k]:
        t, pv = stats.ttest_rel(z, a)
        ci = stats.t.interval(0.95, n - 1, loc=d.mean(), scale=d.std(ddof=1) / np.sqrt(n))
        dz = d.mean() / d.std(ddof=1)
        g = dz * (1 - 3 / (4 * (n - 1) - 1))
        res[h] = pv
        p(f"{h}: t relacionada | M dif = {d.mean():.2f}, DE dif = {d.std(ddof=1):.2f} | t({n - 1}) = {t:.2f} | "
          f"p = {pv:.3g} | IC 95 % [{ci[0]:.2f}; {ci[1]:.2f}] | dz = {dz:.2f} | g = {g:.2f}")
    else:
        wp, wn, nn, zval, pv = wilcoxon_z(d)
        hl, lo, hi = hodges_lehmann(d)
        r = abs(zval) / np.sqrt(n)
        res[h] = pv
        p(f"{h}: Wilcoxon | rangos + = {wp:.1f}, rangos − = {wn:.1f}, n sin empates en 0 = {nn} | Z = {zval:.2f} | "
          f"p = {pv:.3g} | Me dif = {np.median(d):.2f} | HL = {hl:.2f}, IC 95 % [{lo:.2f}; {hi:.2f}] | r = {r:.2f}")
        t, pt = stats.ttest_rel(z, a)
        p(f"   Sensibilidad (t relacionada sobre la misma DIF): t({n - 1}) = {t:.2f}, p = {pt:.3g}, "
          f"dz = {d.mean() / d.std(ddof=1):.2f}")

rech = [h for h in ("He1 SUS", "He2 tiempo", "He3 TAM") if res[h] < 0.05]
p(f"\nHg (regla del PDT §3.6.4: se rechaza H0 general si se rechazan las tres H0 específicas): "
  f"{'se rechaza H0' if len(rech) == 3 else 'no se rechaza H0'} ({len(rech)} de 3).")
p(f"Robustez con Bonferroni (α/3 = .0167): {sum(res[h] < 0.05 / 3 for h in ('He1 SUS', 'He2 tiempo', 'He3 TAM'))} de 3 por debajo.")

# Figura 4.1
fig, ax = plt.subplots(1, 4, figsize=(11, 3.6))
for i, (k, u) in enumerate((("SUS", "puntos (0–100)"), ("Tiempo (s)", "segundos"), ("TAM", "puntos (8–40)"), ("Clics", "clics"))):
    ax[i].boxplot(V[k], tick_labels=["Pretest", "Postest"], widths=0.5,
                  medianprops={"color": "black"}, boxprops={"color": "#333"}, flierprops={"markersize": 3})
    ax[i].set_title(k.replace(" (s)", ""), fontsize=10)
    ax[i].set_ylabel(u, fontsize=9)
    ax[i].tick_params(labelsize=8)
    ax[i].spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "figura-4-1.png", dpi=200)

(OUT / "capitulo4.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("\n".join(lineas))
