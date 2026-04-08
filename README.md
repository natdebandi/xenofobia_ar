# Xenofobia en redes sociales durante la pandemia de COVID-19 en Argentina

**Autora:** Natalia Debandi
**Contexto:** Proyecto PIUBAMAS / Artículo en Revista PERIPLOS

Análisis de discursos xenófobos y discriminatorios en Twitter/X durante la pandemia de COVID-19 en Argentina, con foco en el DNU 70/2017 (decreto de Macri sobre migraciones) y su derogación en marzo de 2021.

---

## Dataset

El dataset base es `tweets_medios_arg.csv`, disponible en [HuggingFace — PIUBAMAS](https://huggingface.co/datasets/piubamas/tweets_medios_arg), que contiene comentarios de usuarios a noticias publicadas por medios argentinos en Twitter/X durante 2020–2021.

Cada fila representa un **comentario** asociado a una **noticia** de un medio. Las columnas de clasificación (`HATEFUL`, `RACISM`, `CALLS`, `WOMEN`, `LGBTI`, `CLASS`, `POLITICS`, `DISABLED`, `APPEARANCE`, `CRIMINAL`) fueron generadas con distintos clasificadores de discurso de odio.

El subconjunto **DNU** (`piubamas_dnu_v2.csv`) filtra noticias cuyo título menciona palabras clave vinculadas al DNU 70/2017 y a migraciones.

---

## Notebooks

| Notebook | Descripción |
|---|---|
| `1_CREATE_PIUBA_DNU.ipynb` | Construye el subconjunto DNU a partir del dataset completo, aplicando filtros por palabras clave |
| `1_PIUBA_DEA_2.ipynb` | EDA principal: descripción del dataset, análisis del dataset DNU, series temporales de odio y racismo, nubes de palabras, ejemplos de noticias discriminatorias |
| `2_DNU_EDA.ipynb` | EDA extendido del dataset DNU con cobertura temporal y clasificación de tweets |
| `2_DNU_EDA_Clasif.ipynb` | Comparación de seis clasificadores de discurso de odio aplicados al dataset DNU (análisis de acuerdo, solapamiento, series temporales) |

---

## Estructura del repositorio

```
xenofobia_ar/
├── 1_CREATE_PIUBA_DNU.ipynb
├── 1_PIUBA_DEA_2.ipynb
├── 2_DNU_EDA.ipynb
├── 2_DNU_EDA_Clasif.ipynb
│
├── data/                  # (local, no versionado) CSVs del dataset
├── data_original/         # (local, no versionado) datos crudos originales
├── DNU_data/              # (local, no versionado) datos intermedios DNU
├── outputs/               # (local, no versionado) imágenes y HTMLs generados
│
├── V1_belu/               # (local) versiones anteriores — exploración inicial
├── V2_create/             # (local) versiones anteriores — construcción del dataset
├── V3_clasificar/         # (local) versiones anteriores — clasificación
└── Relmecs/               # (local) versión para congreso RELMECS
```

---

## Clasificadores comparados

| Clasificador | Modelo base |
|---|---|
| BETO-hate | BETO fine-tuned (hate speech ES) |
| pysentimiento | RoBERTa fine-tuned (hate speech ES) |
| GPT-4o (zero-shot) | OpenAI GPT-4o |
| GPT-4o (fine-tuned) | GPT-4o fine-tuned sobre datos PIUBAMAS |
| HF-hate-es | Modelos de HuggingFace para odio en español |

---

## Contexto histórico

El **DNU 70/2017** fue un decreto del presidente Macri que endureció las condiciones de expulsión de migrantes en Argentina, generando un pico de discurso xenófobo en redes sociales. Fue derogado el **5 de marzo de 2021** bajo el gobierno de Alberto Fernández, lo que generó un nuevo ciclo de debate público analizado en este trabajo.
