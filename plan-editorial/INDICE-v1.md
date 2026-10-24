# ANÁLISIS FORENSE INFORMÁTICO

*Metodologías, adquisición de evidencias, investigación digital y elaboración de informes periciales*

## PARTE I. FUNDAMENTOS, METODOLOGÍA Y ADQUISICIÓN DE EVIDENCIAS

### Capítulo 1. Introducción al análisis forense digital
1. Concepto, objetivos y aplicaciones de la informática forense.
2. Investigación judicial, corporativa y respuesta a incidentes.
3. Evidencias digitales: características, valor y limitaciones.
4. Fuentes de evidencia y responsabilidades del analista.

### Capítulo 2. Metodologías y estándares de investigación
1. Planificación y alcance de una investigación.
2. Fases del proceso forense.
3. Normas ISO/IEC, recomendaciones NIST y buenas prácticas SWGDE.
4. Hipótesis, reproducibilidad y validación de resultados.
5. Preparación forense (*forensic readiness*).

### Capítulo 3. Marco legal, responsabilidad y ética profesional
1. Autorización y legitimidad de una investigación.
2. Tratamiento de evidencias en investigaciones judiciales y corporativas.
3. Protección de datos y privacidad.
4. Jurisdicción y obtención de evidencias.
5. Ética, imparcialidad y responsabilidad profesional.

### Capítulo 4. La escena digital y la cadena de custodia
1. Identificación y aseguramiento de la escena.
2. Inventario y documentación de dispositivos.
3. Intervención sobre equipos encendidos y apagados.
4. Orden de volatilidad y conservación de evidencias.
5. Cadena de custodia, embalaje y almacenamiento.

### Capítulo 5. Adquisición de evidencias y verificación de integridad
1. Adquisición física, lógica y remota.
2. Bloqueadores de escritura.
3. Imágenes forenses y sus formatos.
4. Hashes y comprobación de integridad.
5. Particularidades de HDD, SSD, cifrado y sistemas dañados.
6. Documentación del procedimiento de adquisición.

### Capítulo 6. Preparación del laboratorio forense
1. Equipamiento físico y virtual.
2. Estaciones de trabajo y almacenamiento de evidencias.
3. Herramientas forenses libres y comerciales.
4. Validación de herramientas.
5. Automatización, trazabilidad y reproducción de análisis.
6. Preparación de escenarios prácticos.

---

## PARTE II. ANÁLISIS FORENSE DE EQUIPOS Y SISTEMAS OPERATIVOS

### Capítulo 7. Discos, particiones y sistemas de archivos
1. Estructura de los soportes de almacenamiento.
2. Particiones MBR y GPT.
3. Sistemas de archivos: FAT, exFAT, NTFS, ext4 y APFS.
4. Metadatos y marcas temporales.
5. Análisis de archivos eliminados y espacio no asignado.
6. Recuperación y limitaciones de los resultados.

### Capítulo 8. Análisis forense de Windows
1. Principales fuentes de evidencia.
2. Registro de Windows y perfiles de usuario.
3. Registros de eventos y mecanismos de persistencia.
4. Artefactos de ejecución: Prefetch, Amcache, Shimcache y otros.
5. Actividad del usuario, archivos y dispositivos USB.
6. Investigación práctica de un equipo Windows.

### Capítulo 9. Análisis forense de Linux
1. Estructura y fuentes de información.
2. Logs del sistema y autenticación.
3. Usuarios, permisos, sesiones SSH y privilegios.
4. Historial de comandos y actividad de procesos.
5. Servicios, tareas programadas y persistencia.
6. Investigación práctica de un servidor Linux.

### Capítulo 10. Análisis forense de macOS
1. Arquitectura del sistema y APFS.
2. Cifrado, instantáneas y protecciones.
3. Unified Logs y FSEvents.
4. Actividad de usuarios y aplicaciones.
5. Artefactos relevantes y limitaciones de adquisición.
6. Caso práctico.

### Capítulo 11. Análisis de memoria y evidencias volátiles
1. Memoria RAM como fuente de evidencia.
2. Técnicas y herramientas de adquisición.
3. Análisis con Volatility 3.
4. Procesos, conexiones y módulos.
5. Identificación de actividad sospechosa en memoria.
6. Correlación con las evidencias del disco.

### Capítulo 12. Registros y reconstrucción de líneas temporales
1. Naturaleza y fiabilidad de los logs.
2. Marcas temporales, zonas horarias y sincronización.
3. Extracción y normalización de eventos.
4. Construcción de líneas temporales.
5. Plaso, Timesketch y herramientas relacionadas.
6. Correlación e interpretación de acontecimientos.

---

## PARTE III. REDES, APLICACIONES Y ACTIVIDAD MALICIOSA

### Capítulo 13. Análisis forense de redes
1. Evidencias de red y fuentes de información.
2. Captura y preservación del tráfico.
3. Análisis de paquetes con Wireshark.
4. DNS, HTTP, TLS y otros protocolos relevantes.
5. Logs de firewalls, proxies, routers y VPN.
6. Reconstrucción de comunicaciones sospechosas.

