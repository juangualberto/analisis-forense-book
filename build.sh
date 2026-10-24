
#!/usr/bin/env bash
set -euo pipefail

# ==========================================================
# ANÁLISIS FORENSE INFORMÁTICO
# Compilación del manuscrito con Pandoc y Eisvogel
# ==========================================================

# Trabajar siempre desde el directorio del script
cd "$(dirname "$0")"

TITULO="Análisis Forense Informático"
SALIDA="AnalisisForense"
DESTINO="dist"
AUX="aux"
PORTADA="./plan-editorial/00-Portada.md"

mkdir -p "$DESTINO"

# ----------------------------------------------------------
# 1. Comprobar dependencias
# ----------------------------------------------------------

for programa in pandoc xelatex; do
    if ! command -v "$programa" >/dev/null 2>&1; then
        echo "ERROR: No se encuentra $programa"
        exit 1
    fi
done

# Localizar plantilla Eisvogel
if [[ -f "$AUX/eisvogel.latex" ]]; then
    PLANTILLA="$AUX/eisvogel.latex"
elif [[ -f "$AUX/eisvogel.tex" ]]; then
    PLANTILLA="$AUX/eisvogel.tex"
else
    echo "ERROR: No se encuentra Eisvogel en $AUX/"
    echo "Se esperaba eisvogel.latex o eisvogel.tex"
    exit 1
fi

# ----------------------------------------------------------
# 2. Ordenar manuscrito
# ----------------------------------------------------------

shopt -s nullglob

MANUSCRITO=(
    manuscrito/[0-9][0-9]-*.md
)

if (( ${#MANUSCRITO[@]} == 0 )); then
    echo "ERROR: No hay capítulos en manuscrito/"
    exit 1
fi

# Orden explícito de anexos
ANEXOS=(
    "anexos/A-Listas-de-comprobacion.md"
    "anexos/B-Plantillas-forenses.md"
    "anexos/C-Herramientas-y-recursos.md"
    "anexos/D-Guia-de-laboratorios.md"
    "anexos/Glosario.md"
    "anexos/Bibliografia.md"
)

# Añadir anexos existentes que no estén vacíos
for archivo in "${ANEXOS[@]}"; do
    if [[ -s "$archivo" ]]; then
        MANUSCRITO+=("$archivo")
    fi
done

echo "========================================"
echo " ANÁLISIS FORENSE INFORMÁTICO"
echo "========================================"
echo "Plantilla: $PLANTILLA"
echo "Archivos incluidos: ${#MANUSCRITO[@]}"
echo

# ----------------------------------------------------------
# 3. Opciones comunes
# ----------------------------------------------------------

OPCIONES=(
    --from=markdown
    --standalone
    --toc
    --toc-depth=3
    --number-sections
    --metadata="title:$TITULO"
    --resource-path=".:manuscrito:anexos:figuras:aux"
)

# ----------------------------------------------------------
# 4. Compilar PDF con Eisvogel
# ----------------------------------------------------------

compilar_pdf() {

    echo "[PDF] Iniciando compilación..."

    pandoc "${PORTADA}" \
        "${MANUSCRITO[@]}" \
        "${OPCIONES[@]}" \
        --template="$PLANTILLA" \
        --pdf-engine=xelatex \
        -V lang=es-ES \
        -V colorlinks=false \
        -o "$DESTINO/$SALIDA.pdf"

#        --highlight-style=tango \
#        -V documentclass=book \
#        -V book=true \
#        -V classoption=openright \
#        -V papersize=custom \
#        -V geometry:paperwidth=6in \
#        -V geometry:paperheight=9in \
#        -V geometry:inner=0.85in \
#        -V geometry:outer=0.65in \
#        -V geometry:top=0.75in \
#        -V geometry:bottom=0.75in \
#        -V fontsize=11pt \


    echo "[OK] PDF generado: $DESTINO/$SALIDA.pdf"
}

# ----------------------------------------------------------
# 5. Compilar EPUB
# ----------------------------------------------------------

compilar_epub() {

    echo "[EPUB] Iniciando compilación..."

    pandoc "${MANUSCRITO[@]}" \
        "${OPCIONES[@]}" \
        --to=epub3 \
        --metadata="lang:es-ES" \
        --metadata="language:es-ES" \
        --split-level=1 \
        -o "$DESTINO/$SALIDA.epub"

    echo "[OK] EPUB generado: $DESTINO/$SALIDA.epub"
}

# ----------------------------------------------------------
# 6. Seleccionar formato
# ----------------------------------------------------------

case "${1:-all}" in
    pdf)
        compilar_pdf
        ;;
    epub)
        compilar_epub
        ;;
    all)
        compilar_pdf
        compilar_epub
        ;;
    *)
        echo "Uso: ./build.sh [pdf|epub|all]"
        exit 1
        ;;
esac

echo
echo "Compilación finalizada."
