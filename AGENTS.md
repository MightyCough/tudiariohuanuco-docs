# AGENTS.md

Instrucciones para agentes (Cursor, Claude Code, Codex) en `tudiariohuanuco-docs`, la base documental de la tesis de Tu Diario Huánuco. No hay `pnpm`, Vite ni Vitest: el trabajo es sobre Excel, Markdown y Word.

## Entorno

- No tocar `tudiariohuanuco-web` ni `tudiariohuanuco-api` desde aquí.
- Reglas de la tesis (n, códigos, calendario, pruebas): `.cursor/skills/tesis-cuadernos-excel/REGLAS.md`. Es la única fuente; no copiar sus cifras a otros archivos.
- PDT vigente: `pdt/markdown/PDT-DIARIO-2026.md` (copia del Word en `pdt/fuente/`). Si se corrige uno, se corrige el otro.
- Leer Excel con Python y `openpyxl`. Para editar, seguir la sección «Cómo editar un .xlsx sin romperlo» de `SKILL.md`.
- Archivos de texto en UTF-8.

## Revisión de cuadernos: dos agentes

1. **cruce-cuadernos** (modelo rápido): corre `verificar.py` y compara celdas. No redacta conclusiones estadísticas.
2. **criterio-estadistico** (modelo más capaz): juzga si la prueba elegida cuadra con el diseño, según REGLAS.md. No inventa puntajes ni valores p.

Las definiciones están en `.cursor/agents/` (Cursor) y `.claude/agents/` (Claude Code), con el mismo texto.

## Antes de un PR

- Título: `[tudiariohuanuco-docs] <qué cambió>`.
- No subir nombres, DNI, celular ni claves. El libro de códigos se queda en Drive.
- No incluir archivos de `Downloads` ni de otra tesis.
- Revisar `git status` y no mezclar cambios ajenos al cuaderno que se tocó.
- Entra a `main` solo si `verificar.py` sale sin FALLA y el agente de criterio no encuentra un desajuste de prueba.
