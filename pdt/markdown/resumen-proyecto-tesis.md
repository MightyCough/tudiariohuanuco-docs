> Exportado del Google Doc de Drive el 26 de octubre de 2026. Es un resumen anterior. El documento vigente es [PDT-DIARIO-2026.md](PDT-DIARIO-2026.md): N = 150, n = 108 y el título de la aplicación multiplataforma. Este archivo todavía habla de una muestra de 30 a 40 lectores y de un título previo. No usarlo para llenar los cuadernos.

**RESUMEN MAESTRO**

**DEL PROYECTO DE TESIS**

*Influencia de una aplicación web con asistente conversacional*

*en la experiencia de lectores de un diario digital en Huánuco, 2026*

Universidad de Huánuco

Escuela Profesional de Ingeniería de Sistemas e Informática

*Documento de referencia técnica y metodológica*

**1. Identidad del proyecto**

**Título de tesis:** Influencia de una aplicación web con asistente conversacional en la experiencia de lectores de un diario digital en Huánuco, 2026.

**Universidad:** Universidad de Huánuco (UDH), Escuela Profesional de Ingeniería de Sistemas e Informática.

**Caso de estudio:** Diario digital Tu Diario Huánuco (tudiariohuanuco.pe).

**Línea de investigación:** N° 21 - Tecnologías de la Información y Comunicación.

**Duración total:** 6 meses (24 semanas) divididos en 13 sprints quincenales más fase de recolección de datos.

**Costo total estimado:** menos de 5 USD durante toda la tesis (~S/ 20).

**2. Marco metodológico**

| **Aspecto** | **Decisión** |
|----|----|
| **Tipo** | Aplicada |
| **Enfoque** | Cuantitativo |
| **Nivel** | Aplicativo |
| **Diseño** | Preexperimental con pretest-postest |
| **Población** | Lectores mayores de 18 años residentes en Huánuco |
| **Muestra** | 30-40 lectores |
| **Muestreo** | No probabilístico por conveniencia |
| **Variable independiente** | Aplicación web con asistente conversacional |
| **Variable dependiente** | Experiencia del lector (3 dimensiones) |

**Dimensiones de la variable dependiente**

> **•** Usabilidad percibida medida con escala SUS (System Usability Scale) de Brooke (1996).
>
> **•** Tiempo de búsqueda de información medido en segundos a través de 5 tareas estandarizadas.
>
> **•** Nivel de satisfacción medido con escala Likert basada en el modelo TAM de Davis (1989).

**Análisis estadístico previsto**

Prueba t de Student para muestras relacionadas (si hay normalidad) o prueba de Wilcoxon (si no la hay). Nivel de significancia α=0.05.

**3. Hipótesis**

**Hipótesis general**

**Hi:** La aplicación web con asistente conversacional influye significativamente en la experiencia de lectores de un diario digital en Huánuco, 2026.

**H0:** La aplicación web con asistente conversacional no influye significativamente en la experiencia de lectores de un diario digital en Huánuco, 2026.

Adicionalmente se formulan tres pares de hipótesis específicas, una por cada dimensión de la variable dependiente (usabilidad, tiempo de búsqueda y satisfacción).

**4. Stack tecnológico definitivo**

| **Capa** | **Tecnología** |
|----|----|
| **Frontend** | Next.js 15 + TypeScript + Tailwind + shadcn/ui + Framer Motion + next-pwa |
| **Gestor de paquetes frontend** | pnpm |
| **Backend** | Python 3.10+ con FastAPI + Pydantic v2 + pydantic-settings |
| **ORM** | SQLAlchemy + Alembic (migraciones) |
| **BD desarrollo local** | PostgreSQL 16 + pgvector en Docker (pgvector/pgvector:pg16) |
| **BD producción** | Supabase (PostgreSQL + pgvector) |
| **Autenticación** | Supabase Auth (roles admin y participante) |
| **IA - Embeddings** | OpenAI text-embedding-3-small |
| **IA - Generación** | OpenAI gpt-4o-mini (alternativa: Gemini Flash) |
| **Despliegue frontend** | Vercel |
| **Despliegue backend** | Render o Railway |
| **Versionado** | GitHub - 2 repositorios privados separados |
| **Arquitectura** | Clean Architecture + SOLID + Repository Pattern |

