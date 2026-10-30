# Avance de los capítulos 14 a 24

Registro de la redacción de la parte pendiente de *Análisis Forense Informático*. El PDF completo no se versiona: si `./build.sh pdf` produce un fichero grande, permanece fuera del commit.

## Decisiones

- Rama: `cursor/capitulos-14-24-ba84`, desde `main`.
- `manuscrito/13-Analisis-forense-de-redes.md` está vacío, igual que los capítulos 11 y 12. No se ha modificado. La voz se toma de los capítulos 8, 9 y 10: epígrafes numerados, distinción entre observación, inferencia e hipótesis, caso ficticio y referencias con URL.
- Los capítulos 00 a 13 no se reescriben. La única excepción de compilación es `figuras/figura10.6.png`: el capítulo 10 ya la citaba y el fichero no estaba en el repositorio. Sin ella, Pandoc detiene el libro. El markdown del capítulo 10 no se ha tocado.
- Figuras nuevas generadas con Pillow en `figuras/generar_14_24.py`.

## Estado

Recuento con `wc -w` al cierre de la revisión. Intervalo pedido: 10 500–12 500.

| Cap. | Palabras | Figuras | URLs | Pandoc del conjunto |
| --- | ---: | ---: | --- | --- |
| 14. Navegadores, correo y aplicaciones | 11741 | 6 | lista blanca | en la compilación del libro |
| 15. Datos borrados, cifrado y antiforense | 12463 | 6 | lista blanca | en la compilación del libro |
| 16. Sistemas comprometidos y malware | 12309 | 6 | lista blanca; QEMU en `/docs/master/system/images.html` | en la compilación del libro |
| 17. Android | 11975 | 6 | lista blanca | en la compilación del libro |
| 18. iOS y iPadOS | 11711 | 6 | lista blanca | capítulo suelto compilado antes; el libro, con el resto |
| 19. Nube | 11048 | 7 | lista blanca | en la compilación del libro |
| 20. Virtualización y contenedores | 12235 | 6 | lista blanca; misma corrección de QEMU | en la compilación del libro |
| 21. IoT | 12367 | 7 | lista blanca | en la compilación del libro |
| 22. Interpretación | 12462 | 6 | lista blanca | en la compilación del libro |
| 23. Informes | 12284 | 6 | lista blanca | en la compilación del libro |
| 24. Investigaciones completas | 11795 | 6 | lista blanca | en la compilación del libro |

## Revisión

- Epígrafes de nivel 2 alineados con `plan-editorial/INDICE-v1.md`.
- Cada figura citada existe. Los dominios `.example` del cuerpo son del caso ficticio.
- La lista blanca de URL se comprobó con HTTP. `https://www.qemu.org/docs/` responde 404; la cita usada es `https://www.qemu.org/docs/master/system/images.html`. `https://www.iso.org` rechaza el cliente automático con 403 y se mantiene porque es el portal oficial ya usado en la bibliografía del libro.
- NIST IR 8006 figura como publicado en agosto de 2020 en la ficha del CSRC, con 62 retos en nueve categorías. NIST SP 800-201 es de julio de 2024.
- No se describen procedimientos de explotación, de borrado operativo, de ocultación ni de elusión de cifrado. El capítulo 18 dice expresamente que un método publicado para un chip antiguo no se traslada ni se convierte en procedimiento.
- Segunda lectura: se recortaron repeticiones de los capítulos que superaban 12 500 palabras. Se corrigió la URL de QEMU después de que una pasada posterior la hubiera devuelto a la ruta inexistente.

## Compilación

`build.sh` usa Pandoc y Eisvogel. En este entorno hubo que instalar Pandoc, XeLaTeX y `texlive-fonts-extra` (la plantilla carga `sourcesanspro`). `./build.sh pdf` terminó con código 0. El PDF resultante mide 104 168 521 bytes (unos 99,3 MiB) y **no se incluye en el commit**: el encargo pide no versionar el PDF grande. El fichero que ya estaba en `main` se deja como estaba.

## Bitácora

### Inspección

Los capítulos 14 a 24 estaban vacíos. El índice, los criterios y los capítulos 8 a 10 fijaron la estructura y el tono.

### Cierre

Los once capítulos quedan escritos, ilustrados y dentro del intervalo de extensión. El caso del capítulo 24 es Litoral Media, S. L., independiente de los nombres de los capítulos 8 a 10. La filtración deliberada no se cierra; el envío autorizado mal documentado sigue abierto; el compromiso de credencial queda apoyado, sin modo de operar.