### Capítulo 14. Navegadores, correo electrónico y aplicaciones
1. Historiales y artefactos de navegadores.
2. Análisis forense de correo electrónico y cabeceras.
3. SPF, DKIM, DMARC y trazabilidad de mensajes.
4. Adjuntos, enlaces y metadatos.
5. Artefactos de aplicaciones y mensajería.
6. Investigación práctica de un correo sospechoso.

### Capítulo 15. Datos borrados, cifrado y técnicas antiforenses
1. Borrado de información y recuperación.
2. Técnicas de *file carving*.
3. Cifrado de discos, archivos y aplicaciones.
4. Ocultación de información.
5. Manipulación de evidencias y marcas temporales.
6. Detección y límites técnicos de las técnicas antiforenses.

### Capítulo 16. Análisis forense de sistemas comprometidos y malware
1. Indicadores de compromiso.
2. Evidencias de ejecución y persistencia.
3. Análisis básico de archivos sospechosos.
4. Análisis estático y dinámico en entornos seguros.
5. Correlación entre memoria, disco, procesos y tráfico.
6. Reconstrucción de una intrusión.

---

## PARTE IV. ANÁLISIS FORENSE EN ENTORNOS ESPECIALIZADOS

### Capítulo 17. Análisis forense de dispositivos Android
1. Arquitectura y mecanismos de seguridad.
2. Preservación del dispositivo.
3. Técnicas de extracción de datos.
4. Artefactos de aplicaciones y comunicaciones.
5. Bases de datos, geolocalización y actividad del usuario.
6. Interpretación de evidencias e informe.

### Capítulo 18. Análisis forense de dispositivos iOS y iPadOS
1. Arquitectura y protección de datos.
2. Preservación y adquisición.
3. Copias de seguridad y sus limitaciones.
4. Análisis de aplicaciones, comunicaciones y actividad.
5. Validación de resultados.
6. Caso práctico.

### Capítulo 19. Análisis forense en la nube
1. Modelos y arquitecturas Cloud.
2. Retos técnicos, organizativos y jurídicos.
3. Preparación forense y conservación de registros.
4. Investigación en AWS, Azure y Google Cloud.
5. Identidades, API, almacenamiento y servicios SaaS.
6. Reconstrucción de incidentes.
7. Caso práctico en un entorno cloud.

### Capítulo 20. Virtualización, contenedores y entornos orquestados
1. Evidencias en hipervisores y máquinas virtuales.
2. Discos virtuales, instantáneas y registros.
3. Análisis forense de Docker.
4. Investigación en Kubernetes.
5. Adquisición y preservación de evidencias.
6. Caso práctico.

### Capítulo 21. Análisis forense de dispositivos IoT
1. Arquitectura y ecosistemas IoT.
2. Identificación y preservación de dispositivos.
3. Firmware, memoria, registros y almacenamiento.
4. Redes, protocolos y servicios asociados.
5. Cámaras, routers, sensores y dispositivos domóticos.
6. Reconstrucción de acontecimientos y líneas temporales.
7. Caso práctico de investigación IoT.

---

## PARTE V. INTERPRETACIÓN, INFORMES Y CASOS COMPLETOS

### Capítulo 22. Interpretación de evidencias y reconstrucción de los hechos
1. Diferencia entre artefacto, indicio, evidencia e interpretación.
2. Formulación y contraste de hipótesis.
3. Correlación de fuentes independientes.
4. Reconstrucción cronológica.
5. Evaluación de autenticidad, integridad y fiabilidad.
6. Incertidumbre, límites y revisión de conclusiones.

### Capítulo 23. Informes forenses y presentación de conclusiones
1. Informes técnicos, ejecutivos y periciales.
2. Identificación, objeto, alcance y antecedentes.
3. Metodología y evidencias analizadas.
4. Resultados, cronología y conclusiones.
5. Normativa aplicable y referencias.
6. Anexos, documentación y cadena de custodia.
7. Presentación y defensa de un informe pericial.
8. Ejemplo completo comentado.

### Capítulo 24. Investigaciones completas: del indicio al informe
1. Investigación de un equipo Windows.
2. Análisis de un correo fraudulento y posible filtración de datos.
3. Investigación de un servidor Linux comprometido.
4. Investigación de una cuenta cloud.
5. Correlación de evidencias móviles e IoT.
6. Elaboración y revisión crítica de los informes finales.

---

## MATERIAL COMPLEMENTARIO

**Anexo A.** Listas de comprobación de procedimientos forenses.

**Anexo B.** Plantillas de adquisición, inventario, cadena de custodia e informes.

**Anexo C.** Herramientas y recursos especializados.

**Anexo D.** Guía de laboratorios y evidencias prácticas.

**Glosario de términos y acrónimos.**

**Bibliografía y referencias normativas.**

**Índice analítico alfabético.**