**Repositorios**

> **•** Backend: tudiariohuanuco-api
>
> **•** Frontend: tudiariohuanuco-web
>
> **•** Ambos son privados durante el desarrollo de la tesis.

**5. Estrategia de extracción de notas desde WordPress**

La extracción de notas desde el sitio WordPress del diario hacia la base de datos del proyecto se realiza en tres niveles progresivos. Los dos primeros niveles son obligatorios para el funcionamiento del sistema, mientras que el tercer nivel es opcional y queda como mejora post-tesis.

**5.1. Nivel 1: Sincronización inicial completa**

**Cuándo:** una sola vez al inicio del Sprint 4, después de tener la base de datos lista.

**Cómo funciona:** el backend FastAPI expone un endpoint protegido /admin/sync/full que el investigador ejecuta manualmente desde una herramienta como Thunder Client o curl. El endpoint llama a la REST API pública de WordPress en https://tudiariohuanuco.pe/wp-json/wp/v2/posts, recorre todas las notas históricas con paginación de 100 elementos por página, y por cada lote genera embeddings vectoriales mediante una sola llamada a OpenAI aprovechando el batching. Finalmente guarda en PostgreSQL título, contenido, fecha, autor, categoría, URL, imagen destacada y embedding.

**Tiempo estimado:** entre 10 y 15 minutos para 2,000 notas históricas.

**Costo estimado:** aproximadamente 0.03 USD.

**Idempotencia:** la operación es idempotente, lo que significa que ejecutarla dos veces no duplica registros gracias a la cláusula INSERT ON CONFLICT (wordpress_id) UPDATE de PostgreSQL.

**5.2. Nivel 2: Sincronización incremental continua**

**Cuándo:** desde el Sprint 4 en adelante, cada 15 minutos de manera automática.

**Cómo funciona:** un cron job configurado en Render ejecuta el endpoint /admin/sync/incremental cada 15 minutos. El endpoint consulta WordPress por notas modificadas o creadas desde la última sincronización exitosa registrada en la tabla sync_log, utilizando los parámetros after y modified_after de la REST API. Solo procesa las notas nuevas o actualizadas, lo que típicamente representa entre cero y cinco notas por ciclo. Actualiza la base de datos con los cambios y registra el resultado en sync_log.

**Ventaja:** la base de datos siempre está actualizada con un retraso máximo de 15 minutos respecto al sitio público.

**5.3. Nivel 3: Webhooks en tiempo real (opcional)**

**Cuándo:** solo si sobra tiempo después del Sprint 8, o como mejora post-tesis.

**Cómo funciona:** requiere instalar el plugin WP Webhooks en WordPress y configurarlo para que envíe una petición POST al endpoint /admin/sync/webhook del backend cuando se publica o actualiza una nota. El endpoint recibe la nota y la indexa al instante.

**Decisión estratégica:** se deja para post-tesis. La sincronización incremental cada 15 minutos es suficiente para la fase de investigación.

**6. Las cuatro fases del proyecto**

**Fase 1: Cimientos (Semanas 1 a 4)**

**Objetivo:** tener la infraestructura completa lista, vacía pero funcional.

**Resultado esperado:** frontend desplegado en Vercel, backend desplegado en Render, base de datos lista con esquema, autenticación operativa y sincronización de notas funcionando. Todavía no existe el chatbot conversacional.

**Fase 2: Núcleo RAG (Semanas 5 a 8)**

**Objetivo:** construir el corazón técnico de la tesis, que es el chatbot que responde con noticias reales.

