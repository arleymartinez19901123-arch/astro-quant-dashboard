import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
from collections import Counter
from datetime import datetime
import time

st.set_page_config(page_title="Astro Luna Quant", layout="wide")

# =========================
# 📡 SCRAPER
# =========================
@st.cache_data(ttl=300)
def obtener_datos():
    url = "https://resultadodelaloteria.com/colombia/astro-luna"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except:
        return pd.DataFrame(columns=["Fecha", "Numero", "Signo"])

    soup = BeautifulSoup(r.text, "html.parser")

    datos = []
    filas = soup.select("table tr")

    for f in filas[1:]:
        cols = f.find_all("td")

        if len(cols) >= 3:
            numero_raw = cols[1].text.strip()

            # limpiar número correctamente
            numero = ''.join(filter(str.isdigit, numero_raw)).zfill(4)

            datos.append([
                cols[0].text.strip(),
                numero,
                cols[2].text.strip()
            ])

    df = pd.DataFrame(datos, columns=["Fecha", "Numero", "Signo"])

    # filtrar solo números válidos
    df = df[df["Numero"].str.match(r"^\d{4}$", na=False)]

    return df


# =========================
# 🔢 ANALISIS
# =========================
def analisis(df):
    if df.empty:
        return Counter()

    digitos = [d for n in df["Numero"] for d in str(n)]
    return Counter(digitos)


# =========================
# 🔮 GENERADOR INTELIGENTE
# =========================
def generar_jugadas_real(df, n=5):
    if df.empty:
        return []

    digitos = [d for n in df["Numero"][:50] for d in str(n)]
    freq = Counter(digitos)

    nums = list(freq.keys())
    pesos = list(freq.values())

    signos = [
        "Aries","Tauro","Geminis","Cancer","Leo","Virgo",
        "Libra","Escorpio","Sagitario","Capricornio","Acuario","Piscis"
    ]

    jugadas = []

    for _ in range(n):
        num = "".join(random.choices(nums, pesos, k=4))
        jugadas.append((num, random.choice(signos)))

    return jugadas


# =========================
# 🖥️ UI
# =========================
st.title("📊 Astro Luna Quant Dashboard PRO")

# Obtener datos
df = obtener_datos()

# =========================
# 🟢 ÚLTIMO RESULTADO
# =========================
st.subheader("📈 Histórico reciente")

if not df.empty:
    df_hist = df.copy()

    # Convertir fecha (evita errores si viene como texto raro)
    df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"], errors="coerce")

    # Ordenar por fecha (más reciente arriba)
    df_hist = df_hist.sort_values(by="Fecha", ascending=False)

    # Resetear índice limpio
    df_hist = df_hist.reset_index(drop=True)

    # Mostrar solo últimos 50
    st.dataframe(df_hist.head(50), use_container_width=True)
else:
    st.info("No hay datos históricos disponibles")
# =========================
# ⏰ ESTADO DEL SORTEO
# =========================
hora = datetime.now().hour

if hora >= 22:
    st.success("🟢 Resultado ya disponible")
else:
    st.warning("⏳ Esperando sorteo de hoy")

# =========================
# 📈 HISTÓRICO
# =========================
st.subheader("📈 Histórico reciente")
st.dataframe(df.head(50), use_container_width=True)

# =========================
# 🔢 FRECUENCIA DE DÍGITOS
# =========================
st.subheader("🔢 Frecuencia de dígitos")
freq = analisis(df)

if freq:
    st.bar_chart(pd.DataFrame(freq.values(), index=freq.keys()))
else:
    st.info("Sin datos para analizar")

# =========================
# 🔥 TENDENCIAS
# =========================
st.subheader("🔥 Dígitos calientes")

if freq:
    st.write(freq.most_common(5))

# =========================
# 🧠 ANÁLISIS AUTOMÁTICO
# =========================
st.subheader("🧠 Análisis automático")

if "7" in freq:
    st.write("📌 Tendencia detectada: el dígito 7 está fuerte")

if "0" in freq:
    st.write("📌 Tendencia detectada: el dígito 0 está fuerte")

# =========================
# 🔮 JUGADAS
# =========================
st.subheader("🔮 Jugadas sugeridas (modo quant)")

jugadas = generar_jugadas_real(df)

if jugadas:
    for num, signo in jugadas:
        st.write(f"👉 {num} - {signo}")
else:
    st.info("Esperando datos para generar jugadas")

# =========================
# 🔄 AUTO REFRESH (MEJORADO)
# =========================
st.caption("Actualizando cada 5 minutos...")
st.experimental_rerun()
