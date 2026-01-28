import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from urllib.parse import quote

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CARPETA_SALIDA = os.path.join(CARPETA_ACTUAL, 'reportes_scouting')
if not os.path.exists(CARPETA_SALIDA): os.makedirs(CARPETA_SALIDA)

def convertir_ruta_a_uri(ruta):
    """Convierte una ruta local de Windows a file:// URI o devuelve URL si ya es http/https"""
    if pd.isna(ruta) or ruta == '':
        return ''
    ruta_str = str(ruta)
    # Si ya es una URL, devolverla tal cual
    if ruta_str.startswith(('http://', 'https://')):
        return ruta_str
    # Convertir ruta de Windows a file:// URI
    path = Path(ruta_str).resolve()
    return path.as_uri()

# Configuración Gráfica
COLOR_GOLD = '#EAB308'
COLOR_BG = '#0f1115'

def crear_radar_pro(stats_valores, stats_nombres, nombre_archivo):
    # Lógica circular para cerrar el gráfico
    valores = stats_valores + stats_valores[:1]
    angulos = np.linspace(0, 2 * np.pi, len(stats_valores), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor(COLOR_BG)
    ax.patch.set_alpha(0.6)

    # Dibujar
    ax.plot(angulos, valores, color=COLOR_GOLD, linewidth=2)
    ax.fill(angulos, valores, color=COLOR_GOLD, alpha=0.35)

    # Etiquetas de los ejes (Las métricas específicas)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(stats_nombres, color='white', size=9, fontfamily='sans-serif', weight='bold')
    
    # Limpiar ejes radiales (0, 20, 40...)
    ax.set_yticklabels([])
    ax.set_ylim(0, 100)
    
    # Grid sutil
    ax.grid(color='#555', linestyle=':', linewidth=0.8)
    ax.spines['polar'].set_visible(False)

    plt.savefig(os.path.join(CARPETA_SALIDA, nombre_archivo), format='png', bbox_inches='tight', transparent=True)
    plt.close()
    return nombre_archivo

# --- PROCESO ---
import sys
df = pd.read_excel('datos_scouting.xlsx').fillna('')
env = Environment(loader=FileSystemLoader(CARPETA_ACTUAL))
plantilla = 'plantilla.html'  # Por defecto azul
color_tag = 'azul'
if len(sys.argv) > 1 and sys.argv[1].lower() == 'verde':
    plantilla = 'plantilla_verde.html'
    color_tag = 'verde'
template = env.get_template(plantilla)

# Nombres profesionales para las puntas del gráfico
LABELS_GRAFICO = ['DUELOS %', 'AÉREO', 'PROGRESIÓN', 'REGATE', 'RECUP.', 'GOL ESP. (xG)']

for i, fila in df.iterrows():
    print(f"Generando reporte para: {fila['Apellido']}")
    
    # 1. Datos para gráfico (Los SCORES 0-100)
    valores = [
        fila['Sc_Duelos_Ganados'], fila['Sc_Juego_Aereo'], fila['Sc_Pases_Prog'],
        fila['Sc_Regates'], fila['Sc_Recuperaciones'], fila['Sc_Goles_Esperados']
    ]
    img_name = f"radar_{fila['Apellido']}.png"
    crear_radar_pro(valores, LABELS_GRAFICO, img_name)

    # 2. Procesar listas (Fortalezas / Trayectoria)
    fortalezas = str(fila.get('Fortalezas', '')).split('|') if fila.get('Fortalezas') else []
    debilidades = str(fila.get('Debilidades', '')).split('|') if fila.get('Debilidades') else []
    
    trayectoria = []
    for k in ['Trayectoria_1', 'Trayectoria_2', 'Trayectoria_3']:
        if fila[k]:
            p = str(fila[k]).split('|')
            if len(p) == 4: trayectoria.append({'temp': p[0], 'club': p[1], 'pj': p[2], 'goles': p[3]})

    # 3. Datos HTML
    datos = {
        'nombre': fila['Nombre'], 'apellido': fila['Apellido'], 'posicion': fila['Posicion'],
        'foto_url': convertir_ruta_a_uri(fila['Foto_URL']), 'nacionalidad': fila['Nacionalidad'],
        'edad': fila['Edad'], 'altura': fila['Altura'], 'pie': fila['Pie'],
        'club': fila['Club_Actual'], 'contrato': fila['Contrato_Hasta'],
        'escudo_url': convertir_ruta_a_uri(fila.get('Escudo_Club', '')),
        'salario': fila.get('Salario_Actual', 'N/A'), 'valor': fila['Valor_Mercado'], 'video_url': fila['Video_URL'],
        'instagram_url': fila.get('IG_URL', ''),
        'tm_url': fila.get('TM_URL', ''),
        'chart_path': img_name,
        'fortalezas': fortalezas, 'debilidades': debilidades, 'trayectoria': trayectoria,
        # Datos extra para mostrar debajo del gráfico
        'dato_duelos': fila['Dato_Duelos'], 
        'dato_pases': str(fila.get('Min_jugados', '0')).split('/')[0],
        'dato_pases_percent': (float(str(fila.get('Min_jugados', '0')).split('/')[0]) / 90) * 100,  # Convert minutes to percentage
        'dato_sofascore': str(fila.get('Sofascore', '0')).split('/')[0],
        'dato_sofascore_percent': float(str(fila.get('Sofascore', '0')).split('/')[0]) * 10,  # Convert 0-10 to 0-100%
        # Market Value Projection
        'market_value_projection': fila.get('Market Value Projection', 'N/A')
    }
    
    # Parse market value projection
    import re
    mvp = str(datos['market_value_projection']).split('|')
    datos['mvp_current'] = mvp[0] if len(mvp) > 0 else 'N/A'
    
    # Extract and format short-term with highlighted value
    if len(mvp) > 1 and mvp[1]:
        match = re.search(r'€[\d\.-]+M\+?', mvp[1])
        if match:
            value = match.group()
            datos['mvp_short_term'] = mvp[1].replace(value, f'<span style="color: var(--neon); font-weight: bold;">{value}</span>')
        else:
            datos['mvp_short_term'] = mvp[1]
    else:
        datos['mvp_short_term'] = ''
    
    # Extract and format peak with highlighted value
    if len(mvp) > 2 and mvp[2]:
        match = re.search(r'€[\d\.-]+M\+?', mvp[2])
        if match:
            value = match.group()
            datos['mvp_peak'] = mvp[2].replace(value, f'<span style="color: var(--neon); font-weight: bold;">{value}</span>')
        else:
            datos['mvp_peak'] = mvp[2]
    else:
        datos['mvp_peak'] = ''

    nombre_archivo = f"Reporte_{fila['Apellido']}_{color_tag}.html"
    with open(os.path.join(CARPETA_SALIDA, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(template.render(datos))

print("🚀 Reportes generados en 'reportes_scouting'")