**Resultado esperado:** endpoint /chat funcional que recibe una pregunta, ejecuta búsqueda semántica vectorial, genera una respuesta contextualizada con OpenAI y registra toda la conversación. El sistema es probable únicamente desde Thunder Client, sin frontend bonito aún.

**Fase 3: Frontend y experiencia (Semanas 9 a 12)**

**Objetivo:** construir la cara visible del producto con estética periodística elegante.

**Resultado esperado:** aplicación web instalable como PWA, con interfaz minimalista tipo The New York Times, chatbot integrado visualmente y botón puente desde el sitio principal de WordPress hacia el subdominio.

**Fase 4: Dashboard, recolección y cierre (Semanas 13 a 24)**

**Objetivo:** construir el dashboard de investigación, aplicar instrumentos, analizar datos y redactar los capítulos finales.

**Resultado esperado:** tesis defendida exitosamente.

**7. Detalle de los 13 sprints**

Cada sprint tiene una duración de dos semanas e incluye entregables verificables. Esta es la estructura que se debe configurar como listas en ClickUp.

**Fase 1: Cimientos**

**Sprint 1 (Semanas 1-2): Setup y walking skeleton**

> **•** Verificación de herramientas (Node.js, Python, Docker, Git).
>
> **•** Creación de cuentas (GitHub, Supabase, Vercel, Render, OpenAI).
>
> **•** Dos repositorios privados creados en GitHub.
>
> **•** Estructura SOLID base del backend implementada.
>
> **•** Estructura del frontend Next.js inicializada.
>
> **•** Endpoint /health del backend funcional.
>
> **•** Conexión frontend-backend en local verificada.
>
> **•** Despliegue inicial a Vercel y Render.

***Entregable:*** stack desplegado end-to-end con respuesta de tipo Hello World.

**Sprint 2 (Semanas 3-4): Base de datos y esquema**

> **•** Actualización del Docker local a la imagen pgvector/pgvector:pg16.
>
> **•** Activación de pgvector en Supabase.
>
> **•** Configuración de SQLAlchemy y Alembic.
>
> **•** Creación de las 14 tablas mediante migraciones.
>
> **•** Seed inicial de categorías y tareas estandarizadas.
>
> **•** Conexión de pgAdmin a Supabase y a la base local.

***Entregable:*** base de datos lista con esquema completo en local y Supabase.

**Sprint 3 (Semanas 5-6): Autenticación y roles**

> **•** Integración de Supabase Auth en backend y frontend.
>
> **•** Implementación de rol admin y rol participante.
>
> **•** Middleware de protección de rutas.
>
> **•** Páginas de registro y login en el frontend.
>
> **•** Modal de consentimiento informado.

***Entregable:*** sistema de autenticación completo con dos roles funcionales.

**Sprint 4 (Semanas 7-8): Ingestión desde WordPress**

> **•** Cliente HTTP para la REST API de WordPress.
>
> **•** Endpoint /admin/sync/full (manual).
>
> **•** Endpoint /admin/sync/incremental (cron job cada 15 min).
>
> **•** Generación de embeddings por lotes con OpenAI.
>
> **•** Registro de operaciones en la tabla sync_log.

***Entregable:*** base de datos poblada con todas las notas del diario y sincronización automática activa.

**Fase 2: Núcleo RAG**

**Sprint 5 (Semanas 9-10): Búsqueda semántica**

> **•** Endpoint /search con similitud coseno usando pgvector.
>
> **•** Tuning del parámetro k (cantidad de notas devueltas).
>
> **•** Umbral de relevancia configurable.
>
> **•** Filtros opcionales por categoría y fecha.

***Entregable:*** búsqueda vectorial funcional, probable desde Thunder Client.

**Sprint 6 (Semanas 11-12): Generación con LLM**

> **•** Endpoint /chat con prompting de RAG.
>
> **•** Prompt de sistema optimizado para periodismo regional.
>
> **•** Respuesta estructurada con cards (título, resumen, link).
>
> **•** Registro de cada interacción en la tabla conversaciones.

