import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
from collections import Counter
from datetime import datetime
import time

st.set_page_config(page_title="Astro Luna Quant PRO", layout="wide")

# =========================
# 📡 SCRAPER ROBUSTO
# =========================
@st.cache_data(ttl=300)
def obtener_datos():
    url = "https://resultadodelaloteria.com/colombia/astro-luna"

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        datos = []
        filas = soup.select("table tr")

        for f in filas:
            cols = f.find_all("td")

            if len(cols) >= 3:
                fecha = cols[0].text.strip()
                numero_raw = cols[1].text.strip()
                signo = cols[2].text.strip()

                # 🔒 LIMPIEZA EXTREMA
                numero = ''.join(c for c in numero_raw if c.isdigit())

                # SOLO números válidos de 4 dígitos
                if len(numero) == 4:
                    datos.append([fecha, numero, signo])

        df = pd.DataFrame(datos, columns=["Fecha", "Numero", "Signo"])

        # eliminar duplicados
        df = df.drop_duplicates()

        return df

    except Exception:
        return pd.DataFrame(columns=["Fecha", "Numero", "Signo"])

# =========================
# 🔢 ANALISIS SEGURO
# =========================
def analisis(df):
    digitos = []

    for n in df["Numero"]:
        if isinstance(n, str) and n.isdigit():
            digitos.extend(list(n))

    return Counter(digitos)

# =========================
# 🔮 GENERADOR SEGURO
# =========================
def generar_jugadas_real(df, n=5):

    if df.empty:
        return []

    digitos = []

    for n in df["Numero"].head(50):
        if isinstance(n, str) and n.isdigit():
            digitos.extend(list(n))

    if not digitos:
        return []

    freq = Counter(digitos)

    nums = list(freq.keys())
    pesos = list(freq.values())

    signos = ["Aries","Tauro","Geminis","Cancer","Leo","Virgo",
              "Libra","Escorpio","Sagitario","Capricornio","Acuario","Piscis"]

    jugadas = []

    for _ in range(n):
        num = "".join(random.choices(nums, pesos, k=4))
        jugadas.append((num, random.choice(signos)))

    return jugadas

# =========================
# 🖥️ UI
# =========================
st.title("📊 Astro Luna Quant Dashboard PRO")

df = obtener_datos()

# =========================
# 🟢 RESULTADO
# =========================
st.subheader("🟢 Último resultado en tiempo real")

if not df.empty:
    ultimo = df.iloc[0]
    st.success(f"🎯 {ultimo['Numero']} - {ultimo['Signo']}")
    st.caption(f"📅 Fecha: {ultimo['Fecha']}")
else:
    st.error("⚠️ No se pudieron obtener datos")

# =========================
# ⏰ ESTADO
# =========================
hora = datetime.now().hour

if hora >= 22:
    st.success("🟢 Resultado disponible")
else:
    st.warning("⏳ Esperando sorteo")

# =========================
# 📈 HISTORICO
# =========================
st.subheader("📈 Histórico reciente")

if not df.empty:
    st.dataframe(df.head(50), use_container_width=True)

# =========================
# 🔢 FRECUENCIAS LIMPIAS
# =========================
st.subheader("🔢 Frecuencia de dígitos")

freq = analisis(df)

if freq:
    df_freq = pd.DataFrame({
        "frecuencia": list(freq.values())
    }, index=list(freq.keys()))

    st.bar_chart(df_freq)

# =========================
# 🔥 TOP DIGITOS
# =========================
st.subheader("🔥 Dígitos calientes")

if freq:
    st.write(freq.most_common(5))

# =========================
# 🧠 ANALISIS
# =========================
st.subheader("🧠 Análisis automático")

if "7" in freq:
    st.write("📌 El dígito 7 está fuerte")

if "0" in freq:
    st.write("📌 El dígito 0 está fuerte")

# =========================
# 🔮 JUGADAS
# =========================
st.subheader("🔮 Jugadas sugeridas")

jugadas = generar_jugadas_real(df)

if jugadas:
    for num, signo in jugadas:
        st.write(f"👉 {num} - {signo}")
else:
    st.warning("No hay datos suficientes para generar jugadas")

# =========================
# 🔄 AUTO REFRESH
# =========================
st.caption("🔄 Actualización automática cada 5 minutos")
time.sleep(300)
st.rerun()
