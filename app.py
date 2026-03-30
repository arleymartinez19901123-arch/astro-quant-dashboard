import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
from collections import Counter

st.set_page_config(page_title="Astro Luna Quant", layout="wide")

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
            datos.append([
                cols[0].text.strip(),
                cols[1].text.strip().zfill(4),
                cols[2].text.strip()
            ])

    return pd.DataFrame(datos, columns=["Fecha", "Numero", "Signo"])

def analisis(df):
    digitos = [d for n in df["Numero"] for d in n]
    return Counter(digitos)

def generar_jugadas():
    signos = ["Aries","Tauro","Geminis","Cancer","Leo","Virgo",
              "Libra","Escorpio","Sagitario","Capricornio","Acuario","Piscis"]

    return [
        ("".join(str(random.randint(0,9)) for _ in range(4)), random.choice(signos))
        for _ in range(5)
    ]

st.title("📊 Astro Luna Quant Dashboard")

df = obtener_datos()

st.subheader("📡 Resultados recientes")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("🔢 Frecuencia de dígitos")
freq = analisis(df)
st.bar_chart(pd.DataFrame(freq.values(), index=freq.keys()))

st.subheader("🔮 Jugadas sugeridas")
for num, signo in generar_jugadas():
    st.write(f"👉 {num} - {signo}")
