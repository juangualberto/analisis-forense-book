---
title: Introducción al Análisis Forense
subtitle: Guía para Peritos e Ingenieros 
author: Juan Gualberto Gutiérrez Marín
lang: "es"
keywords: [DFIR, Respuesta a Incidentes, Análisis Forense, Ciberseguridad, OSINT]

titlepage: true
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "360049"
titlepage-background: "figuras/cover.png"

latex_engine: xelatex
toc: false
toc-depth: 2
geometry:
  - paperwidth=17.78cm
  - paperheight=25.4cm
  - top=1.5cm
  - bottom=1.5cm
  - inner=2.5cm
  - outer=2cm
  - twoside
  - includehead
  - includefoot

fontsize: 10pt
---

\pagestyle{empty}

\newpage
\thispagestyle{empty}

\vspace*{\fill}

> **Nota para la edición digital.** Este libro contiene numerosos enlaces y referencias web pensados para consultarse desde un lector de PDF. En la versión impresa, los enlaces siguen apareciendo como referencia y se complementan con la bibliografía incluida en los capítulos.

\vspace*{\fill}

\newpage
\thispagestyle{empty}

\section*{Licencia}
**© 2026 Juan Gualberto Gutiérrez Marín.**

**Tras la Brecha.** Primera edición, 2026.

Obra autopublicada mediante Amazon Kindle Direct Publishing (KDP).

El contenido original de esta obra se distribuye bajo la licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

Se permite copiar, compartir, redistribuir y adaptar el contenido con fines no comerciales, siempre que se reconozca adecuadamente la autoría, se indiquen las modificaciones realizadas y las adaptaciones se distribuyan bajo la misma licencia.

**Los derechos de explotación comercial quedan reservados al autor.** La reproducción, distribución, venta o explotación comercial de esta obra por terceros requiere autorización previa y expresa de su titular.

La edición comercial disponible mediante Amazon Kindle Direct Publishing (KDP) se publica por autorización del propio autor, titular de los derechos.

Licencia completa: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es

Las marcas, logotipos, capturas, citas y demás materiales pertenecientes a terceros conservan sus correspondientes derechos y condiciones de uso.

\begingroup
\setkeys{Gin}{keepaspectratio}

![Atribución-CompartirIgual (CC BY-SA 4.0)](figuras/licencia.png){width=4.5cm}

\endgroup

Página del autor: <https://juangualberto.github.io>.

\newpage
\thispagestyle{empty}

\section*{Sobre el autor}

**Juan Gualberto Gutiérrez Marín** es profesor de Informática y cuenta con **más de veintidós años de experiencia docente**. Su trayectoria se ha desarrollado principalmente en la enseñanza de tecnologías de la información, programación, sistemas, redes y ciberseguridad, combinando la docencia técnica con el diseño de materiales y laboratorios orientados a situaciones reales.

Ha desarrollado también parte de su experiencia profesional en **Estados Unidos**, lo que ha contribuido a una visión de la tecnología y de la formación técnica conectada con distintos entornos profesionales y educativos.

Además de su actividad en Formación Profesional, ha impartido docencia universitaria en la **Universidad de Jaén**, tanto en titulaciones del ámbito de la Ingeniería Informática como en formación de posgrado. En el **Máster de Seguridad Informática de la Universidad de Jaén** ha impartido la asignatura **Análisis de Software**, vinculada al estudio técnico del comportamiento de programas y a la seguridad.

Su trabajo docente actual presta especial atención a la **ciberseguridad defensiva, DFIR, respuesta a incidentes, análisis forense, administración de sistemas, redes, cloud y automatización**. En sus materiales intenta conectar los fundamentos con la práctica profesional: entender qué ocurre en un sistema, qué evidencias deja una acción, cómo detectarla y cómo responder de manera proporcionada.

Este libro nace de ese enfoque. No pretende presentar la ciberseguridad como una colección de herramientas aisladas, sino como un proceso en el que tecnología, procedimientos, investigación y toma de decisiones deben funcionar conjuntamente.

\newpage
\thispagestyle{empty}

\vspace*{\fill}

\begin{center}

{\Large\itshape "In mathematics, all can be found in the computer; everything we know or have found out in twenty thousand years. In history, that’s not so. Historians pick and choose and every one of them picks and chooses the same thing."}

\vspace{1.2cm}

{\large Hari Seldon}\\
{\itshape Isaac Asimov, Prelude to Foundation } (1988) 

\end{center}

\vspace*{\fill}

\newpage
\pagestyle{empty}
\thispagestyle{empty}

\setcounter{tocdepth}{2}
\tableofcontents
\clearpage

\pagestyle{eisvogel-header-footer}

\clearpairofpagestyles

\lehead{\pagemark}
\rehead{\small\itshape Incidentes de Ciberseguridad}
\lohead{\small\leftmark}
\rohead{\pagemark}

\lefoot{}
\refoot{}
\lofoot{}
\rofoot{}
\cfoot{}

\KOMAoptions{headsepline=true}
\KOMAoptions{footsepline=false}

\renewcommand{\sectionmark}[1]{\markboth{#1}{}}

\AddToHook{cmd/section/before}{\cleardoublepage}

