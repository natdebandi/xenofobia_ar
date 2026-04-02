import html as htmllib
import unicodedata
from IPython.display import display, HTML
from pathlib import Path

# ── Variable: noticia con temática COVID ──────────────────────────────────────
# Detecta si el título o resumen de la noticia contiene alguna palabra clave.
# El flag se propaga a todos los comentarios de esa noticia (nivel fila del df).

PALABRAS_COVID = [
    'coronavirus', 'covid', 'wuhan', 'cuarentena', 'normalidad',
    'aislamiento', 'encierro', 'fase', 'infectados', 'distanciamiento',
    'fiebre', 'sintomas',          # sin tilde para cubrir ambas grafías
]

def _normalizar(s):
    """Minúsculas + elimina tildes para comparación robusta."""
    if not isinstance(s, str):
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', s.lower())
        if unicodedata.category(c) != 'Mn'
    )

_patron_covid = r'\b(' + '|'.join(PALABRAS_COVID) + r')\b'

df['covid'] = (
    df['title'].map(_normalizar).str.contains(_patron_covid, regex=True, na=False) |
    df['resumen'].map(_normalizar).str.contains(_patron_covid, regex=True, na=False)
).astype(int)

_n_noticias_covid = df.groupby('tweet_id_noticia')['covid'].max().sum()
_n_noticias_total = df['tweet_id_noticia'].nunique()
_n_comentarios_covid = df['covid'].sum()
print(f"covid=1 → {_n_noticias_covid:,} noticias de {_n_noticias_total:,} "
      f"({_n_noticias_covid/_n_noticias_total:.1%})")
print(f"         {_n_comentarios_covid:,} comentarios de {len(df):,} "
      f"({_n_comentarios_covid/len(df):.1%})")

# ── Selección de noticia representativa (top en comentarios RACISM) ──────────
candidatas = (
    df[df['RACISM'] == 1]
    .groupby(['tweet_id_noticia', 'medio', 'title', 'resumen'])
    .size()
    .reset_index(name='n_racism')
    .query('n_racism >= 5')
    .sort_values('n_racism', ascending=False)
)

# Índice 2 para tener variedad (cambiar por 0, 1, 3... para ver otras noticias)
row = candidatas.iloc[2]
tweet_id  = row['tweet_id_noticia']
medio     = row['medio']
titulo    = htmllib.escape(str(row['title']))
resumen   = htmllib.escape(str(row['resumen'])[:300])

todos = df[df['tweet_id_noticia'] == tweet_id].copy()
fecha_str         = todos['date_tweet'].min().strftime('%d %b %Y')
total_comentarios = len(todos)
n_racism          = row['n_racism']

# 1 comentario SIN odio (ninguna categoría activa) y 4 CON RACISM=1
cats = list(CATEGORIAS.keys()) if 'CATEGORIAS' in dir() else [
    'RACISM','CALLS','WOMEN','LGBTI','CLASS','POLITICS','DISABLED','APPEARANCE','CRIMINAL'
]
sin_odio_pool = todos[todos[cats].sum(axis=1) == 0]
sin_odio = sin_odio_pool.head(1)   # 1 comentario neutro

odiosos = todos[todos['RACISM'] == 1].head(4)

url_tweet = f"https://twitter.com/{medio}/status/{tweet_id}"

# ── Badges de categorías ─────────────────────────────────────────────────────
CATEGORIAS = {
    'RACISM':     ('#c0392b', 'Xenofobia / Racismo'),
    'CALLS':      ('#922b21', 'Llamado a violencia'),
    'WOMEN':      ('#884ea0', 'Odio a mujeres'),
    'LGBTI':      ('#1a5276', 'Odio LGBTI+'),
    'CLASS':      ('#1e8449', 'Odio por clase social'),
    'POLITICS':   ('#d4ac0d', 'Odio político'),
    'DISABLED':   ('#2471a3', 'Odio a discapacidad'),
    'APPEARANCE': ('#ca6f1e', 'Odio por apariencia'),
    'CRIMINAL':   ('#5d6d7e', 'Estigma criminal'),
}

def make_badges(c_row):
    badges = ''
    for col, (color, label) in CATEGORIAS.items():
        if c_row.get(col, 0) == 1:
            badges += (f'<span style="background:{color};color:white;'
                       f'padding:2px 8px;border-radius:10px;font-size:11px;'
                       f'margin-right:4px;">{label}</span>')
    return badges or '<span style="color:#aaa;font-size:11px;">sin etiqueta</span>'

# ── Nombres legibles de medios ────────────────────────────────────────────────
NOMBRES = {
    'clarincom': 'Clarín', 'LANACION': 'La Nación', 'infobae': 'Infobae',
    'pagina12': 'Página 12', 'cronica': 'Crónica', 'perfilcom': 'Perfil',
    'laderechamedios': 'La Derecha Medios', 'laderechadiario': 'La Derecha Diario',
    'izquierdadiario': 'Izquierda Diario',
}
nombre_medio = NOMBRES.get(medio, medio)