***Entregable:*** chatbot completamente funcional vía API.

**Sprint 7 (Semanas 13-14): Calidad y métricas**

> **•** Sistema de feedback (pulgar arriba/abajo).
>
> **•** Rate limiting por usuario e IP para prevenir abuso.
>
> **•** Logging estructurado de errores.
>
> **•** Endpoints para métricas básicas.

***Entregable:*** sistema robusto contra abuso y con métricas registradas.

**Sprint 8 (Semanas 15-16): Optimización del RAG**

> **•** Caché de respuestas frecuentes para reducir costos.
>
> **•** Chunking de notas largas para mejor recuperación.
>
> **•** Reranking de resultados de búsqueda.
>
> **•** Ajuste fino del prompt del sistema.
>
> **•** Pruebas con preguntas reales del dominio periodístico.

***Entregable:*** RAG pulido, rápido y económico.

**Fase 3: Frontend y experiencia**

**Sprint 9 (Semanas 17-18): UI base del subdominio**

> **•** Layout periodístico elegante con tipografía serif.
>
> **•** Header, footer y sistema de navegación.
>
> **•** Grilla de noticias con categorías.
>
> **•** Vista de noticia individual con lectura cómoda.

***Entregable:*** layout editorial completo y responsivo.

**Sprint 10 (Semanas 19-20): Componente conversacional**

> **•** Hero con caja de pregunta protagonista.
>
> **•** Chips de sugerencias clickeables.
>
> **•** Render de cards de respuesta del chatbot.
>
> **•** Historial de conversación.

***Entregable:*** chatbot integrado visualmente en la interfaz.

**Sprint 11 (Semanas 21-22): PWA y animaciones**

> **•** Configuración de manifest y service worker.
>
> **•** App instalable en dispositivos móviles.
>
> **•** Framer Motion para micro-interacciones.
>
> **•** Responsive móvil completo.

***Entregable:*** PWA pulida e instalable desde el navegador.

**Sprint 12 (Semanas 23-24): Botón puente en WordPress**

> **•** Snippet o plugin de WordPress para el botón flotante.
>
> **•** Banner discreto en la página principal del diario.
>
> **•** Redirección elegante al subdominio.

***Entregable:*** WordPress integrado con la nueva aplicación web.

**Fase 4: Dashboard y cierre**

**Sprint 13 (Semanas 25-26): Dashboard admin**

> **•** Ruta /admin protegida por rol.
>
> **•** Métricas SUS pretest vs postest.
>
> **•** Métricas de tiempos de búsqueda.
>
> **•** Tabla de participantes y su progreso.
>
> **•** Exportador CSV/Excel para análisis estadístico.

***Entregable:*** dashboard de investigación listo para la fase de recolección.

**Semanas 27-30: Recolección de datos**

> **•** Captación de participantes.
>
> **•** Aplicación del pretest.
>
> **•** Intervención (uso del sistema durante una semana).
>
> **•** Aplicación del postest.

**Semanas 31-32: Análisis y redacción final**

> **•** Análisis estadístico (t-Student o Wilcoxon).
>
> **•** Redacción de los Capítulos III, IV y V de la tesis.
>
> **•** Pre-sustentación con asesores.
>
> **•** Ajustes finales y defensa pública.

**8. Plan de configuración de ClickUp**

Para mantener el control del proyecto se utilizará ClickUp como herramienta de gestión. La estructura propuesta permite gestionar tanto el desarrollo técnico como el avance académico y la recolección de datos.

**8.1. Workspace principal**

**Nombre:** Tesis Tu Diario Huánuco.

**8.2. Spaces (espacios) recomendados**

**Space 1: Tesis Académica**

Engloba todo lo relacionado con la redacción de la tesis, asesorías, trámites institucionales y entregables académicos. Listas internas:

