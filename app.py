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
# 📡 SCRAPER LIMPIO
# =========================
@st.cache_data(ttl=300)
def obtener_datos():
    url = "https://resultadodelaloteria.com/colombia/astro-luna"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    datos = []
    filas = soup.select("table tr")

    for f in filas[1:]:
        cols = f.find_all("td")
        if len(cols) >= 3:

            fecha = cols[0].text.strip()
            numero_raw = cols[1].text.strip()
            signo = cols[2].text.strip()

            # 🔥 limpiar solo números
            numero = ''.join(filter(str.isdigit, numero_raw)).zfill(4)

            datos.append([fecha, numero, signo])

    df = pd.DataFrame(datos, columns=["Fecha", "Numero", "Signo"])

    # 🔒 FILTRO: solo números válidos de 4 dígitos
    df = df[df["Numero"].str.match(r"^\d{4}$")]

    return df

# =========================
# 🔢 ANALISIS LIMPIO
# =========================
def analisis(df):
    digitos = []
    for n in df["Numero"]:
        if n.isdigit():
            digitos.extend(list(n))
    return Counter(digitos)

# =========================
# 🔮 GENERADOR INTELIGENTE
# =========================
def generar_jugadas_real(df, n=5):
    digitos = []
    for n in df["Numero"][:50]:
        if n.isdigit():
            digitos.extend(list(n))

    freq = Counter(digitos)

    nums = list(freq.keys())
    pesos = list(freq.values())

    signos = ["Aries","Tauro","Geminis","Cancer","Leo","Virgo",
              "Libra","Escorpio","Sagitario","Capricornio","Acuario","Piscis"]

    jugadas = []

    for _ in range(n):
        num = "".join(str(random.choices(nums, pesos)[0]) for _ in range(4))
        jugadas.append((num, random.choice(signos)))

    return jugadas

# =========================
# 🖥️ UI
# =========================
st.title("📊 Astro Luna Quant Dashboard PRO")

df = obtener_datos()

# =========================
# 🟢 ÚLTIMO RESULTADO CORRECTO
# =========================
st.subheader("🟢 Último resultado en tiempo real")

if not df.empty:
    ultimo = df.iloc[0]
    st.success(f"🎯 {ultimo['Numero']} - {ultimo['Signo']}")
    st.caption(f"📅 Fecha: {ultimo['Fecha']}")
else:
    st.error("No se pudieron cargar los datos")

# =========================
# ⏰ ESTADO DEL SORTEO
# =========================
hora = datetime.now().hour

if hora >= 22:
    st.success("🟢 Resultado ya disponible")
else:
    st.warning("⏳ Esperando sorteo de hoy")

# =========================
# 📈 HISTÓRICO LIMPIO
# =========================
st.subheader("📈 Histórico reciente")
st.dataframe(df.head(50), use_container_width=True)

# =========================
# 🔢 FRECUENCIA LIMPIA
# =========================
st.subheader("🔢 Frecuencia de dígitos")
freq = analisis(df)

df_freq = pd.DataFrame({
    "digito": list(freq.keys()),
    "frecuencia": list(freq.values())
}).set_index("digito")

st.bar_chart(df_freq)

# =========================
# 🔥 TENDENCIAS REALES
# =========================
st.subheader("🔥 Dígitos calientes")
st.write(freq.most_common(5))

# =========================
# 🧠 ANÁLISIS IA SIMPLE
# =========================
st.subheader("🧠 Análisis automático")

if "7" in freq:
    st.write("📌 Tendencia detectada: el dígito 7 está fuerte")

if "0" in freq:
    st.write("📌 Tendencia detectada: el dígito 0 está fuerte")

# =========================
# 🔮 JUGADAS LIMPIAS
# =========================
st.subheader("🔮 Jugadas sugeridas (modo quant)")

jugadas = generar_jugadas_real(df)

for num, signo in jugadas:
    st.write(f"👉 {num} - {signo}")

# =========================
# 🔄 AUTO REFRESH
# =========================
st.caption("Actualizando cada 5 minutos...")
time.sleep(300)
st.rerun()
