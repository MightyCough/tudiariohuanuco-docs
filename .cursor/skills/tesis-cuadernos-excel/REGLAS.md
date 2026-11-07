# Reglas — cuadernos Excel de Seminario de Tesis III

Seminario de Tesis III, 062110052, Jenny Reynoso. Única fuente de las reglas: `SKILL.md`, `AGENTS.md` y los subagentes remiten aquí. Si un dato cambia, se cambia solo en este archivo.

Cuadernos en `instrumentos/sesion-01` … `sesion-11`. No hay sesión 8: la consolidación es la sesión 9. PDT vigente: `pdt/markdown/PDT-DIARIO-2026.md`.

## Diseño y muestra

- Diseño GU: O1 — X — O2. No hay grupo de comparación. En las plantillas el grupo único se guarda como GE, porque así cuentan las fórmulas. Si la plantilla habla de GC, marcar No aplica.
- Población N = 150. Muestra n = 108 (conveniencia, no probabilístico). 150 no es la muestra.
- Códigos GU-TDH-002 a GU-TDH-125 (108 en total, con huecos). No usar GU-TDH-001 ni P01.
- Retiros sin postest: GU-TDH-015, GU-TDH-033 y GU-TDH-053. El análisis apareado usa 105.
- Instrumentos de pretest y postest idénticos (SUS 10, TAM 8, tiempos y clics). Solo cambian las tareas 1-2 frente a 3-4.
- X dura 7 días y al menos 3 sesiones.

## Calendario

Pretest 12–17/10/2026, congelamiento el 18/10/2026 (tag v1.0.0-frozen-2026-10-18), intervención 19–25/10/2026, postest 26–31/10/2026, holgura 01–07/11/2026, cierre 08–12/11/2026. Capacitación el 17/10. Las autorizaciones del 10/07/2026 no se mueven.

## Llenado

- Solo celdas amarillas (relleno FFFDE7). El dato escrito va en azul. Las fórmulas van en celdas blancas y no se pisan.
- No copiar el ejemplo de clase: municipalidad, GE/GC, GE-001, n = 41 o n = 25, 6 semanas. Borrar sus filas de ejemplo.
- No inventar IP del VPS, otro tag Git ni firmas. La firma del asesor sigue pendiente.
- Stack del PDT: Next.js PWA, FastAPI, Supabase+pgvector, Redis, Gemini free, WordPress REST, Hostinger VPS KVM 1, Dokploy, chat.tudiariohuanuco.pe.
- No autocalificar rúbricas del docente.

## Datos simulados

Los 108 casos de las sesiones 1 a 11 son simulación del seminario, no campo real. El SUS del postest de la sesión 7 es simulado; no presentarlo como O2 de campo. La sesión 9 es v1.0-simulada, no liberada para campo.

## Sesiones 10 a 12

- Sesión 10: descriptivos por objetivo (caracterización, luego SUS, TAM, tiempo y clics en pretest y postest: n, media, mediana, DE, mínimo, máximo y niveles). No contrasta hipótesis ni dice «significativo».
- Sesión 11: normalidad de la diferencia postest ? pretest. Con n = 105 (> 50) es Kolmogorov-Smirnov con Lilliefors, no Shapiro-Wilk. Levene no aplica. Si p de Lilliefors < .05, Wilcoxon; si no, t para muestras relacionadas. ? = .05, bilateral. Sin valor p de t ni de Wilcoxon. La ficha se firma antes de contrastar.
- Sesión 12: solo hay PDF de clase (`clases/sesion-12-contrastacion/Sesion 12.pdf`), sin Excel en Drive. Contrasta con la prueba elegida en la 11. Reporta p, intervalo y tamaño del efecto. Dice «se rechaza H0» o «no se rechaza H0», nunca «se acepta H0».
- Nunca U de Mann-Whitney, chi-cuadrado ni Fisher: eran de otra tesis, de muestras independientes.

## Privacidad

La hoja «2. Libro de códigos» no está en este repositorio. El original, con nombres, sigue en Drive. No subir nombres, DNI, celular ni claves.
