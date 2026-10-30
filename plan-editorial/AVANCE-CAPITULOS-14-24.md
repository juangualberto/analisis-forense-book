# Avance capítulos 14–24

**Actualizado:** 2026-10-30 (Europe/Madrid)  
**Rama:** `devel-recorte`  
**Modelo de estilo:** `manuscrito/13-Analisis-forense-de-redes.md`  
**Índice autoridad:** `plan-editorial/INDICE-v1.md`

## Extensión objetivo

| Referencia | Palabras |
|---|---|
| Cap. 10 | 14 036 |
| Cap. 11 | 13 827 |
| Cap. 12 | 14 213 |
| Cap. 13 | 16 135 |
| Media 10–12 (sin outlier 13) | ≈ 14 025 |
| Media 10–13 | ≈ 14 553 |

- Objetivo editorial del encargo: **60–70 %** de la referencia, orientación **10 000–13 000** palabras (la media recortada 10–13 es ~14,5k; el 65 % daría ~9,5k, pero el encargo pide no bajar del rigor y cita 10–13k).
- **Meta operativa por capítulo:** **≈ 11 000 palabras** (rango aceptable **10 000–12 500**), ajustable al alza en 17, 18, 19 y 24.

## Figuras

- Convención Markdown: `![Título](../figuras/figuraN.M.png)`
- Destino: `figuras/figuraN.M.png` (no tocar figuras ≤13)
- Estética: fondo claro, español, legible en impresión; referencia visual caps. 12–13 (~1448–1536 px; nuevas preferible ≥2000 px de ancho)
- `build.sh` usa `--resource-path=".:manuscrito:anexos:figuras:aux"`

## Estado por capítulo

| Cap | Archivo | Redacción | Figuras | 2ª revisión | Refs | Pandoc | Notas |
|---|---|---|---|---|---|---|---|
| 14 | `14-Navegadores-correo-y-aplicaciones.md` | en curso | pendiente | pendiente | pendiente | pendiente | Stub vacío (0 palabras) |
| 15 | `15-Datos-borrados-cifrado-y-antiforense.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 16 | `16-Sistemas-comprometidos-y-malware.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 17 | `17-Analisis-forense-de-Android.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 18 | `18-Analisis-forense-de-iOS.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 19 | `19-Analisis-forense-en-la-nube.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 20 | `20-Virtualizacion-y-contenedores.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 21 | `21-Analisis-forense-de-IoT.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 22 | `22-Interpretacion-de-evidencias.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 23 | `23-Informes-forenses.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |
| 24 | `24-Investigaciones-completas.md` | pendiente | pendiente | pendiente | pendiente | pendiente | Stub vacío |

## Compilación

- Script: `./build.sh` → `dist/AnalisisForense.pdf`
- Estado global: pendiente hasta completar 14–24 (y pruebas intermedias)

## Incidencias

- Cursor Cloud Agent: GitHub no conectado al lanzar el encargo; se solicitó conexión. Mientras tanto el trabajo se hace sobre el árbol local en `/home/juna/git/analisis-forense` (rama `devel-recorte`, 1 commit local respecto a tracking remoto según `rev-list`).
- No modificar capítulos 00–13 salvo fallo de compilación.

## Siguiente acción concreta

1. Redactar capítulo 14 según índice (6 epígrafes).
2. Generar e integrar figuras 14.1–14.N.
3. Segunda revisión técnica + URLs.
4. Validar Pandoc del capítulo e integrar en el árbol.
5. Actualizar esta tabla y pasar al 15.