> **•** Capítulos (Cap I, II, III, IV, V con sus subtareas).
>
> **•** Anexos (tareas estandarizadas, consentimiento, autorizaciones).
>
> **•** Asesorías (reuniones, observaciones, correcciones por sprint).
>
> **•** Trámites UDH (designación de jurado, aprobaciones, formularios).

**Space 2: Desarrollo Software**

Engloba todo lo técnico del desarrollo del sistema. Listas internas:

> **•** Una lista por cada sprint (Sprint 1, Sprint 2, ..., Sprint 13).
>
> **•** Backlog técnico (cosas que surgen y no entran ahora, pero conviene anotar).
>
> **•** Bugs y errores (lo que necesita arreglo).
>
> **•** Refactors pendientes (mejoras de código sin urgencia).

**Space 3: Recolección y Análisis**

Engloba la fase final de aplicación de instrumentos y análisis estadístico. Listas internas:

> **•** Captación de participantes.
>
> **•** Aplicación pretest.
>
> **•** Aplicación postest.
>
> **•** Análisis estadístico.
>
> **•** Procesamiento de datos.

**8.3. Tags útiles transversales**

> **•** Crítico: para tareas que bloquean el avance.
>
> **•** Importante: prioridad alta pero no bloqueante.
>
> **•** Mejora: opcionales y agregables.
>
> **•** Bloqueado: esperando algo externo (asesor, diario, etc.).
>
> **•** Requiere asesor: necesita revisión académica antes de avanzar.
>
> **•** Bug: problema técnico identificado.

**8.4. Custom fields recomendados**

> **•** Sprint: dropdown con los 13 sprints planificados.
>
> **•** Fase: dropdown con las 4 fases (Cimientos, RAG, Frontend, Cierre).
>
> **•** Esfuerzo: tamaños S, M, L, XL.
>
> **•** Estado: Backlog, En progreso, En revisión, Terminado, Bloqueado.
>
> **•** Vinculado a tesis: sí/no (para saber qué afecta el documento académico).
>
> **•** Sesión con asesor: fecha de próxima validación si aplica.

**8.5. Vistas recomendadas**

**Vista 1: Sprint actual (Board)**

Tablero Kanban filtrado por el sprint en curso, agrupado por estado. Permite ver de un vistazo qué está pendiente, en progreso, en revisión y terminado.

**Vista 2: Cronograma general (Timeline)**

Vista de línea de tiempo con todos los sprints distribuidos en las 24 semanas. Útil para mostrar al asesor el plan macro y verificar si se está avanzando al ritmo previsto.

**Vista 3: Bloqueados (List filtrada)**

Lista de todas las tareas con estado Bloqueado o tag Requiere asesor. Permite identificar rápidamente lo que está esperando algo externo.

**Vista 4: Mi día (Lista filtrada por hoy)**

Lista de tareas asignadas con fecha de vencimiento hoy o vencidas. Es la vista que se usa al iniciar cada jornada de trabajo.

**9. Principios rectores del proyecto**

**9.1. Principios técnicos**

> **•** Aplicación de SOLID y Clean Architecture en todo el código del backend.
>
> **•** Idempotencia en todas las operaciones de sincronización con WordPress.
>
> **•** Batching en llamadas a APIs externas, especialmente OpenAI, para optimizar costos.
>
> **•** Repository Pattern para abstraer el acceso a datos y permitir migraciones futuras.
>
> **•** Versionado de API mediante prefijo /api/v1/ desde el inicio.
>
> **•** Operaciones async/await para todo I/O.
>
> **•** Variables de entorno para todo lo configurable.

**9.2. Principios estratégicos**

> **•** No over-engineering: entregar funcional siempre prima sobre perfeccionar.
>
> **•** Tier gratuito mientras dure: no pagar servicios hasta tener evidencia clara de necesidad.
>
> **•** Migrabilidad: código portable por si algún día se migra de proveedor.
>
> **•** Documentación viva: mantener actualizado el CLAUDE.md y resúmenes.
>
> **•** Validación frecuente con asesor para evitar retrabajos masivos.

