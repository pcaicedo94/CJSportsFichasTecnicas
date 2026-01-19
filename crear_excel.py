import pandas as pd

data = {
    # --- INFO BASICA ---
    'Nombre': ['Lionel', 'Cristiano'],
    'Apellido': ['Gómez', 'Silva'],
    'Posicion': ['MEDIOCENTRO', 'DELANTERO'],
    'Foto_URL': [
        'https://images.unsplash.com/photo-1517466787929-bc90951d0974?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?auto=format&fit=crop&w=800&q=80'
    ],
    'Nacionalidad': ['🇦🇷 ARG', '🇵🇹 POR'],
    'Edad': [24, 28],
    'Altura': ['1.82m', '1.87m'],
    'Peso': ['78kg', '84kg'],
    'Pie': ['Izquierdo', 'Derecho'],
    
    # --- PERFIL MERCADO ---
    'Club_Actual': ['CA Central', 'Sporting Norte'],
    'Contrato_Hasta': ['30/06/2026', '30/06/2025'],
    'Valor_Mercado': ['€1.5M', '€2.8M'],
    'Agencia': ['CJ Sports', 'CJ Sports'],
    
    # --- VIDEO HIGHLIGHTS (Nuevo) ---
    'Video_URL': ['https://youtube.com', 'https://hudl.com'],

    # --- SCOUTING METRICS (SCORE 0-100 PARA GRAFICO) ---
    # Usamos percentiles: 90 significa "Mejor que el 90% de la liga"
    'Sc_Duelos_Ganados': [88, 60],      # % Duelos
    'Sc_Juego_Aereo': [45, 95],         # Duelos aéreos
    'Sc_Pases_Prog': [98, 70],          # Pases progresivos
    'Sc_Regates': [92, 85],             # Regates completados
    'Sc_Recuperaciones': [75, 40],      # Recuperaciones campo rival
    'Sc_Goles_Esperados': [80, 96],     # xG (Expected Goals)

    # --- DATOS REALES (PARA TEXTO) ---
    # Estos son los números "duros" que el gráfico representa
    'Dato_Duelos': ['68%', '45%'],
    'Dato_Aereo': ['1.2/90', '5.8/90'],
    'Dato_Pases': ['12.5/90', '4.2/90'],

    # --- FODA (Texto separado por '|') ---
    'Fortalezas': ['Visión de juego|Pase entre líneas|Balón parado', 'Juego aéreo|Finalización|Potencia física'],
    'Debilidades': ['Duelo aéreo defensivo|Uso pie derecho', 'Participación en construcción|Presión alta'],
    
    'Trayectoria_1': ['2023/24|CA Central|32|12', '2023/24|Sp. Norte|28|15'],
    'Trayectoria_2': ['2022/23|Dep. Sur|28|5',  '2022/23|FC Porto B|30|10'],
    'Trayectoria_3': ['2021/22|Juniors|15|2',   '2021/22|Braga U23|22|8'],
}

df = pd.DataFrame(data)
df.to_excel('datos_scouting.xlsx', index=False)
print("✅ Excel 'datos_scouting.xlsx' actualizado con métricas profesionales.")