# ── Comentario sin odio (primero, en verde) ───────────────────────────────────
neutro_html = ''
for _, c in sin_odio.iterrows():
    texto   = htmllib.escape(str(c['text'])[:280])
    fecha_c = c['date_tweet'].strftime('%d %b %Y %H:%M')
    neutro_html += f"""
    <div style="margin:10px 0 10px 36px; padding:12px 15px; background:#fff;
                border-left:3px solid #27ae60; border-radius:6px;
                box-shadow:0 1px 3px rgba(0,0,0,0.08);">
      <div style="font-size:12px; color:#888; margin-bottom:6px;">
        💬 Usuario anónimo · {fecha_c}
      </div>
      <div style="font-size:14px; color:#222; line-height:1.6;">
        {texto}
      </div>
      <div style="margin-top:8px;">
        <span style="background:#27ae60;color:white;padding:2px 8px;
                     border-radius:10px;font-size:11px;">Sin odio</span>
      </div>
    </div>"""

# ── Bloque de comentarios con odio ───────────────────────────────────────────
comentarios_html = ''
for _, c in odiosos.iterrows():
    texto  = htmllib.escape(str(c['text'])[:280])
    fecha_c = c['date_tweet'].strftime('%d %b %Y %H:%M')
    comentarios_html += f"""
    <div style="margin:10px 0 10px 36px; padding:12px 15px; background:#fff;
                border-left:3px solid #e74c3c; border-radius:6px;
                box-shadow:0 1px 3px rgba(0,0,0,0.08);">
      <div style="font-size:12px; color:#888; margin-bottom:6px;">
        💬 Usuario anónimo · {fecha_c}
      </div>
      <div style="font-size:14px; color:#222; line-height:1.6;">
        {texto}
      </div>
      <div style="margin-top:8px;">
        {make_badges(c)}
      </div>
    </div>"""

# ── Contenido principal ───────────────────────────────────────────────────────
contenido = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif; max-width:700px; margin:20px auto;">

  <!-- Encabezado explicativo -->
  <div style="background:#e8f4fd; border-radius:8px; padding:10px 16px;
              margin-bottom:16px; font-size:13px; color:#2471a3; line-height:1.6;">
    <strong>Estructura del dataset</strong><br>
    Cada fila representa un <em>comentario</em> asociado a una <em>noticia</em> publicada
    por un medio en Twitter/X. Esta noticia recibió
    <strong>{total_comentarios:,} comentarios</strong>,
    de los cuales <strong>{n_racism} fueron clasificados como xenofobia/racismo</strong>.
    Se muestra 1 comentario sin odio (en verde) y 4 con xenofobia/racismo (en rojo).
  </div>

  <!-- Tweet del medio (noticia) -->
  <div style="background:#f7f9fa; border:1px solid #dce1e7; border-radius:12px;
              padding:18px 20px;">

    <!-- Cabecera usuario -->
    <div style="display:flex; align-items:center; margin-bottom:12px;">
      <div style="width:42px; height:42px; background:#1da1f2; border-radius:50%;
                  display:flex; align-items:center; justify-content:center;
                  color:white; font-weight:bold; font-size:17px; margin-right:12px;
                  flex-shrink:0;">
        {nombre_medio[0]}
      </div>
      <div>
        <div style="font-weight:700; font-size:14px; color:#14171a;">{nombre_medio}</div>
        <div style="font-size:12px; color:#657786;">@{medio} · {fecha_str}</div>
      </div>
      <div style="margin-left:auto;">
        <span style="background:#1da1f2; color:white; font-size:11px;
                     padding:3px 9px; border-radius:12px;">NOTICIA</span>
      </div>
    </div>

    <!-- Texto del tweet -->
    <div style="font-size:15px; color:#14171a; line-height:1.65; margin-bottom:12px;">
      {resumen}
    </div>

    <!-- Card título noticia -->
    <div style="border:1px solid #dce1e7; border-radius:10px; padding:12px 15px;
                background:white; margin-bottom:12px;">
      <div style="font-size:10px; color:#aaa; text-transform:uppercase;
                  letter-spacing:.5px; margin-bottom:5px;">Título</div>
      <div style="font-size:14px; font-weight:600; color:#14171a; line-height:1.45;">
        {titulo}
      </div>
    </div>

    <!-- Enlace -->
    <div style="font-size:13px;">
      <a href="{url_tweet}" target="_blank"
         style="color:#1da1f2; text-decoration:none;">
        🔗 Ver tweet original en Twitter/X →
      </a>
    </div>
  </div>

  <!-- Separador de hilo -->
  <div style="margin:8px 0 4px 18px; color:#aaa; font-size:12px;">
    ↳ {total_comentarios:,} respuestas en total —
    mostrando 1 sin odio + {len(odiosos)} con xenofobia/racismo
  </div>

  <!-- Comentario sin odio (primero) -->
  {neutro_html}

  <!-- Comentarios con odio -->
  {comentarios_html}

</div>
"""

# ── Mostrar en notebook ───────────────────────────────────────────────────────
display(HTML(contenido))

# ── Exportar a HTML standalone (fondo blanco, listo para abrir en browser) ───
html_standalone = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ejemplo de comentarios — {nombre_medio}</title>
  <style>
    body {{ background: #ffffff; margin: 0; padding: 20px; }}
  </style>
</head>
<body>
{contenido}
</body>
</html>"""

output_path = Path('outputs/ejemplo_comentarios.html')
output_path.parent.mkdir(exist_ok=True)
output_path.write_text(html_standalone, encoding='utf-8')
print(f"✓ Exportado a: {output_path.resolve()}")