**9.3. Principios académicos**

> **•** Formato APA séptima edición en toda la redacción.
>
> **•** Trazabilidad entre tesis y código: cada funcionalidad responde a un objetivo de la investigación.
>
> **•** Rigor estadístico en el análisis final.
>
> **•** Ética garantizada con consentimiento informado y privacidad de datos personales.

**10. Plan de contingencia con Supabase**

Aunque el tier gratuito de Supabase es suficiente para toda la fase de tesis, se establece un plan de acción claro para los escenarios futuros donde se supere ese tier.

| **Escenario** | **Acción** | **Costo mensual** |
|----|----|----|
| Durante la tesis (5% probabilidad) | Pagar Pro temporalmente solo si es estrictamente necesario | \$25 USD |
| Boom moderado post-tesis | Mantener Pro y monetizar el producto con publicidad o suscripciones | \$25 USD |
| Boom grande sostenido | Evaluar migración planificada a infraestructura propia o plan Team | Variable |
| Mega-boom (más de un año) | VPS propio con Docker y stack equivalente auto-hospedado | \$30-50 USD |

El principio rector de este plan es evitar el over-engineering: construir código portable desde el inicio (PostgreSQL estándar, capa de auth abstraída con interfaces) permite que cualquier migración futura, si llega a ser necesaria, tome solo aproximadamente una semana de trabajo.

**11. Estado actual del proyecto**

A la fecha de elaboración de este documento, el proyecto se encuentra en el Sprint 1, con aproximadamente 60-70% de avance.

**11.1. Avances completados**

> **•** Herramientas de desarrollo instaladas (Node, Python, Docker, Git, pnpm).
>
> **•** Cuentas creadas en GitHub, Supabase, Vercel, Render y OpenAI.
>
> **•** Repositorios privados creados en GitHub.
>
> **•** Estructura SOLID del backend implementada.
>
> **•** Código base del chat con OpenAI escrito.
>
> **•** Frontend Next.js con interfaz de chat creado.
>
> **•** Capítulos I y II de la tesis redactados en formato APA 7.
>
> **•** Anexos de tareas estandarizadas y consentimiento informado producidos.

**11.2. Pendientes inmediatos del Sprint 1**

> **•** Resolver el error ModuleNotFoundError mediante la creación de archivos \_\_init\_\_.py faltantes.
>
> **•** Verificar que el backend levanta correctamente con uvicorn.
>
> **•** Probar la comunicación end-to-end frontend-backend con respuesta de OpenAI.
>
> **•** Desplegar el backend en Render.
>
> **•** Desplegar el frontend en Vercel.
>
> **•** Cierre formal del Sprint 1.

**11.3. Pendientes académicos**

> **•** Capítulo III: Metodología.
>
> **•** Capítulo IV: Resultados.
>
> **•** Capítulo V: Discusión y conclusiones.
>
> **•** Autorización formal escrita del diario.
>
> **•** Completar datos del consentimiento informado con nombre del investigador y asesor.

**12. Conclusión y siguiente paso**

Este documento consolida todas las decisiones técnicas, metodológicas y de gestión tomadas para el desarrollo del proyecto de tesis. Funciona como referencia maestra a la que se puede recurrir en cualquier momento para retomar el contexto del proyecto.

El siguiente paso inmediato consiste en cerrar el Sprint 1 mediante la resolución del error técnico del backend y el despliegue de ambos componentes a sus plataformas de producción (Vercel y Render). Una vez completado el Sprint 1, se puede proceder con confianza al Sprint 2, que aborda la configuración completa de la base de datos con las 14 tablas planificadas, las migraciones con Alembic y la activación de pgvector tanto en el entorno local como en Supabase.

La configuración de ClickUp según la estructura descrita en este documento permitirá mantener la disciplina de avance constante mediante sprints quincenales con entregables verificables, garantizando que el cronograma de seis meses se cumpla y que la tesis se defienda exitosamente.

*Fin del documento*
