#!/usr/bin/env python3
"""Figuras originales de los capítulos 14 a 24.

Diagramas didácticos generados con Pillow. No contienen datos de casos reales.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W = 1500
# Lienzo de trabajo alto; al final se recorta al contenido para no dejar
# bandas vacías que, al escalar el PNG al ancho de página, encogerían el texto.
H = 2200

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (246, 248, 252)
INK = (30, 41, 59)
MUTED = (71, 85, 105)
HAIR = (226, 232, 240)
WHITE = (255, 255, 255)

PALETTE = {
    "azul": ((239, 246, 255), (29, 78, 216)),
    "verde": ((240, 253, 244), (21, 128, 61)),
    "ambar": ((255, 247, 237), (194, 65, 12)),
    "rosa": ((255, 241, 242), (190, 18, 60)),
    "violeta": ((245, 243, 255), (109, 40, 217)),
    "teal": ((240, 253, 250), (15, 118, 110)),
    "cielo": ((240, 249, 255), (3, 105, 161)),
    "pizarra": ((248, 250, 252), (51, 65, 85)),
}


def F(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = word if not cur else f"{cur} {word}"
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def rounded(draw, box, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def shadow_card(draw, box, radius=18):
    x0, y0, x1, y1 = box
    rounded(draw, (x0 + 4, y0 + 5, x1 + 4, y1 + 5), radius, (226, 232, 240))


def arrow(draw, x0, y0, x1, y1, color=(100, 116, 139)):
    draw.line((x0, y0, x1, y1), fill=color, width=3)
    if abs(x1 - x0) >= abs(y1 - y0):
        sign = 1 if x1 >= x0 else -1
        tip = (x1, y1)
        draw.polygon(
            [(tip[0], tip[1]), (tip[0] - 12 * sign, tip[1] - 6), (tip[0] - 12 * sign, tip[1] + 6)],
            fill=color,
        )
    else:
        sign = 1 if y1 >= y0 else -1
        tip = (x1, y1)
        draw.polygon(
            [(tip[0], tip[1]), (tip[0] - 6, tip[1] - 12 * sign), (tip[0] + 6, tip[1] - 12 * sign)],
            fill=color,
        )


class Canvas:
    def __init__(self, title: str, subtitle: str, accent: str = "azul"):
        self.img = Image.new("RGB", (W, H), BG)
        self.d = ImageDraw.Draw(self.img)
        _, border = PALETTE[accent]
        self.d.rectangle((0, 0, W, 12), fill=border)
        self.d.text((36, 32), title, font=F(40, True), fill=INK)
        sub_lines = wrap(self.d, subtitle, F(22), W - 72)
        yy = 86
        for line in sub_lines[:2]:
            self.d.text((36, yy), line, font=F(22), fill=MUTED)
            yy += 30
        self.header_bottom = yy + 8
        self.warnings: list[str] = []

    def footer(self, note: str, legend: list[tuple[str, str]], top: int) -> int:
        y = top + 8
        self.d.line((36, y, W - 36, y), fill=HAIR, width=2)
        lines = wrap(self.d, note, F(20), W - 72)
        yy = y + 16
        for line in lines[:3]:
            self.d.text((36, yy), line, font=F(20), fill=MUTED)
            yy += 28
        lx = 36
        ly = yy + 12
        for name, key in legend:
            fill, border = PALETTE[key]
            self.d.rounded_rectangle((lx, ly, lx + 28, ly + 22), radius=5, fill=fill, outline=border, width=2)
            self.d.text((lx + 36, ly - 1), name, font=F(20), fill=INK)
            lx += 36 + int(self.d.textlength(name, font=F(20))) + 28
        return ly + 40

    def card(self, box, title, bullets, key="azul", badge=None):
        x, y, w, h = box
        fill, border = PALETTE[key]
        shadow_card(self.d, (x, y, x + w, y + h))
        rounded(self.d, (x, y, x + w, y + h), 16, fill, border, 2)
        self.d.rectangle((x, y, x + 10, y + h), fill=border)
        tx = x + 24
        self.d.text((tx, y + 16), title, font=F(26, True), fill=border)
        if badge:
            bw = int(self.d.textlength(badge, font=F(18, True))) + 18
            bx = x + w - bw - 14
            self.d.rounded_rectangle((bx, y + 16, bx + bw, y + 42), radius=8, fill=WHITE, outline=border, width=2)
            self.d.text((bx + 9, y + 18), badge, font=F(18, True), fill=border)
        yy = y + 58
        max_w = w - 48
        for bullet in bullets:
            parts = wrap(self.d, bullet, F(22), max_w - 18)
            for i, part in enumerate(parts):
                prefix = "• " if i == 0 else "  "
                if yy + 28 > y + h - 12:
                    self.warnings.append(f"overflow:{title}:{part}")
                    return
                self.d.text((tx, yy), prefix + part, font=F(22), fill=INK)
                yy += 30

    def band(self, box, title, body, key="pizarra"):
        x, y, w, h = box
        fill, border = PALETTE[key]
        rounded(self.d, (x, y, x + w, y + h), 16, fill, border, 3)
        self.d.text((x + 20, y + 14), title, font=F(26, True), fill=border)
        yy = y + 54
        for line in wrap(self.d, body, F(22), w - 40):
            if yy + 30 > y + h - 8:
                self.warnings.append(f"band:{title}:{line}")
                return
            self.d.text((x + 20, yy), line, font=F(22), fill=INK)
            yy += 30

    def save(self, name: str, bottom: int):
        cropped = self.img.crop((0, 0, W, min(H, bottom)))
        path = OUT / name
        cropped.save(path, format="PNG", optimize=True)
        return path


def row_layout(n, y, h, margin=32, gap=18):
    inner = W - 2 * margin - gap * (n - 1)
    w = inner // n
    boxes = []
    x = margin
    for _ in range(n):
        boxes.append((x, y, w, h))
        x += w + gap
    return boxes


def _card_height(draw, item, width):
    yy = 64
    max_w = width - 66
    for bullet in item["b"]:
        parts = wrap(draw, bullet, F(22), max_w - 18)
        yy += 30 * max(1, len(parts))
    return yy + 20


def flow(name, title, subtitle, items, note, legend, accent="azul", rows=0):
    c = Canvas(title, subtitle, accent)
    n = len(items)
    if rows <= 0:
        rows = 2 if n >= 4 else 1
    per = (n + rows - 1) // rows
    probe_w = (W - 64 - 18 * (per - 1)) // max(per, 1)
    idx = 0
    y = c.header_bottom + 8
    for _r in range(rows):
        chunk = items[idx : idx + per]
        idx += per
        if not chunk:
            break
        rh = max(_card_height(c.d, item, probe_w) for item in chunk)
        boxes = row_layout(len(chunk), y, rh)
        for i, ((x, yy, w, h), item) in enumerate(zip(boxes, chunk)):
            c.card((x, yy, w, h), item["t"], item["b"], item.get("k", "azul"), item.get("badge"))
            if rows == 1 and i < len(chunk) - 1 and item.get("arrow", True):
                x2 = boxes[i + 1][0]
                arrow(c.d, x + w + 2, yy + 34, x2 - 2, yy + 34)
        y += rh + 16
    bottom = c.footer(note, legend, y)
    path = c.save(name, bottom)
    if c.warnings:
        print(name, c.warnings)
    return path


def _band_height(draw, body, width):
    lines = wrap(draw, body, F(22), width - 40)
    return 54 + 30 * len(lines) + 16


def layers(name, title, subtitle, bands, note, legend, accent="azul"):
    c = Canvas(title, subtitle, accent)
    y = c.header_bottom + 8
    gap = 12
    width = W - 64
    for band in bands:
        h = _band_height(c.d, band["b"], width)
        c.band((32, y, width, h), band["t"], band["b"], band.get("k", "pizarra"))
        y += h + gap
    bottom = c.footer(note, legend, y)
    path = c.save(name, bottom)
    if c.warnings:
        print(name, c.warnings)
    return path


# ---------------------------------------------------------------------------
# Datos de las figuras. Textos cortos, comprobables y no operativos.
# ---------------------------------------------------------------------------

def build_all() -> None:
    flow(
        "figura14.1.png",
        "Artefactos habituales de un perfil de navegador",
        "La ruta y el esquema dependen de la versión, el canal, el sistema y el perfil",
        [
            {"t": "Chromium y derivados", "k": "azul", "b": [
                "Directorio de datos de usuario y subcarpeta de perfil, a menudo Default.",
                "History, Cookies, Login Data, Web Data y Bookmarks.",
                "Favicons y Top Sites acompañan al historial.",
                "La caché puede residir en otra ruta, sobre todo en macOS.",
            ]},
            {"t": "Firefox", "k": "ambar", "b": [
                "El perfil se localiza mediante profiles.ini.",
                "places.sqlite reúne historial y marcadores.",
                "cookies.sqlite y formhistory.sqlite son ficheros distintos.",
                "logins.json y key4.db no deben separarse si se conservan ambos.",
            ]},
            {"t": "Safari", "k": "teal", "b": [
                "History.db es la base habitual del historial en macOS.",
                "Descargas, cookies y pestañas cambian de nombre y de sitio.",
                "Los perfiles de Safari recientes multiplican los directorios.",
                "Una ruta de un artículo antiguo es solo una hipótesis de búsqueda.",
            ]},
            {"t": "Qué no asumir", "k": "rosa", "b": [
                "Un registro de visita no identifica a la persona.",
                "La sincronización puede crear historial en otro equipo.",
                "El modo privado reduce rastros; no promete ausencia total.",
                "Faltan WAL, SHM o journal: la copia puede estar incompleta.",
            ]},
        ],
        "Figura 14.1. Mapa de localización. Los nombres proceden de la documentación de Chromium y de la estructura conocida de Firefox y Safari; hay que verificarlos en la copia.",
        [("Perfil", "azul"), ("Bases", "ambar"), ("Límites", "rosa")],
        accent="azul",
    )

    flow(
        "figura14.2.png",
        "Cadena Received: el orden de lectura importa",
        "Cada sistema que retransmite el mensaje suele anteponer su propia cabecera Received",
        [
            {"t": "1. Cerca del cuerpo", "k": "pizarra", "badge": "más antigua", "b": [
                "Suele describir el primer salto aceptado por la infraestructura.",
                "Las líneas añadidas por el emisor, antes de ese salto, pueden ser falsas.",
                "No se lee como si fuera un acta de la máquina del autor.",
            ]},
            {"t": "2. Saltos intermedios", "k": "cielo", "b": [
                "Relacionan servidores, direcciones y horas de cada tramo.",
                "Hay que contrastar el nombre anunciado con la dirección y el DNS.",
                "Relojes desfasados explican horas que no encajan.",
            ]},
            {"t": "3. Cabecera superior", "k": "verde", "badge": "más reciente", "b": [
                "La añade, en general, el último sistema que recibió el mensaje.",
                "Es la más útil para saber qué servidor entregó el correo al buzón.",
                "Sigue siendo un registro de sistema, no una identificación civil.",
            ]},
            {"t": "Cabeceras declaradas", "k": "ambar", "b": [
                "From, Date, Message-ID y Reply-To las afirma el emisor.",
                "No heredan la confianza del último Received.",
                "Se conservan junto al mensaje original, sin reenviar el correo.",
            ]},
        ],
        "Figura 14.2. Lectura de la cadena Received. La confianza disminuye en los tramos que el emisor pudo escribir antes de entrar en un sistema controlado.",
        [("Declarado", "ambar"), ("Intermedio", "cielo"), ("Último salto", "verde")],
    )

    flow(
        "figura14.3.png",
        "SPF, DKIM y DMARC no responden a la misma pregunta",
        "Un resultado de autenticación no convierte el contenido en verdadero ni en fraudulento",
        [
            {"t": "SPF  ·  RFC 7208", "k": "azul", "b": [
                "Comprueba el servidor que envía el sobre SMTP.",
                "Usa MAIL FROM o HELO y la política DNS del dominio.",
                "No autentica, por sí solo, el encabezado From visible.",
                "Resultados: pass, fail, softfail, neutral, none y errores.",
            ]},
            {"t": "DKIM  ·  RFC 6376", "k": "verde", "b": [
                "Firma criptográfica de cabeceras seleccionadas y del cuerpo.",
                "El dominio firmante aparece en d=; la clave, en el selector.",
                "Un pass significa que lo firmado no cambió desde la firma.",
                "No identifica a la persona que redactó el texto.",
            ]},
            {"t": "DMARC  ·  RFC 7489", "k": "violeta", "b": [
                "Exige alineación de SPF o DKIM con el dominio del From.",
                "La política p= puede ser none, quarantine o reject.",
                "Los informes agregados no son la prueba del mensaje concreto.",
                "ARC puede explicar reenvíos; no anula el análisis del caso.",
            ]},
        ],
        "Figura 14.3. Tres controles complementarios. Se documenta el resultado observado, el dominio evaluado y qué parte del mensaje quedó cubierta.",
        [("Sobre SMTP", "azul"), ("Integridad firmada", "verde"), ("Alineación", "violeta")],
        accent="violeta",
    )

    flow(
        "figura14.4.png",
        "Examen de adjuntos, enlaces y metadatos",
        "Preservar el mensaje original antes de abrirlo o de seguir un enlace",
        [
            {"t": "Conservar", "k": "pizarra", "b": [
                "Copia íntegra del mensaje, con cabeceras y cuerpo MIME.",
                "Hash del contenedor y, después, de cada parte extraída.",
                "No se reenvía el correo para «ver qué pasa».",
            ]},
            {"t": "Describir", "k": "azul", "b": [
                "Content-Type, disposición, nombre y transferencia.",
                "El nombre visible puede no coincidir con el tipo real.",
                "Los metadatos de un documento tienen otro autor y otra hora.",
            ]},
            {"t": "Separar", "k": "ambar", "b": [
                "El enlace observado no es la página finalmente servida.",
                "Redirecciones y acortadores cambian el destino.",
                "Una resolución posterior no reproduce el estado del día del hecho.",
            ]},
            {"t": "Acotar", "k": "rosa", "b": [
                "El análisis de ficheros se hace en una copia y en un entorno aislado.",
                "Abrir el adjunto en el puesto de trabajo del analista contamina la escena.",
                "La peligrosidad no se deduce solo de la extensión.",
            ]},
        ],
        "Figura 14.4. Orden de trabajo. Cada paso produce una observación distinta: contenedor, parte MIME, metadato interno y comportamiento posterior.",
        [("Conservación", "pizarra"), ("Metadato", "ambar"), ("Aislamiento", "rosa")],
        accent="ambar",
    )

    flow(
        "figura14.5.png",
        "La mensajería no vive en un solo sitio",
        "Cliente, servidor y otros dispositivos pueden conservar historias distintas",
        [
            {"t": "Cliente local", "k": "azul", "b": [
                "Bases, cachés e índices de la aplicación instalada.",
                "Puede guardar borradores que nunca se enviaron.",
                "Una desinstalación no vacía necesariamente copias de seguridad.",
            ]},
            {"t": "Servidor o proveedor", "k": "verde", "b": [
                "Buzón, registros de entrega y retención del servicio.",
                "El acceso depende de la cuenta, el contrato y la jurisdicción.",
                "Lo que el usuario ve puede ser un subconjunto del registro.",
            ]},
            {"t": "Otros dispositivos", "k": "violeta", "b": [
                "Sincronización parcial, colas y mensajes ya borrados en un extremo.",
                "Una exportación «completa» debe decir de qué extremo lo es.",
                "La hora del cliente y la hora del servidor no son intercambiables.",
            ]},
        ],
        "Figura 14.5. Tres depósitos. La ausencia en uno de ellos no demuestra que el mensaje no existiera en otro.",
        [("Equipo", "azul"), ("Servicio", "verde"), ("Réplicas", "violeta")],
        accent="teal",
    )

    flow(
        "figura14.6.png",
        "Caso de laboratorio: de la cabecera a la hipótesis",
        "Escenario ficticio. Cada fila es una fuente, no una conclusión sobre la persona",
        [
            {"t": "Mensaje recibido", "k": "azul", "badge": "observado", "b": [
                "El buzón conserva el mensaje y la cadena Received.",
                "DMARC del dominio visible resulta alineado.",
                "Eso autentica un dominio, no el relato del cuerpo.",
            ]},
            {"t": "Clic y descarga", "k": "ambar", "badge": "correlación", "b": [
                "El historial muestra una visita posterior al enlace.",
                "La carpeta de descargas conserva un fichero con otro hash.",
                "La cercanía temporal no prueba que el clic causara la descarga.",
            ]},
            {"t": "Sesión de la cuenta", "k": "rosa", "badge": "pendiente", "b": [
                "Hay un inicio de sesión remoto en una hora compatible.",
                "Falta el registro del proveedor de identidad.",
                "Siguen abiertas la cuenta compartida y el reenvío automático.",
            ]},
        ],
        "Figura 14.6. Tres niveles del mismo caso ficticio: lo que está en la copia, lo que puede relacionarse y lo que todavía habría que pedir.",
        [("Observado", "azul"), ("Correlación", "ambar"), ("Pendiente", "rosa")],
        accent="rosa",
    )

    layers(
        "figura15.1.png",
        "Borrar un nombre no es borrar todas las representaciones",
        "Qué puede quedar después de una eliminación ordinaria",
        [
            {"t": "Vista del directorio", "k": "rosa", "b": "El nombre deja de aparecer en el listado activo. Esta es la observación más débil: solo describe la vista actual del sistema de archivos."},
            {"t": "Metadatos aún referenciados", "k": "ambar", "b": "Papelera, journal, instantáneas, índices de aplicación o copias de volumen pueden conservar nombre, ruta y marcas de tiempo."},
            {"t": "Contenido no asignado", "k": "azul", "b": "Los bloques pueden seguir en el medio hasta que se reutilicen. Su recuperación ya no aporta, por sí sola, la ruta original."},
            {"t": "Medios de estado sólido", "k": "violeta", "b": "TRIM y la nivelación de desgaste hacen incierto el momento en que el contenido deja de ser legible. No hay un plazo universal."},
            {"t": "Copias fuera del soporte", "k": "verde", "b": "Copias de seguridad, sincronización y otros equipos son fuentes distintas. Su existencia no se deduce del disco examinado."},
        ],
        "Figura 15.1. Capas de conservación. Cada una responde a una pregunta diferente y tiene su propia integridad.",
        [("Vista actual", "rosa"), ("Residuo", "azul"), ("Fuente externa", "verde")],
        accent="ambar",
    )

    flow(
        "figura15.2.png",
        "File carving: candidatos a contenido, no archivos originales",
        "La talla busca firmas; no restituye el directorio que ya no existe",
        [
            {"t": "Cabecera", "k": "azul", "b": [
                "Una firma conocida sugiere el inicio de un formato.",
                "La misma secuencia puede aparecer dentro de otro fichero.",
                "Por eso el hallazgo es un candidato, no una identificación cerrada.",
            ]},
            {"t": "Cuerpo contiguo", "k": "ambar", "b": [
                "Muchos talladores suponen que el contenido sigue en bloques seguidos.",
                "La fragmentación rompe esa suposición.",
                "Un fichero cortado puede abrirse solo en parte.",
            ]},
            {"t": "Pie o tamaño", "k": "verde", "b": [
                "Algunos formatos anuncian el final o la longitud.",
                "Si el pie se reutilizó, el recorte puede mezclar datos ajenos.",
                "Hay que validar el resultado con el formato, no solo con la firma.",
            ]},
            {"t": "Lo que no vuelve", "k": "rosa", "b": [
                "Nombre, ruta, propietario y permisos no viven en la firma.",
                "Las marcas de tiempo del sistema de archivos pueden haberse perdido.",
                "El informe debe llamar al producto «fragmento tallado», no «archivo del usuario».",
            ]},
        ],
        "Figura 15.2. Límites del carving. Una apertura correcta del fragmento demuestra estructura, no el contexto en el que existió.",
        [("Firma", "azul"), ("Validación", "verde"), ("Contexto perdido", "rosa")],
        accent="ambar",
    )

    layers(
        "figura15.3.png",
        "Capas de cifrado que no deben confundirse",
        "Una imagen fiel de bloques cifrados puede ser ilegible",
        [
            {"t": "Cifrado de volumen o de disco", "k": "azul", "b": "Protege el soporte en reposo. Sin la clave o sin el estado desbloqueado, la copia de sectores no revela documentos."},
            {"t": "Contenedor o fichero cifrado", "k": "violeta", "b": "Un archivo puede ser un volumen completo. Su presencia se observa; su contenido exige una clave distinta de la del disco."},
            {"t": "Cifrado de aplicación", "k": "ambar", "b": "Gestores de contraseñas, mensajería y copias de seguridad protegen registros concretos aunque el volumen esté abierto."},
            {"t": "Transporte", "k": "teal", "b": "TLS protege un canal. No cifra el disco ni garantiza que los extremos conservaran el contenido en claro."},
        ],
        "Figura 15.3. Cuatro capas. Documentar «está cifrado» sin decir cuál impide entender qué adquisición podría ser útil y cuál no.",
        [("Volumen", "azul"), ("Aplicación", "ambar"), ("Canal", "teal")],
        accent="violeta",
    )

    flow(
        "figura15.4.png",
        "Dónde contrasta el examinador una posible ocultación",
        "Mapa de búsqueda. No es un procedimiento para ocultar datos",
        [
            {"t": "Dentro del sistema de archivos", "k": "azul", "b": [
                "Flujos alternativos, holgura de archivo y espacio reservado.",
                "Nombres engañosos y extensiones que no coinciden con el tipo.",
                "Directorios que una vista ordinaria no muestra.",
            ]},
            {"t": "Fuera de la vista activa", "k": "ambar", "b": [
                "Espacio no asignado, particiones no montadas e instantáneas.",
                "Contenedores cifrados cuyo interior no se interpreta.",
                "Copias de volumen con estados anteriores.",
            ]},
            {"t": "En el contenido aparente", "k": "violeta", "b": [
                "Un fichero portador puede incluir datos añadidos.",
                "Una anomalía estadística no demuestra un mensaje oculto.",
                "Hace falta una hipótesis y una validación; no basta un indicador.",
            ]},
            {"t": "Límite de la conclusión", "k": "rosa", "b": [
                "No encontrar datos ocultos no prueba que no se intentara.",
                "Encontrar un contenedor no prueba que se usara para el hecho.",
                "Se informa del alcance de la búsqueda realizada.",
            ]},
        ],
        "Figura 15.4. Lugares de contraste. La figura delimita la búsqueda legítima y lo que cada hallazgo no autoriza a afirmar.",
        [("Sistema de archivos", "azul"), ("Fuera de la vista", "ambar"), ("Límite", "rosa")],
        accent="rosa",
    )

    flow(
        "figura15.5.png",
        "Marcas temporales: varias horas para un solo fichero",
        "Una discrepancia es un hecho. La manipulación es una hipótesis que hay que contrastar",
        [
            {"t": "Sistema de archivos", "k": "azul", "b": [
                "Creación, modificación, acceso y cambio de metadatos no significan lo mismo.",
                "En NTFS, $STANDARD_INFORMATION y $FILE_NAME pueden divergir.",
                "La copia y la sincronización también las alteran.",
            ]},
            {"t": "Aplicación y documento", "k": "ambar", "b": [
                "El interior de un oficio puede guardar otra hora y otro autor.",
                "Esa hora describe el documento, no el instante de copia al disco.",
                "Zona horaria y reloj del equipo se documentan aparte.",
            ]},
            {"t": "Registros externos", "k": "verde", "b": [
                "Un evento de correo, de proxy o de copia de seguridad es independiente.",
                "Sirve para contrastar, no para sustituir, la marca local.",
                "Si los relojes no estaban sincronizados, la diferencia se explica.",
            ]},
        ],
        "Figura 15.5. Tres relojes. Antes de hablar de manipulación se anotan la fuente, la resolución, la zona horaria y una causa ordinaria compatible.",
        [("Volumen", "azul"), ("Documento", "ambar"), ("Fuente externa", "verde")],
    )

    flow(
        "figura15.6.png",
        "Detección y límite de las técnicas antiforenses",
        "Nombre del fenómeno, rastro posible y lo que no queda demostrado",
        [
            {"t": "Borrado y desgaste", "k": "ambar", "b": [
                "Rastro posible: ausencia, journal, instantánea o talla.",
                "No queda demostrado el motivo ni la persona.",
                "En SSD, la ausencia de talla no fecha el borrado.",
            ]},
            {"t": "Cifrado y contenedores", "k": "violeta", "b": [
                "Rastro posible: fichero opaco, cabecera o volumen bloqueado.",
                "No queda demostrado el contenido ni el uso.",
                "No existe una vía general para leer cualquier cifrado actual.",
            ]},
            {"t": "Relojes alterados", "k": "azul", "b": [
                "Rastro posible: marcas incoherentes entre fuentes.",
                "No queda demostrada la intención solo con la incoherencia.",
                "Hay que excluir copia, zona horaria y reloj mal configurado.",
            ]},
            {"t": "Huellas del propio análisis", "k": "rosa", "b": [
                "Rastro posible: montajes, vistas previas y horas de acceso nuevas.",
                "Se separan del hecho investigado.",
                "Trabajar sobre copias reduce este ruido.",
            ]},
        ],
        "Figura 15.6. Matriz de límite. La detección orienta la búsqueda; la atribución exige fuentes independientes.",
        [("Fenómeno", "ambar"), ("Contraste", "azul"), ("Ruido del análisis", "rosa")],
        accent="ambar",
    )

    flow(
        "figura16.1.png",
        "Indicadores: de lo concreto y frágil a lo contextual",
        "Un indicador orienta la búsqueda. No sustituye la evidencia del caso",
        [
            {"t": "Hash y tamaño", "k": "rosa", "badge": "frágil", "b": [
                "Identifica un contenido exacto ya conocido.",
                "Cambia con una modificación mínima.",
                "No explica qué hizo el programa en este equipo.",
            ]},
            {"t": "Nombres de red", "k": "ambar", "b": [
                "Direcciones, dominios y URL observados o consultados.",
                "Pueden ser compartidos, reutilizados o caducados.",
                "Una resolución actual no reproduce la del día del hecho.",
            ]},
            {"t": "Rutas y persistencia", "k": "azul", "b": [
                "Claves, servicios, tareas o ficheros de arranque.",
                "La configuración puede existir sin haberse ejecutado.",
                "También la crea software legítimo.",
            ]},
            {"t": "Comportamiento", "k": "verde", "badge": "contextual", "b": [
                "Secuencia de proceso, línea de órdenes y red.",
                "Resiste mejor un cambio de hash.",
                "Exige más interpretación y más falsos positivos si se usa solo.",
            ]},
        ],
        "Figura 16.1. Tipos de indicador y su alcance. La pirámide de especificidad no es una escala de culpabilidad.",
        [("Contenido", "rosa"), ("Configuración", "azul"), ("Conducta", "verde")],
        accent="rosa",
    )

    flow(
        "figura16.2.png",
        "Persistencia observable, sin confundirla con la ejecución",
        "Tres sistemas, una misma pregunta: ¿está preparado, habilitado y llegó a correr?",
        [
            {"t": "Windows", "k": "azul", "b": [
                "Servicios, tareas, claves de ejecución y suscripciones.",
                "El evento de creación de proceso es otra fuente.",
                "Una clave Run no demuestra que el programa hiciera algo.",
            ]},
            {"t": "Linux", "k": "ambar", "b": [
                "Unidades systemd, temporizadores, cron y claves SSH.",
                "Habilitado, activo y ejecutado en una fecha son estados distintos.",
                "El historial de shell no es un registro de auditoría.",
            ]},
            {"t": "macOS", "k": "violeta", "b": [
                "LaunchAgents, LaunchDaemons y elementos de inicio.",
                "SIP y el volumen firmado cambian dónde merece la pena mirar.",
                "La firma de código no equivale a confianza sobre el efecto.",
            ]},
        ],
        "Figura 16.2. Lugares de persistencia frecuentes. El detalle de rutas y eventos se contrasta con la versión del sistema, como en los capítulos de cada plataforma.",
        [("Windows", "azul"), ("Linux", "ambar"), ("macOS", "violeta")],
        accent="rosa",
    )

    flow(
        "figura16.3.png",
        "Triaje de un fichero sospechoso sobre una copia",
        "Ningún paso se ejecuta en el equipo original ni en el puesto cotidiano del analista",
        [
            {"t": "Identificar", "k": "pizarra", "b": [
                "Hash, tamaño, ruta de hallazgo y tipo declarado.",
                "El tipo por contenido puede discrepar de la extensión.",
                "Se anota la cuenta y el volumen de procedencia.",
            ]},
            {"t": "Contextualizar", "k": "azul", "b": [
                "Proceso padre, usuario, hora y mecanismo de persistencia.",
                "Un hash conocido acelera; no cierra el caso.",
                "Se registran también las búsquedas negativas.",
            ]},
            {"t": "Decidir el entorno", "k": "ambar", "b": [
                "Metadatos y estructura pueden bastar para una pregunta concreta.",
                "La ejecución, si hace falta, ocurre en un laboratorio aislado.",
                "La decisión y su motivo quedan escritos antes de actuar.",
            ]},
            {"t": "Correlacionar", "k": "verde", "b": [
                "Se vuelve al disco, a la memoria y a la red del caso.",
                "Lo visto en el laboratorio no se atribuye al equipo sin puente.",
                "El informe separa muestra, comportamiento y hecho investigado.",
            ]},
        ],
        "Figura 16.3. Orden de triaje. El aislamiento protege la evidencia y evita ejecutar código no confiable en el sistema de análisis.",
        [("Copia", "pizarra"), ("Decisión", "ambar"), ("Vuelta al caso", "verde")],
        accent="ambar",
    )

    flow(
        "figura16.4.png",
        "Laboratorio: análisis estático y dinámico separados",
        "El puesto de examen no comparte red con la muestra en ejecución",
        [
            {"t": "Estático, sin ejecutar", "k": "azul", "b": [
                "Formato, hashes, cadenas visibles, imports y firma.",
                "Puede hacerse en una estación sin red de producción.",
                "No muestra lo que el programa haría solo en determinadas condiciones.",
            ]},
            {"t": "Dinámico, en huésped aislado", "k": "rosa", "b": [
                "Máquina virtual con instantánea conocida y reloj documentado.",
                "Red simulada o filtrada, sin salida hacia la organización.",
                "Se conserva la captura de lo ocurrido dentro de ese ensayo.",
            ]},
            {"t": "Puente con el caso", "k": "verde", "b": [
                "Solo se traslada lo que aparece también en la evidencia.",
                "Un comportamiento de laboratorio es una observación experimental.",
                "No es, por sí mismo, la reconstrucción del incidente.",
            ]},
        ],
        "Figura 16.4. Dos modos y un puente. Mezclarlos produce informes que atribuyen al incidente lo que solo ocurrió en el ensayo.",
        [("Estático", "azul"), ("Dinámico", "rosa"), ("Caso", "verde")],
        accent="rosa",
    )

    flow(
        "figura16.5.png",
        "Cuatro fuentes para una sola pregunta",
        "Memoria, disco, registro de procesos y tráfico no demuestran lo mismo",
        [
            {"t": "Memoria", "k": "violeta", "b": [
                "Estado volátil en el momento de la captura.",
                "Procesos, módulos y conexiones entonces presentes.",
                "No conserva toda la historia anterior.",
            ]},
            {"t": "Disco", "k": "azul", "b": [
                "Ficheros, configuración y restos.",
                "Puede mostrar persistencia aún no ejecutada.",
                "También conserva instaladores legítimos.",
            ]},
            {"t": "Registro de ejecución", "k": "ambar", "b": [
                "Eventos de proceso, servicio o auditoría, si existían.",
                "Depende de la política que estuviera activa.",
                "La ausencia puede deberse a retención, no a inocencia.",
            ]},
            {"t": "Tráfico y registros de red", "k": "teal", "b": [
                "Sesiones, nombres consultados y volúmenes.",
                "Cifra el contenido con frecuencia.",
                "No identifica el fichero transferido sin más datos.",
            ]},
        ],
        "Figura 16.5. Correlación. La conclusión más sólida es la que dice qué fuente aporta cada pieza y cuál falta.",
        [("Estado", "violeta"), ("Persistencia", "azul"), ("Canal", "teal")],
    )

    flow(
        "figura16.6.png",
        "Reconstrucción de una intrusión: fuerza de cada tramo",
        "Escenario ficticio. El color indica la fuerza, no la gravedad",
        [
            {"t": "Acceso inicial", "k": "ambar", "badge": "inferido", "b": [
                "Cuenta válida usada desde una dirección nueva.",
                "No hay prueba de cómo se obtuvo la credencial.",
                "Siguen abiertas la reutilización y el acceso legítimo no documentado.",
            ]},
            {"t": "Ejecución", "k": "verde", "badge": "observado", "b": [
                "Un evento de proceso registra ruta, usuario y hora.",
                "El hash coincide con un fichero aún en disco.",
                "Eso demuestra ejecución de ese binario, no todo su efecto.",
            ]},
            {"t": "Persistencia", "k": "azul", "badge": "observado", "b": [
                "Existe un servicio apuntando a la misma ruta.",
                "No hay evento posterior de rearranque de ese servicio.",
                "Preparado no equivale a utilizado de nuevo.",
            ]},
            {"t": "Salida de datos", "k": "rosa", "badge": "pendiente", "b": [
                "Hay una conexión saliente en la misma ventana.",
                "Falta volumen, nombre de objeto y destino útil.",
                "No se afirma exfiltración.",
            ]},
        ],
        "Figura 16.6. Tramos de una intrusión ficticia. El informe puede cerrar un tramo y dejar otro expresamente abierto.",
        [("Inferido", "ambar"), ("Observado", "verde"), ("Pendiente", "rosa")],
        accent="rosa",
    )

    layers(
        "figura17.1.png",
        "Android: capas que condicionan la evidencia",
        "El detalle cambia con la versión, el fabricante y el parche",
        [
            {"t": "Aplicaciones y perfil de usuario", "k": "verde", "b": "Cada aplicación queda contenida. Sus bases, cachés y ficheros compartidos son fuentes distintas y no heredan un significado único."},
            {"t": "Cifrado de ficheros y arranque verificado", "k": "azul", "b": "El cifrado en reposo y la cadena de arranque determinan si una copia de bloques será legible y si el sistema arrancado es el esperado."},
            {"t": "Núcleo, SELinux y sandbox", "k": "violeta", "b": "El aislamiento entre aplicaciones limita qué puede ver cada una. Un permiso concedido no prueba que el recurso se usara."},
            {"t": "Hardware, bloqueo y estado", "k": "ambar", "b": "Encendido, bloqueado, red y nivel de batería deciden qué se puede conservar. Esas condiciones se documentan antes de intervenir."},
        ],
        "Figura 17.1. Mapa de capas. Sirve para elegir una modalidad de extracción, no para suponer que todas están disponibles.",
        [("Datos de usuario", "verde"), ("Protección", "azul"), ("Estado", "ambar")],
        accent="verde",
    )

    flow(
        "figura17.2.png",
        "Preservación de un teléfono Android",
        "Primero se documenta el estado. Después se decide si conviene tocar el dispositivo",
        [
            {"t": "Documentar", "k": "pizarra", "b": [
                "Modelo, IMEI solo si el encargo lo exige, versión y parche.",
                "Encendido o apagado, bloqueo, SIM y redes activas.",
                "Fotografía del estado de pantalla, sin manipular notificaciones.",
            ]},
            {"t": "Aislar con criterio", "k": "ambar", "b": [
                "La red puede traer borrados remotos o nueva sincronización.",
                "También puede ser la vía de un desbloqueo legítimo ya autorizado.",
                "La decisión de aislar se anota con su motivo.",
            ]},
            {"t": "No reiniciar por rutina", "k": "rosa", "b": [
                "Un reinicio pierde estado volátil y puede completar un cifrado.",
                "Apagar no es siempre la opción más conservadora.",
                "Se actúa según batería, bloqueo y pregunta del caso.",
            ]},
            {"t": "Registrar la intervención", "k": "verde", "b": [
                "Quién tocó el equipo, cuándo y con qué resultado.",
                "Los comandos de consulta también son intervención.",
                "La cadena de custodia empieza en este momento, no en el laboratorio.",
            ]},
        ],
        "Figura 17.2. Decisiones de preservación. No hay un gesto único que sirva para todos los teléfonos encendidos.",
        [("Hecho", "pizarra"), ("Riesgo", "rosa"), ("Custodia", "verde")],
        accent="verde",
    )

    flow(
        "figura17.3.png",
        "Modalidades de extracción y su cobertura",
        "El nombre comercial de la herramienta no describe lo que se obtuvo",
        [
            {"t": "Manual o lógica", "k": "verde", "b": [
                "Informes, copias de seguridad y exportaciones visibles.",
                "Útil con cooperación y dispositivo desbloqueado.",
                "Omite gran parte de las bases internas de las aplicaciones.",
            ]},
            {"t": "Sistema de archivos", "k": "azul", "b": [
                "Ficheros y bases cuando el acceso está autorizado y es posible.",
                "Hay que llevarse también WAL y SHM.",
                "No incluye necesariamente espacio no asignado.",
            ]},
            {"t": "Física o de bloques", "k": "ambar", "b": [
                "Representación más amplia del medio, si el método existe para ese modelo.",
                "En un dispositivo cifrado puede ser ilegible.",
                "No es una capacidad general de los teléfonos actuales.",
            ]},
            {"t": "Nube de la cuenta", "k": "violeta", "b": [
                "Copias, ubicación y mensajes pueden estar solo en el proveedor.",
                "Es otra autorización y otra retención.",
                "No se deduce del teléfono lo que la nube todavía guarda.",
            ]},
        ],
        "Figura 17.3. Cobertura. El informe nombra la modalidad, el estado del dispositivo y lo que quedó fuera.",
        [("Lógica", "verde"), ("Ficheros", "azul"), ("Cuenta", "violeta")],
        accent="verde",
    )

    flow(
        "figura17.4.png",
        "Artefactos de una aplicación Android",
        "El paquete organiza los datos; el significado lo pone la versión de la aplicación",
        [
            {"t": "Área privada", "k": "azul", "b": [
                "Bases y preferencias del paquete, si la extracción las alcanza.",
                "SQLite más sus ficheros laterales.",
                "El esquema se comprueba; no se memoriza de un caso antiguo.",
            ]},
            {"t": "Almacenamiento compartido", "k": "verde", "b": [
                "Medios y descargas visibles para otras aplicaciones.",
                "Un fichero aquí no indica qué aplicación lo creó.",
                "Las marcas de tiempo pueden ser de copia, no de captura.",
            ]},
            {"t": "Restos y copias", "k": "ambar", "b": [
                "Cachés, miniaturas y copias de seguridad locales.",
                "Pueden sobrevivir a un borrado dentro de la aplicación.",
                "También pueden no significar más que una vista previa.",
            ]},
        ],
        "Figura 17.4. Tres zonas de la misma aplicación. Tratarlas como un único «chat» mezcla observaciones de fuerza distinta.",
        [("Privado", "azul"), ("Compartido", "verde"), ("Restos", "ambar")],
        accent="verde",
    )

    flow(
        "figura17.5.png",
        "Localización y actividad: tres procedencias",
        "Un punto en un mapa es una interpretación de una fuente concreta",
        [
            {"t": "El propio teléfono", "k": "azul", "b": [
                "Cachés de redes, fotos con coordenadas y bases de aplicaciones.",
                "La precisión y el origen —GPS, red o manual— cambian el significado.",
                "Una miniatura no sitúa a la persona en ese lugar.",
            ]},
            {"t": "La aplicación", "k": "ambar", "b": [
                "Historiales de mapas, transporte o mensajería.",
                "Pueden guardar destinos buscados, no visitados.",
                "La versión define las tablas disponibles.",
            ]},
            {"t": "La cuenta en la nube", "k": "violeta", "b": [
                "Historial de ubicación del proveedor, si existe y se autoriza.",
                "Puede contener días que el teléfono ya no tiene.",
                "También puede mezclar varios dispositivos de la misma cuenta.",
            ]},
        ],
        "Figura 17.5. Procedencia de una coordenada. El informe dice de qué depósito salió y qué error de interpretación se ha evitado.",
        [("Dispositivo", "azul"), ("Aplicación", "ambar"), ("Cuenta", "violeta")],
        accent="verde",
    )

    flow(
        "figura17.6.png",
        "Del artefacto a la frase del informe",
        "Cuatro saltos que no deben colapsarse en una sola oración",
        [
            {"t": "Observación", "k": "azul", "b": [
                "Qué fichero, qué campo, qué hora y qué hash de la copia.",
                "Herramienta y versión usadas para leerlo.",
            ]},
            {"t": "Explicación técnica", "k": "ambar", "b": [
                "Qué mecanismo escribe normalmente ese campo.",
                "Qué otras causas conocidas lo producen.",
            ]},
            {"t": "Inferencia del caso", "k": "verde", "b": [
                "Qué hipótesis favorece y cuáles siguen vivas.",
                "Qué fuente independiente la refuerza o la debilita.",
            ]},
            {"t": "Límite explícito", "k": "rosa", "b": [
                "Qué no se puede afirmar.",
                "Qué dato faltante cambiaría la lectura.",
            ]},
        ],
        "Figura 17.6. Plantilla de redacción. Una frase que salta de la observación al motivo de una persona no está terminada.",
        [("Hecho", "azul"), ("Mecanismo", "ambar"), ("Límite", "rosa")],
        accent="verde",
    )

    layers(
        "figura18.1.png",
        "iOS y iPadOS: protección de datos antes que rutas",
        "Sin el estado de desbloqueo, muchas adquisiciones solo conservan bloques opacos",
        [
            {"t": "Código, Secure Enclave y clases de protección", "k": "violeta", "b": "Las clases de protección de datos atan ficheros a claves que pueden exigir el código del usuario después de un bloqueo. No es una única contraseña guardada en un archivo."},
            {"t": "Volumen cifrado y arranque", "k": "azul", "b": "El almacenamiento interno está cifrado y vinculado al dispositivo. Extraer el medio no entrega, por sí solo, el contenido."},
            {"t": "Contenedores de aplicaciones", "k": "verde", "b": "Cuando una extracción autorizada los alcanza, cada aplicación conserva sus datos en un contenedor. El esquema depende de la versión."},
            {"t": "Copias y servicios de la cuenta", "k": "ambar", "b": "La copia local y la copia en iCloud son fuentes distintas, con cifrado, retención y cobertura diferentes."},
        ],
        "Figura 18.1. Condiciones de acceso. La arquitectura se usa para explicar qué modalidad es realista, no para prometer una extracción universal.",
        [("Hardware y claves", "violeta"), ("Aplicaciones", "verde"), ("Copias", "ambar")],
        accent="violeta",
    )

    flow(
        "figura18.2.png",
        "Preservación y adquisición en iPhone y iPad",
        "El estado de bloqueo pesa más que el modelo comercial de la herramienta",
        [
            {"t": "Estado", "k": "pizarra", "b": [
                "Encendido, bloqueado, versión de iOS y modelo.",
                "Confianza del equipo con un ordenador ya emparejado.",
                "Red, batería y si hay una copia reciente conocida.",
            ]},
            {"t": "Vías ordinarias", "k": "verde", "b": [
                "Cooperación, código facilitado y copia de seguridad cifrada.",
                "Exportaciones de aplicaciones dentro del alcance.",
                "Registros ya conservados por la organización.",
            ]},
            {"t": "Vías especializadas", "k": "ambar", "b": [
                "Dependen del modelo, del iOS y de la autorización.",
                "Un método publicado para un chip antiguo no se traslada.",
                "Su cobertura se describe; no se da por completa.",
            ]},
            {"t": "Lo que no se hace", "k": "rosa", "b": [
                "No se prueba el desbloqueo repetidamente sobre el original.",
                "No se actualiza el sistema «para que la herramienta funcione».",
                "No se presenta una explotación como procedimiento del libro.",
            ]},
        ],
        "Figura 18.2. Decisión de adquisición. Lo excluido forma parte del método, porque protege la evidencia y el alcance legal.",
        [("Ordinaria", "verde"), ("Especializada", "ambar"), ("Excluido", "rosa")],
        accent="violeta",
    )

    flow(
        "figura18.3.png",
        "Copias de seguridad: útiles y parciales",
        "Una copia no es una imagen del dispositivo",
        [
            {"t": "Copia local", "k": "azul", "b": [
                "Manifiestos que relacionan objetos con rutas lógicas.",
                "Los nombres de fichero de la copia no son las rutas originales.",
                "Hay que conservar el conjunto, no un solo archivo suelto.",
            ]},
            {"t": "Cifrada o sin cifrar", "k": "violeta", "b": [
                "La copia cifrada puede incluir más material del llavero.",
                "Sigue sin ser todo el sistema de archivos.",
                "La contraseña de la copia es distinta del código del dispositivo.",
            ]},
            {"t": "iCloud y otros dispositivos", "k": "ambar", "b": [
                "Otra autorización, otra retención y otros objetos.",
                "Puede reflejar varios dispositivos de la misma cuenta.",
                "Un mensaje presente solo allí no estaba necesariamente en el teléfono intervenido.",
            ]},
        ],
        "Figura 18.3. Tres copias que no se suman sin más. El informe dice cuál se analizó y qué clases de datos suelen quedar fuera.",
        [("Local", "azul"), ("Cifrada", "violeta"), ("Cuenta", "ambar")],
        accent="violeta",
    )

    flow(
        "figura18.4.png",
        "Aplicaciones, comunicaciones y actividad",
        "Cada fuente tiene su reloj y su motivo para existir",
        [
            {"t": "Mensajes", "k": "azul", "b": [
                "Base local, notificaciones y copia en el servicio pueden divergir.",
                "Un borrado en la vista no borra todas las réplicas.",
                "El sentido de la conversación no se deduce de un solo globo.",
            ]},
            {"t": "Actividad del sistema", "k": "verde", "b": [
                "Registros de uso, conocimiento y localización dependen de la versión.",
                "Pueden estar agregados y no ser una traza continua.",
                "Su ausencia puede deberse a la modalidad de extracción.",
            ]},
            {"t": "Documentos y fotos", "k": "ambar", "b": [
                "Metadatos internos, álbum y copia en la nube.",
                "La fecha de captura y la fecha de copia no coinciden siempre.",
                "Una coordenada puede haber sido editada o heredada.",
            ]},
        ],
        "Figura 18.4. Tres familias de actividad. Se citan por separado aunque el lector quiera una sola historia.",
        [("Comunicación", "azul"), ("Sistema", "verde"), ("Documento", "ambar")],
        accent="violeta",
    )

    flow(
        "figura18.5.png",
        "Validar un resultado de móvil antes de firmarlo",
        "La segunda lectura busca el mismo dato, no una confirmación complaciente",
        [
            {"t": "Fuente", "k": "pizarra", "b": [
                "Hash de la copia o de la base examinada.",
                "Versión de iOS, de la aplicación y del analizador.",
            ]},
            {"t": "Segunda vía", "k": "azul", "b": [
                "Consulta independiente del mismo campo.",
                "Si la herramienta lo traduce, se mira también el valor bruto.",
            ]},
            {"t": "Conjunto conocido", "k": "verde", "b": [
                "Cuando sea posible, un ensayo con datos sembrados.",
                "Sirve para entender el campo, no para fabricar el caso.",
            ]},
            {"t": "Negativos", "k": "rosa", "b": [
                "Lo buscado y no hallado se anota con el alcance.",
                "Un fallo del parser no se redacta como ausencia del hecho.",
            ]},
        ],
        "Figura 18.5. Controles de validación. Repetir la misma pulsación de la misma herramienta no es una segunda fuente.",
        [("Bruto", "azul"), ("Ensayo", "verde"), ("Negativo", "rosa")],
        accent="violeta",
    )

    flow(
        "figura18.6.png",
        "Caso de laboratorio: copia, mensaje y lugar",
        "Escenario ficticio de un iPhone corporativo",
        [
            {"t": "Copia cifrada", "k": "azul", "badge": "observado", "b": [
                "Se obtiene con la contraseña facilitada por la organización.",
                "Incluye la base de mensajes de la aplicación examinada.",
                "No incluye el sistema de archivos completo.",
            ]},
            {"t": "Mensaje y adjunto", "k": "ambar", "badge": "correlación", "b": [
                "Hay un mensaje en la ventana del encargo.",
                "El adjunto de la copia y el fichero del portátil no coinciden en hash.",
                "Pueden ser versiones distintas o un adjunto sustituido.",
            ]},
            {"t": "Localización", "k": "rosa", "badge": "límite", "b": [
                "Una foto del carrete lleva coordenadas.",
                "No hay historial de ubicación de la cuenta dentro del alcance.",
                "No se sitúa al usuario durante toda la mañana.",
            ]},
        ],
        "Figura 18.6. Cierre parcial de un caso ficticio. Lo observado queda separado de lo que la copia no puede sostener.",
        [("Copia", "azul"), ("Contraste", "ambar"), ("Límite", "rosa")],
        accent="violeta",
    )

    flow(
        "figura19.1.png",
        "Quién puede tener la evidencia en la nube",
        "El modelo de servicio reparte el control; no elimina la necesidad de autorización",
        [
            {"t": "IaaS", "k": "azul", "b": [
                "El cliente suele controlar sistema, aplicaciones y parte de los registros.",
                "El proveedor controla el hipervisor y la plataforma física.",
                "Una instantánea de volumen es del cliente si su cuenta puede crearla.",
            ]},
            {"t": "PaaS", "k": "ambar", "b": [
                "El cliente controla la aplicación y sus datos.",
                "El sistema operativo subyacente puede quedar fuera de su alcance.",
                "Los registros de plataforma dependen del plan contratado.",
            ]},
            {"t": "SaaS", "k": "violeta", "b": [
                "El cliente conserva configuración, identidades y exportaciones.",
                "La infraestructura no es accesible como un disco.",
                "El contrato y los registros de auditoría son la vía principal.",
            ]},
        ],
        "Figura 19.1. Reparto orientativo, no una regla de todos los contratos. El acuerdo real manda sobre el esquema.",
        [("IaaS", "azul"), ("PaaS", "ambar"), ("SaaS", "violeta")],
        accent="cielo",
    )

    flow(
        "figura19.2.png",
        "Retos forenses de la nube",
        "Categorías descritas a partir de NIST IR 8006 y retomadas en NIST SP 800-201",
        [
            {"t": "Arquitectura y recogida", "k": "azul", "b": [
                "Multiinquilino, elasticidad y datos repartidos.",
                "No siempre se puede imagenar «el servidor».",
                "La recogida no debe exponer a otros clientes.",
            ]},
            {"t": "Análisis y tiempo", "k": "ambar", "b": [
                "Correlación entre servicios y proveedores.",
                "Relojes y metadatos de distinta resolución.",
                "Los registros solo existen si alguien los activó y los conservó.",
            ]},
            {"t": "Identidad y rol", "k": "verde", "b": [
                "La credencial no es la persona.",
                "Cuentas de servicio, federación y roles temporales.",
                "Hay que conservar el identificador, no solo el nombre visible.",
            ]},
            {"t": "Derecho y contrato", "k": "violeta", "b": [
                "Jurisdicción, encargo y acuerdo de servicio.",
                "La vía técnica no sustituye a la vía de acceso legítima.",
                "Privacidad de terceros que comparten el mismo servicio.",
            ]},
        ],
        "Figura 19.2. Cuatro grupos de retos. El documento del NIST detalla más categorías, entre ellas normas, formación y primera respuesta.",
        [("Plataforma", "azul"), ("Identidad", "verde"), ("Marco", "violeta")],
        accent="cielo",
    )

    flow(
        "figura19.3.png",
        "Preparación forense antes del incidente",
        "Lo que no se activó y no se retuvo no podrá pedirse después con el mismo detalle",
        [
            {"t": "Registrar", "k": "azul", "b": [
                "Auditoría de plano de gestión y, si procede, de datos.",
                "Identidad, resultado y recurso en cada evento.",
                "Reloj coherente y zona horaria documentada.",
            ]},
            {"t": "Conservar", "k": "ambar", "b": [
                "Retención y almacén inmutable cuando el servicio lo ofrezca.",
                "Separar la cuenta que investiga de la cuenta investigada.",
                "Probar que el registro cabe en el plazo del caso.",
            ]},
            {"t": "Ensayar", "k": "verde", "b": [
                "Una exportación de prueba revela permisos que faltan.",
                "Se anota el coste, el volumen y el tiempo de respuesta.",
                "El ensayo no se hace sobre la evidencia del incidente ya abierto.",
            ]},
        ],
        "Figura 19.3. Preparación. NIST SP 800-201 trata la arquitectura de referencia para esta preparación; no sustituye el diseño concreto de cada cuenta.",
        [("Registro", "azul"), ("Retención", "ambar"), ("Ensayo", "verde")],
        accent="cielo",
    )

    flow(
        "figura19.4.png",
        "Fuentes que suelen existir en tres plataformas",
        "Nombres de servicio orientativos. La región, el plan y la configuración deciden si hay datos",
        [
            {"t": "AWS", "k": "ambar", "b": [
                "CloudTrail para llamadas a la API de gestión.",
                "Registros de flujo de VPC y accesos a almacenamiento, si se activaron.",
                "El historial reciente no reemplaza un trail con retención propia.",
            ]},
            {"t": "Azure", "k": "azul", "b": [
                "Registro de actividad de la suscripción.",
                "Inicios de sesión y auditoría de identidad, según licencia y diagnóstico.",
                "Registros de plataforma y de recurso son niveles distintos.",
            ]},
            {"t": "Google Cloud", "k": "verde", "b": [
                "Cloud Audit Logs: actividad de administración y, si se habilita, acceso a datos.",
                "Registros de flujo de VPC cuando existen.",
                "La retención por defecto puede ser más corta que el caso.",
            ]},
        ],
        "Figura 19.4. Puntos de entrada. Cada nombre debe comprobarse en la documentación vigente del proveedor antes de citarlo en un informe.",
        [("AWS", "ambar"), ("Azure", "azul"), ("Google Cloud", "verde")],
        accent="cielo",
    )

    flow(
        "figura19.5.png",
        "Identidad, API, almacenamiento y SaaS",
        "Cuatro preguntas que no se responden con el mismo registro",
        [
            {"t": "¿Quién?", "k": "violeta", "b": [
                "Principal, rol asumido, aplicación federada.",
                "MFA y contexto del inicio de sesión, si se registró.",
                "Una clave de API no tiene horario de oficina.",
            ]},
            {"t": "¿Qué llamada?", "k": "azul", "b": [
                "Servicio, operación, recurso y resultado.",
                "Error de permiso es un hecho distinto de una operación lograda.",
                "La ausencia de data events puede ocultar lecturas de objetos.",
            ]},
            {"t": "¿Qué dato?", "k": "ambar", "b": [
                "Versiones, bloqueos de retención y copias del objeto.",
                "Un cubo o contenedor no es un disco con espacio no asignado clásico.",
                "El hash, si se calculó, se conserva con el método.",
            ]},
            {"t": "¿Qué aplicación SaaS?", "k": "verde", "b": [
                "Auditoría del arrendatario, buzones y registros de archivo.",
                "Exportación según contrato y rol de administrador.",
                "El proveedor puede no entregar la infraestructura subyacente.",
            ]},
        ],
        "Figura 19.5. Preguntas separadas. Un evento de API demuestra una llamada autorizada por unas credenciales, no el contenido descargado, salvo que el registro lo diga.",
        [("Identidad", "violeta"), ("API", "azul"), ("Dato", "ambar")],
        accent="cielo",
    )

    flow(
        "figura19.6.png",
        "Reconstrucción de un incidente en la nube",
        "Caso ficticio: una clave de almacenamiento y un objeto nuevo",
        [
            {"t": "Credencial", "k": "ambar", "badge": "observado", "b": [
                "CloudTrail muestra AssumeRole desde una dirección no inventariada.",
                "La clave de acceso pertenece a un usuario de automatización.",
                "No identifica a la persona que la copió.",
            ]},
            {"t": "Objeto", "k": "azul", "badge": "observado", "b": [
                "Hay un PutObject en la misma hora, con nombre y tamaño.",
                "El registro de datos estaba activo en ese cubo.",
                "El objeto sigue bajo retención.",
            ]},
            {"t": "Contenido y destino", "k": "rosa", "badge": "parcial", "b": [
                "El objeto es un archivo cifrado por la aplicación.",
                "No hay registro del puesto que lo generó.",
                "No se afirma qué información de negocio contiene.",
            ]},
        ],
        "Figura 19.6. Tramo cloud de un caso ficticio. La llamada y el objeto están observados; el significado de negocio queda pendiente.",
        [("Identidad técnica", "ambar"), ("Objeto", "azul"), ("Pendiente", "rosa")],
        accent="cielo",
    )

    flow(
        "figura19.7.png",
        "Qué se pide y qué se puede mirar ya",
        "Separar la cuenta del cliente de la petición al proveedor",
        [
            {"t": "Ya en la cuenta", "k": "verde", "b": [
                "Registros que el cliente configuró y aún retiene.",
                "Instantáneas, objetos y configuración exportable.",
                "Identidades y políticas de la propia organización.",
            ]},
            {"t": "Hay que pedir", "k": "ambar", "b": [
                "Registros que solo conserva el proveedor.",
                "Datos de otro inquilino, que normalmente no se obtienen.",
                "Conservación legal, con su propio procedimiento.",
            ]},
            {"t": "No estará", "k": "rosa", "b": [
                "Espacio no asignado de un hipervisor ajeno.",
                "Memoria de una función que ya terminó, si nadie la registró.",
                "Un historial infinito de API solo porque el servicio existe.",
            ]},
        ],
        "Figura 19.7. Expectativas. Pedir «una imagen forense del cloud» no describe una operación real en la mayoría de los servicios.",
        [("Disponible", "verde"), ("Petición", "ambar"), ("Inalcanzable", "rosa")],
        accent="cielo",
    )

    flow(
        "figura20.1.png",
        "Hipervisor y máquina virtual: dos escenas",
        "La evidencia puede estar en el invitado, en el anfitrión o en ambos",
        [
            {"t": "Invitado", "k": "azul", "b": [
                "Sistema de archivos, memoria y registros del sistema instalado.",
                "Se analiza como un equipo, con las cautelas de los capítulos anteriores.",
                "No ve, normalmente, las otras máquinas del mismo anfitrión.",
            ]},
            {"t": "Anfitrión", "k": "verde", "b": [
                "Configuración de la máquina, discos, instantáneas y registros del hipervisor.",
                "Puede mostrar encendidos, migraciones y consolas.",
                "Su reloj no sustituye al reloj del invitado.",
            ]},
            {"t": "Plataforma", "k": "violeta", "b": [
                "Orquestador, clúster o nube que mueve la máquina.",
                "Una migración cambia de anfitrión sin cambiar el nombre lógico.",
                "Hay que conservar el identificador, no solo el nombre.",
            ]},
        ],
        "Figura 20.1. Tres niveles. Apagar la máquina equivocada —anfitrión o invitado— destruye evidencias distintas.",
        [("Invitado", "azul"), ("Anfitrión", "verde"), ("Plataforma", "violeta")],
        accent="teal",
    )

    flow(
        "figura20.2.png",
        "Discos virtuales e instantáneas",
        "Un fichero de disco no es automáticamente una imagen forense",
        [
            {"t": "Disco virtual", "k": "azul", "b": [
                "VMDK, VHD, VHDX, QCOW2 y raw son contenedores distintos.",
                "Pueden ser planos, diferenciales o encadenados.",
                "Copiar solo el diferencial deja la cadena incompleta.",
            ]},
            {"t": "Instantánea", "k": "ambar", "b": [
                "Conserva un estado anterior si todavía existe.",
                "No es un historial continuo de todo lo escrito.",
                "Consolidar o borrar instantáneas es una intervención.",
            ]},
            {"t": "Memoria suspendida", "k": "violeta", "b": [
                "Algunos estados guardan RAM junto al disco.",
                "Es volátil en origen, aunque ahora esté en un fichero.",
                "Su utilidad depende de que el formato se interprete.",
            ]},
            {"t": "Integridad", "k": "verde", "b": [
                "Hash del fichero copiado y relación con la cadena.",
                "Se documenta si la máquina estaba encendida.",
                "Una copia en caliente puede ser incoherente.",
            ]},
        ],
        "Figura 20.2. Objetos virtuales. El informe nombra el formato, la cadena de diferenciales y si la copia se tomó en caliente o en frío.",
        [("Disco", "azul"), ("Estado", "ambar"), ("Integridad", "verde")],
        accent="teal",
    )

    flow(
        "figura20.3.png",
        "Docker: qué puede conservarse y qué es efímero",
        "El contenedor en ejecución no agota la evidencia",
        [
            {"t": "Imagen", "k": "azul", "b": [
                "Capas de solo lectura y manifiesto.",
                "El identificador de imagen permite repetir el análisis.",
                "Una etiqueta latest no es un identificador estable.",
            ]},
            {"t": "Contenedor", "k": "ambar", "b": [
                "Capa escribible, configuración y variables.",
                "Desaparece si se borra el contenedor y no hay copia.",
                "Los registros dependen del controlador configurado.",
            ]},
            {"t": "Volúmenes y red", "k": "verde", "b": [
                "Los datos persistentes suelen estar en volúmenes, no en la capa efímera.",
                "La red publicada explica puertos, no el contenido de las sesiones.",
                "Un volumen compartido puede mezclar varios contenedores.",
            ]},
        ],
        "Figura 20.3. Tres objetos Docker. Parar y borrar «para limpiar» elimina precisamente la capa que diferencia al contenedor de la imagen.",
        [("Imagen", "azul"), ("Capa viva", "ambar"), ("Volumen", "verde")],
        accent="teal",
    )

    flow(
        "figura20.4.png",
        "Kubernetes: el pod no es el único registro",
        "El plano de control, el nodo y la carga dicen cosas distintas",
        [
            {"t": "Carga", "k": "azul", "b": [
                "Pod, contenedores, montajes y variables.",
                "Un pod recreado no conserva la capa anterior.",
                "Las sondas y los reinicios explican huecos.",
            ]},
            {"t": "Nodo", "k": "ambar", "b": [
                "Runtime, imágenes en caché y registros locales.",
                "Puede sobrevivir al borrado del objeto en la API.",
                "También puede reciclarse y perder esa caché.",
            ]},
            {"t": "Plano de control", "k": "violeta", "b": [
                "Auditoría de la API, si está habilitada.",
                "Quién pidió crear, ejecutar o borrar.",
                "No contiene el fichero que la aplicación escribió en un volumen.",
            ]},
            {"t": "Despliegue", "k": "verde", "b": [
                "Manifiestos, historial de revisiones y registro de imágenes.",
                "Permiten saber qué se declaró, no todo lo que se ejecutó.",
                "Una imagen cambiada bajo la misma etiqueta confunde la revisión.",
            ]},
        ],
        "Figura 20.4. Cuatro sitios. La auditoría de la API no reemplaza el volumen ni el registro del contenedor.",
        [("Carga", "azul"), ("Nodo", "ambar"), ("API", "violeta")],
        accent="teal",
    )

    flow(
        "figura20.5.png",
        "Orden de preservación en un entorno orquestado",
        "Lo más volátil no es siempre lo más útil; sí es lo que antes desaparece",
        [
            {"t": "Identificar", "k": "pizarra", "b": [
                "Clúster, espacio de nombres, carga e identificadores.",
                "Nodo donde corre ahora, que puede cambiar.",
            ]},
            {"t": "Capturar lo efímero", "k": "rosa", "b": [
                "Estado, registros aún no enviados y, si procede, memoria.",
                "Anotando el efecto de la propia captura.",
            ]},
            {"t": "Copiar lo persistente", "k": "azul", "b": [
                "Volúmenes, objetos de configuración y registros centralizados.",
                "Imagen por identificador, no solo por etiqueta.",
            ]},
            {"t": "Proteger el plano", "k": "verde", "b": [
                "Auditoría y manifiestos.",
                "Evitar borrados de «limpieza» hasta que la copia esté verificada.",
            ]},
        ],
        "Figura 20.5. Secuencia orientativa. Se altera si una destrucción automática del pod es inminente y esa es la evidencia crítica.",
        [("Efímero", "rosa"), ("Persistente", "azul"), ("Control", "verde")],
        accent="teal",
    )

    flow(
        "figura20.6.png",
        "Caso de laboratorio: un pod y un volumen",
        "Escenario ficticio. La etiqueta de la imagen no basta para repetir el análisis",
        [
            {"t": "Declaración", "k": "azul", "badge": "observado", "b": [
                "El manifiesto fija la imagen por etiqueta latest.",
                "El identificador resuelto aquel día está en el registro del nodo.",
                "Hoy, latest apunta a otra compilación.",
            ]},
            {"t": "Ejecución", "k": "ambar", "badge": "parcial", "b": [
                "La auditoría de la API muestra quién creó el despliegue.",
                "Los registros del contenedor cubren solo unas horas.",
                "No hay captura de memoria del pod.",
            ]},
            {"t": "Dato", "k": "verde", "badge": "observado", "b": [
                "El volumen conserva un fichero con hash calculado.",
                "No está en la imagen de solo lectura.",
                "Eso sitúa el fichero en la capa persistente, no a su autor humano.",
            ]},
        ],
        "Figura 20.6. Caso ficticio de contenedores. Identificador de imagen, auditoría y volumen responden a tres preguntas distintas.",
        [("Imagen", "azul"), ("API", "ambar"), ("Volumen", "verde")],
        accent="teal",
    )

    flow(
        "figura21.1.png",
        "Un dispositivo IoT casi nunca está solo",
        "El objeto físico es una pieza de un sistema más amplio",
        [
            {"t": "Dispositivo", "k": "verde", "b": [
                "Firmware, almacenamiento local y registros escasos.",
                "Puede no tener hora fiable ni usuario local.",
            ]},
            {"t": "Pasarela y red", "k": "azul", "b": [
                "Router, puente o hub por el que salen los mensajes.",
                "A menudo conserva más historia que el sensor.",
            ]},
            {"t": "Controlador", "k": "ambar", "b": [
                "Aplicación móvil o panel que configura el dispositivo.",
                "Puede guardar escenas, cuentas y horarios.",
            ]},
            {"t": "Nube del fabricante", "k": "violeta", "b": [
                "Eventos, vídeo o telemetría según el contrato.",
                "Otra autorización y otra retención.",
            ]},
        ],
        "Figura 21.1. Ecosistema. Intervenir solo el aparato pequeño puede destruir poco y conservar menos todavía.",
        [("Objeto", "verde"), ("Red", "azul"), ("Servicio", "violeta")],
        accent="verde",
    )

    flow(
        "figura21.2.png",
        "Identificar y preservar sin convertir el dispositivo en otra cosa",
        "Alimentación, red y emparejamiento forman parte del estado",
        [
            {"t": "Identificar", "k": "pizarra", "b": [
                "Fabricante, modelo, versión visible y número de serie.",
                "Función en la escena: cámara, sensor, cerradura, router.",
                "Relación con la cuenta y con la aplicación.",
            ]},
            {"t": "Alimentar y aislar", "k": "ambar", "b": [
                "Muchos dispositivos pierden estado al quedarse sin energía.",
                "La red puede seguir sobrescribiendo búferes circulares.",
                "Aislar también impide una actualización o un borrado remoto.",
            ]},
            {"t": "No restablecer", "k": "rosa", "b": [
                "Un restablecimiento de fábrica es una destrucción.",
                "Emparejar de nuevo el dispositivo cambia credenciales.",
                "Las pulsaciones de prueba se anotan como experimento, no como hecho.",
            ]},
        ],
        "Figura 21.2. Preservación. El orden se justifica por la volatilidad real del aparato, no por una plantilla única.",
        [("Identidad", "pizarra"), ("Energía y red", "ambar"), ("No destruir", "rosa")],
        accent="verde",
    )

    flow(
        "figura21.3.png",
        "Firmware, memoria y almacenamiento local",
        "El acceso físico especializado no garantiza contenido en claro",
        [
            {"t": "Firmware", "k": "azul", "b": [
                "Versión y fecha de compilación, si son legibles.",
                "Explica capacidades; no demuestra un evento.",
                "Una extracción de firmware es una técnica de especialista.",
            ]},
            {"t": "Memoria y búferes", "k": "rosa", "b": [
                "Vídeo reciente, colas y registros circulares.",
                "Se pierden con el corte de energía o al llenarse.",
                "Su hora puede ser relativa al arranque, no civil.",
            ]},
            {"t": "Almacenamiento", "k": "verde", "b": [
                "Tarjeta, flash o partición de configuración.",
                "Puede estar cifrado o ser solo un caché.",
                "La copia se hace con el menor arranque posible del original.",
            ]},
        ],
        "Figura 21.3. Tres soportes. Se describe el método solo hasta donde hace falta para entender la cobertura, sin convertir el capítulo en un manual de intrusión sobre el aparato.",
        [("Firmware", "azul"), ("Volátil", "rosa"), ("Persistente", "verde")],
        accent="verde",
    )

    flow(
        "figura21.4.png",
        "Protocolos: qué puede verse en la red",
        "El mensaje observado depende de dónde se capturó y de si iba cifrado",
        [
            {"t": "En el segmento local", "k": "azul", "b": [
                "Descubrimiento, emparejamiento y telemetría de corto alcance.",
                "MQTT, CoAP u otros, según el producto.",
                "Una captura tardía no reconstruye el mes anterior.",
            ]},
            {"t": "Hacia la nube", "k": "violeta", "b": [
                "Conexiones TLS que ocultan el cuerpo.",
                "Quedan direcciones, horas y tamaños, si se registraron.",
                "El nombre DNS no es el contenido del evento.",
            ]},
            {"t": "En el controlador", "k": "ambar", "b": [
                "La aplicación puede mostrar una historia ya interpretada.",
                "Esa historia es una fuente más, con su propia integridad.",
                "No se corrige «a mano» para que encaje con el sensor.",
            ]},
        ],
        "Figura 21.4. Tres puntos de observación. El protocolo explica el límite; no autoriza a descifrar un canal ajeno fuera del encargo.",
        [("Local", "azul"), ("Nube", "violeta"), ("Aplicación", "ambar")],
        accent="verde",
    )

    flow(
        "figura21.5.png",
        "Cámaras, routers, sensores y domótica",
        "Preguntas distintas según la función del aparato",
        [
            {"t": "Cámara", "k": "azul", "b": [
                "Búfer, tarjeta, NVR y nube de vídeo.",
                "Hora en pantalla y hora del fichero pueden diferir.",
                "El movimiento detectado no identifica a una persona.",
            ]},
            {"t": "Router", "k": "verde", "b": [
                "Concesiones, clientes y a veces registros de conexión.",
                "El registro suele ser corto y circular.",
                "Una MAC puede falsificarse; se contrasta, no se adora.",
            ]},
            {"t": "Sensor o cerradura", "k": "ambar", "b": [
                "Eventos de estado: abierto, cerrado, presencia.",
                "Dependen de la pila y de la pasarela.",
                "Un evento perdido no equivale a un evento contrario.",
            ]},
        ],
        "Figura 21.5. Familias de dispositivos. El caso práctico del capítulo elige una y muestra cómo se cruzan con las demás.",
        [("Vídeo", "azul"), ("Red", "verde"), ("Estado", "ambar")],
        accent="verde",
    )

    flow(
        "figura21.6.png",
        "Línea temporal de un ecosistema IoT",
        "Caso ficticio: una cámara, su router y la cuenta del fabricante",
        [
            {"t": "Cámara", "k": "azul", "badge": "parcial", "b": [
                "La tarjeta conserva fragmentos de la madrugada.",
                "El reloj de la cámara iba retrasado varios minutos.",
                "Se documenta el desfase; no se reescriben los ficheros.",
            ]},
            {"t": "Router", "k": "verde", "badge": "observado", "b": [
                "El cliente de la cámara renueva concesión esa noche.",
                "No hay historial de semanas anteriores.",
                "La MAC coincide con la etiqueta del aparato.",
            ]},
            {"t": "Cuenta", "k": "violeta", "badge": "observado", "b": [
                "El fabricante entrega eventos de movimiento bajo requerimiento.",
                "Cubren horas que la tarjeta ya sobrescribió.",
                "No incluyen identidad de la persona que aparece.",
            ]},
            {"t": "Lectura conjunta", "k": "ambar", "badge": "inferencia", "b": [
                "Hay actividad del sistema de cámara en esa ventana.",
                "No se identifica al visitante.",
                "El desfase de reloj impide una hora al segundo.",
            ]},
        ],
        "Figura 21.6. Correlación ficticia. Cada fuente conserva un tramo distinto y una precisión distinta.",
        [("Dispositivo", "azul"), ("Red", "verde"), ("Servicio", "violeta")],
        accent="verde",
    )

    flow(
        "figura21.7.png",
        "Qué se puede afirmar al cerrar un caso IoT",
        "La frase final no es más precisa que la peor fuente de la que depende",
        [
            {"t": "Se observó", "k": "verde", "b": [
                "Eventos concretos, con fuente, hora y margen de error.",
                "Identificadores de aparato y de cuenta.",
            ]},
            {"t": "Es compatible con", "k": "ambar", "b": [
                "Una hipótesis que otras fuentes no contradicen.",
                "Sin convertir la compatibilidad en certeza.",
            ]},
            {"t": "No se establece", "k": "rosa", "b": [
                "Identidad humana, intención y contenido no registrado.",
                "Hechos ocurridos dentro de los huecos de retención.",
            ]},
        ],
        "Figura 21.7. Cierre. Estas tres cajas son también la estructura de la conclusión del informe.",
        [("Observado", "verde"), ("Compatible", "ambar"), ("No establecido", "rosa")],
        accent="verde",
    )

    flow(
        "figura22.1.png",
        "Artefacto, indicio, evidencia e interpretación",
        "Cuatro palabras que el informe no debe usar como sinónimos",
        [
            {"t": "Artefacto", "k": "pizarra", "b": [
                "Objeto técnico producido por un sistema.",
                "Existe con independencia de la hipótesis.",
                "Ejemplo: una fila de una base de historial.",
            ]},
            {"t": "Indicio", "k": "azul", "b": [
                "Artefacto que parece relevante para la pregunta.",
                "Todavía no ha sido contrastado.",
                "Orienta la búsqueda siguiente.",
            ]},
            {"t": "Evidencia", "k": "verde", "b": [
                "Información incorporada al expediente con custodia y método.",
                "Sirve para sostener o debilitar una hipótesis.",
                "Incluye los resultados negativos bien delimitados.",
            ]},
            {"t": "Interpretación", "k": "ambar", "b": [
                "Lectura que une evidencias y conocimientos del mecanismo.",
                "Puede ser revisada sin reescribir los artefactos.",
                "No se presenta como si fuera el artefacto mismo.",
            ]},
        ],
        "Figura 22.1. Escala de lenguaje. Saltar del artefacto a la interpretación es el error que este capítulo enseña a evitar.",
        [("Objeto", "pizarra"), ("Expediente", "verde"), ("Lectura", "ambar")],
        accent="ambar",
    )

    flow(
        "figura22.2.png",
        "Hipótesis rivales antes de la favorita",
        "Una hipótesis útil es concreta, falsable y ligada a una fuente",
        [
            {"t": "Formular", "k": "azul", "b": [
                "Qué hecho concreto afirma.",
                "Qué observación la haría menos creíble.",
                "No es un adjetivo sobre la persona.",
            ]},
            {"t": "Emparejar", "k": "verde", "b": [
                "Qué fuentes la apoyan.",
                "Qué fuentes la contradicen.",
                "Qué fuentes todavía no se han pedido.",
            ]},
            {"t": "Conservar la rival", "k": "ambar", "b": [
                "La explicación ordinaria sigue escrita.",
                "Error, sincronización, cuenta compartida, reloj.",
                "Si no se puede descartar, la conclusión lo dice.",
            ]},
        ],
        "Figura 22.2. Contraste. La hipótesis favorita no se refuerza ocultando la alternativa compatible con los mismos datos.",
        [("Afirmación", "azul"), ("Apoyo", "verde"), ("Rival", "ambar")],
        accent="ambar",
    )

    flow(
        "figura22.3.png",
        "Correlación no es repetición de la misma fuente",
        "Independencia de origen, de reloj y de mecanismo",
        [
            {"t": "Misma fuente, otra herramienta", "k": "rosa", "b": [
                "Comprueba el parser.",
                "No añade un hecho nuevo.",
                "Sigue siendo una sola observación.",
            ]},
            {"t": "Otro mecanismo, mismo equipo", "k": "azul", "b": [
                "Registro de aplicación y metadato del fichero.",
                "Pueden compartir el reloj y el fallo.",
                "Aun así, reducen el error de una sola estructura.",
            ]},
            {"t": "Otro sistema", "k": "verde", "b": [
                "Servidor, proxy, copia o dispositivo distinto.",
                "Es la correlación de más valor.",
                "Hay que alinear zonas horarias antes de unirlos.",
            ]},
        ],
        "Figura 22.3. Grados de independencia. El informe dice de qué grado es cada refuerzo.",
        [("Réplica", "rosa"), ("Mismo equipo", "azul"), ("Sistema distinto", "verde")],
        accent="ambar",
    )

    flow(
        "figura22.4.png",
        "Reconstrucción cronológica",
        "La línea de tiempo muestra incertidumbre, no solo una lista de horas",
        [
            {"t": "Normalizar", "k": "azul", "b": [
                "Una zona de referencia, sin borrar la original.",
                "Resolución de cada marca: día, segundo, microsegundo.",
                "Fuente y reloj asociados.",
            ]},
            {"t": "Ordenar con huecos", "k": "ambar", "b": [
                "Lo que cae dentro de la ventana.",
                "Lo que no puede ordenarse por falta de precisión.",
                "Los periodos sin registros se dibujan, no se rellenan.",
            ]},
            {"t": "Separar hechos", "k": "verde", "b": [
                "Hecho del sistema, hecho de la intervención y hecho inferido.",
                "Tres capas evitan contar el análisis como parte del incidente.",
            ]},
        ],
        "Figura 22.4. Cronología defendible. Una hora sin zona ni fuente es un adorno, no una evidencia.",
        [("Tiempo", "azul"), ("Hueco", "ambar"), ("Tipo de hecho", "verde")],
        accent="ambar",
    )

    flow(
        "figura22.5.png",
        "Autenticidad, integridad y fiabilidad",
        "Tres propiedades que un hash no cubre por sí solo",
        [
            {"t": "Autenticidad", "k": "violeta", "b": [
                "El objeto es el que se dice que es.",
                "Procedencia, cadena de custodia y contexto de creación.",
                "Un hash no demuestra el origen.",
            ]},
            {"t": "Integridad", "k": "azul", "b": [
                "El objeto no cambió desde la adquisición.",
                "Hashes, copias y controles de acceso.",
                "Protege la copia; no interpreta el contenido.",
            ]},
            {"t": "Fiabilidad", "k": "verde", "b": [
                "El mecanismo que produjo el dato es adecuado a la pregunta.",
                "Incluye retención, reloj, sesgo y pruebas del método.",
                "Puede ser íntegro y, aun así, poco fiable para esa inferencia.",
            ]},
        ],
        "Figura 22.5. Tres preguntas. «El hash coincide» solo contesta la segunda.",
        [("Origen", "violeta"), ("Inalterado", "azul"), ("Apto", "verde")],
        accent="ambar",
    )

    flow(
        "figura22.6.png",
        "Incertidumbre que debe verse en la conclusión",
        "Cerrar un caso no es eliminar las reservas",
        [
            {"t": "Dato que falta", "k": "rosa", "b": [
                "Fuente no conservada o no autorizada.",
                "Se dice qué cambiaría si apareciera.",
            ]},
            {"t": "Hipótesis que sigue viva", "k": "ambar", "b": [
                "Explicación ordinaria no descartada.",
                "Se evita el adjetivo absoluto.",
            ]},
            {"t": "Límite del método", "k": "azul", "b": [
                "Herramienta, versión y cobertura.",
                "Resultados negativos con su alcance.",
            ]},
            {"t": "Revisión", "k": "verde", "b": [
                "Otra persona puede repetir la lectura.",
                "Las notas distinguen hecho y juicio.",
            ]},
        ],
        "Figura 22.6. Reservas. Ocultarlas en un anexo que nadie lee debilita el informe, no lo protege.",
        [("Falta", "rosa"), ("Rival", "ambar"), ("Método", "azul")],
        accent="ambar",
    )

    flow(
        "figura23.1.png",
        "Tres informes, tres lectores",
        "El mismo expediente no se resume con el mismo detalle para todos",
        [
            {"t": "Nota técnica", "k": "azul", "b": [
                "Hashes, rutas, versiones y consultas.",
                "Permite que otro analista repita el trabajo.",
                "No es todavía el dictamen.",
            ]},
            {"t": "Informe ejecutivo", "k": "ambar", "b": [
                "Pregunta, respuesta y límites en pocas páginas.",
                "Sin rutas crípticas como si fueran la conclusión.",
                "No esconde la incertidumbre para sonar decidido.",
            ]},
            {"t": "Informe pericial", "k": "verde", "b": [
                "Objeto, método, resultados y conclusiones separados.",
                "Lenguaje que un tribunal o un instructor puede seguir.",
                "Remite a los anexos sin mezclarlos con el juicio.",
            ]},
        ],
        "Figura 23.1. Destinatarios. Recortar tecnicismos no autoriza a subir el nivel de certeza.",
        [("Reproducción", "azul"), ("Decisión", "ambar"), ("Dictamen", "verde")],
        accent="azul",
    )

    layers(
        "figura23.2.png",
        "Esqueleto de un informe pericial",
        "El orden ayuda a no adelantar la conclusión",
        [
            {"t": "1. Identificación, objeto y alcance", "k": "pizarra", "b": "Quién encarga, qué se pregunta, qué queda fuera y qué autorización existe."},
            {"t": "2. Antecedentes y materiales", "k": "azul", "b": "Qué se recibió, con qué cadena de custodia, y cuál es el identificador de cada pieza."},
            {"t": "3. Metodología", "k": "teal", "b": "Qué se hizo, con qué medios, qué limitaciones tiene el método y qué no se hizo."},
            {"t": "4. Resultados", "k": "ambar", "b": "Observaciones, sin convertirlas todavía en la respuesta final."},
            {"t": "5. Discusión y conclusiones", "k": "verde", "b": "Hipótesis, contraste y respuesta a cada pregunta del objeto, con su reserva."},
            {"t": "6. Anexos", "k": "violeta", "b": "Hashes, registros de custodia, salidas relevantes y glosario mínimo."},
        ],
        "Figura 23.2. Orden expositivo. Los resultados no empiezan en la primera página disfrazados de antecedentes.",
        [("Hechos del encargo", "azul"), ("Hallazgos", "ambar"), ("Juicio", "verde")],
        accent="azul",
    )

    flow(
        "figura23.3.png",
        "Metodología que otro puede repetir",
        "Versiones, copias de trabajo y búsquedas negativas",
        [
            {"t": "Entrada", "k": "pizarra", "b": [
                "Identificador de la evidencia y hash de recepción.",
                "Herramienta, versión y parámetros relevantes.",
            ]},
            {"t": "Operación", "k": "azul", "b": [
                "Copia de trabajo, nunca el original si puede evitarse.",
                "Consulta o procedimiento descrito de forma concreta.",
            ]},
            {"t": "Salida", "k": "verde", "b": [
                "Resultado conservado, con su propio hash si es un derivado.",
                "Incluye lo buscado y no encontrado.",
            ]},
        ],
        "Figura 23.3. Trazabilidad mínima de un análisis. Sin ella, el anexo de hashes solo protege la recepción, no el trabajo posterior.",
        [("Entrada", "pizarra"), ("Operación", "azul"), ("Salida", "verde")],
        accent="azul",
    )

    flow(
        "figura23.4.png",
        "Resultados, cronología y conclusiones",
        "Tres bloques que el lector debe poder separar con un rotulador",
        [
            {"t": "Resultado", "k": "azul", "b": [
                "«En la copia X, el campo Y vale Z».",
                "Verbo de observación.",
                "Sin motivo ni identidad todavía.",
            ]},
            {"t": "Cronología", "k": "ambar", "b": [
                "Hechos ordenados con fuente y margen.",
                "Huecos visibles.",
                "Intervención del analista en otra capa.",
            ]},
            {"t": "Conclusión", "k": "verde", "b": [
                "Respuesta a la pregunta del objeto.",
                "Grado de apoyo y alternativa viva.",
                "Nada que no esté ya en los resultados.",
            ]},
        ],
        "Figura 23.4. Separación. Si la conclusión necesita un dato que no está en los resultados, falta un resultado, no un adjetivo.",
        [("Observación", "azul"), ("Tiempo", "ambar"), ("Respuesta", "verde")],
        accent="azul",
    )

    flow(
        "figura23.5.png",
        "Norma, anexo y cadena de custodia",
        "La cita normativa no sustituye al método descrito",
        [
            {"t": "Norma y buenas prácticas", "k": "violeta", "b": [
                "ISO/IEC 27037, 27041, 27042 y 27043 como marco.",
                "NIST SP 800-86 y documentos SWGDE según el tema.",
                "Se cita lo que de verdad se aplicó.",
            ]},
            {"t": "Anexos", "k": "azul", "b": [
                "Inventario, hashes, salidas y glosario.",
                "Lo voluminoso no se pega en el cuerpo.",
                "Cada anexo se numera y se referencia.",
            ]},
            {"t": "Custodia", "k": "verde", "b": [
                "De la recepción a la devolución o al archivo.",
                "Incluye copias de trabajo y quién las tuvo.",
                "Un hueco de custodia se declara, no se maquilla.",
            ]},
        ],
        "Figura 23.5. Soporte del dictamen. La cadena cubre también los derivados, porque de ellos salen las tablas del informe.",
        [("Marco", "violeta"), ("Anexo", "azul"), ("Custodia", "verde")],
        accent="azul",
    )

    flow(
        "figura23.6.png",
        "Defender el informe sin ampliarlo en la sala",
        "Lo que no está escrito no debería estrenarse en una respuesta oral",
        [
            {"t": "Preparar", "k": "azul", "b": [
                "Pregunta del objeto y frase de conclusión.",
                "Límite que se está dispuesto a repetir.",
                "Anexo donde está el dato bruto.",
            ]},
            {"t": "Distinguir", "k": "ambar", "b": [
                "Lo observado, lo inferido y lo que se ignora.",
                "No aceptar un resumen ajeno que suba la certeza.",
            ]},
            {"t": "Corregir", "k": "verde", "b": [
                "Si aparece un error, se documenta la corrección.",
                "Una versión nueva no se disimula.",
                "El hash del informe entregado queda registrado.",
            ]},
        ],
        "Figura 23.6. Presentación. La defensa explica el escrito; no lo sustituye por una versión más atrevida.",
        [("Preparación", "azul"), ("Límite", "ambar"), ("Corrección", "verde")],
        accent="azul",
    )

    flow(
        "figura24.1.png",
        "Caso integrado: del indicio al informe",
        "Litoral Media, S. L. Escenario ficticio usado a lo largo del capítulo",
        [
            {"t": "Indicio", "k": "ambar", "b": [
                "Alerta de un archivo comprimido en una estación.",
                "Aún no es una filtración.",
            ]},
            {"t": "Preservar", "k": "azul", "b": [
                "Estación, buzón, servidor, cuenta cloud y teléfono.",
                "Cada uno con su custodia.",
            ]},
            {"t": "Analizar", "k": "verde", "b": [
                "Fuentes separadas, hipótesis rivales.",
                "Correlación solo donde hay independencia.",
            ]},
            {"t": "Informar", "k": "violeta", "b": [
                "Respuesta por pregunta, con reservas.",
                "Nada que el expediente no sostenga.",
            ]},
        ],
        "Figura 24.1. Hilo del capítulo. Los cinco escenarios siguientes son tramos de un mismo encargo ficticio, no casos reales.",
        [("Indicio", "ambar"), ("Análisis", "verde"), ("Informe", "violeta")],
        accent="verde",
    )

    flow(
        "figura24.2.png",
        "Tramo Windows y tramo de correo",
        "Dos preguntas: qué ocurrió en la estación y qué autentica el mensaje",
        [
            {"t": "Estación", "k": "azul", "b": [
                "Ejecución de una utilidad y creación de un archivo.",
                "USB y red como hipótesis de salida, no como prueba cerrada.",
                "La cuenta de la sesión no es todavía la persona.",
            ]},
            {"t": "Correo", "k": "ambar", "b": [
                "Cabeceras, DMARC y adjunto con hash.",
                "El dominio autenticado puede ser el de la propia empresa.",
                "Eso no decide si el envío estaba autorizado.",
            ]},
            {"t": "Puente", "k": "verde", "b": [
                "¿El hash del adjunto es el hash del archivo de la estación?",
                "Si coincide, hay un vínculo de contenido.",
                "Si no coincide, no se fuerza la historia.",
            ]},
        ],
        "Figura 24.2. Primer puente del caso ficticio. El vínculo se hace por contenido e tiempo, no por el relato del mensaje.",
        [("Estación", "azul"), ("Mensaje", "ambar"), ("Contraste", "verde")],
        accent="verde",
    )

    flow(
        "figura24.3.png",
        "Tramo Linux y tramo cloud",
        "La cuenta del servidor y la clave de la nube pueden ser el mismo secreto o no serlo",
        [
            {"t": "Servidor", "k": "ambar", "b": [
                "Autenticación SSH y una unidad no prevista.",
                "Ejecución observada si el diario la conserva.",
                "Salida de red sin volumen identificado.",
            ]},
            {"t": "Nube", "k": "cielo", "b": [
                "Llamada a la API con un rol de automatización.",
                "Objeto escrito, si el registro de datos existe.",
                "Contenido aún no interpretado.",
            ]},
            {"t": "Límite", "k": "rosa", "b": [
                "No se unen los tramos solo porque ocurrieron el mismo día.",
                "Hace falta un identificador común o se declaran independientes.",
            ]},
        ],
        "Figura 24.3. Segundo puente. La simultaneidad es una hipótesis de trabajo, no una correlación suficiente.",
        [("Servidor", "ambar"), ("API", "cielo"), ("Reserva", "rosa")],
        accent="verde",
    )

    flow(
        "figura24.4.png",
        "Tramo móvil e IoT",
        "El teléfono y la cámara pueden situar actividad; no identifican por sí solos",
        [
            {"t": "Teléfono", "k": "violeta", "b": [
                "Copia o extracción descrita con su cobertura.",
                "Mensaje o foto relevantes, con su límite.",
            ]},
            {"t": "Cámara y router", "k": "verde", "b": [
                "Evento de movimiento y concesión de red.",
                "Relojes con desfase documentado.",
            ]},
            {"t": "Lectura", "k": "ambar", "b": [
                "Compatibilidad temporal con el resto del caso.",
                "Sin identificar a la persona que aparece o que porta el teléfono.",
            ]},
        ],
        "Figura 24.4. Tercer puente del escenario ficticio. La correlación temporal se expresa con el margen de error de la peor fuente.",
        [("Móvil", "violeta"), ("IoT", "verde"), ("Margen", "ambar")],
        accent="verde",
    )

    flow(
        "figura24.5.png",
        "Matriz de hipótesis del encargo completo",
        "Cada fila debe poder sobrevivir si las demás se caen",
        [
            {"t": "Filtración deliberada", "k": "rosa", "b": [
                "Exige contenido, salida y atribución.",
                "En el escenario, alguna de las tres queda corta.",
                "No se afirma como hecho cerrado.",
            ]},
            {"t": "Envío autorizado mal documentado", "k": "azul", "b": [
                "Compatible con dominio propio y cuenta corporativa.",
                "Falta la política o el ticket que lo autorizaría.",
                "Permanece abierta.",
            ]},
            {"t": "Compromiso de credencial", "k": "ambar", "b": [
                "Compatible con orígenes nuevos en SSH y en la API.",
                "No hay prueba del modo en que se copió el secreto.",
                "Se informa como hipótesis apoyada, no como modo operandi cerrado.",
            ]},
        ],
        "Figura 24.5. Hipótesis rivales del caso ficticio. El capítulo las mantiene hasta la revisión final del informe.",
        [("No cerrada", "rosa"), ("Abierta", "azul"), ("Apoyada", "ambar")],
        accent="verde",
    )

    flow(
        "figura24.6.png",
        "Revisión crítica antes de entregar",
        "Lista de defectos que este capítulo enseña a buscar en el propio informe",
        [
            {"t": "Certeza de más", "k": "rosa", "b": [
                "Adjetivos que no están en los resultados.",
                "Persona donde solo hay una cuenta.",
            ]},
            {"t": "Fuente única", "k": "ambar", "b": [
                "Un tramo entero apoyado en un solo registro.",
                "La segunda herramienta contada como segunda fuente.",
            ]},
            {"t": "Hueco oculto", "k": "azul", "b": [
                "Retención, reloj o cobertura que no aparecen.",
                "Peticiones al proveedor que nadie hizo.",
            ]},
            {"t": "Se puede entregar", "k": "verde", "b": [
                "Preguntas respondidas al nivel que las pruebas permiten.",
                "Anexos y custodia alineados con el texto.",
            ]},
        ],
        "Figura 24.6. Última lectura. El informe sale cuando sobrevive a esta revisión, no cuando suena completo.",
        [("Defecto", "rosa"), ("Hueco", "azul"), ("Listo", "verde")],
        accent="verde",
    )


if __name__ == "__main__":
    build_all()
    print("figuras escritas en", OUT)
