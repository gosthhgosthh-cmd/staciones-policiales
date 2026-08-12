import math
import pandas as pd
import streamlit as st
from streamlit_js_eval import get_geolocation

st.set_page_config(
    page_title="Estaciones Policiales", page_icon="👮", layout="centered"
)

st.title("👮 Estaciones Policiales Más Cercanas")
st.write(
    "Localiza las 3 estaciones policiales más cercanas a tu ubicación actual."
)

# 1. Base de datos de estaciones
ESTACIONES = [
    {
        "nombre": "Estación Policial Core 7 (Centro)",
        "lat": 14.1025,
        "lon": -87.2038,
    },
    {"nombre": "Estación Policial Belén", "lat": 14.1120, "lon": -87.2180},
    {"nombre": "Estación Policial Kennedy", "lat": 14.0750, "lon": -87.1650},
    {"nombre": "Estación Policial Subirana", "lat": 14.0980, "lon": -87.2080},
    {"nombre": "Estación Policial Loarque", "lat": 14.0320, "lon": -87.2250},
    {"nombre": "Estación Policial San Miguel", "lat": 14.0910, "lon": -87.1710},
]


def haversine(lat1, lon1, lat2, lon2):
  R = 6371.0
  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)
  a = (
      math.sin(dlat / 2) ** 2
      + math.cos(math.radians(lat1))
      * math.cos(math.radians(lat2))
      * math.sin(dlon / 2) ** 2
  )
  return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def buscar_cercanas(user_lat, user_lon, limite=3):
  resultados = []
  for est in ESTACIONES:
    dist = haversine(user_lat, user_lon, est["lat"], est["lon"])
    resultados.append({
        "nombre": est["nombre"],
        "lat": est["lat"],
        "lon": est["lon"],
        "distancia_km": round(dist, 2),
    })
  return sorted(resultados, key=lambda x: x["distancia_km"])[:limite]


# Detección de ubicación mediante navegador
st.subheader("📍 Ubicación del Usuario")
loc = get_geolocation()

lat_defecto = 14.088000
lon_defecto = -87.190000

if loc and "coords" in loc:
  lat_defecto = loc["coords"]["latitude"]
  lon_defecto = loc["coords"]["longitude"]
  st.success("✅ Ubicación GPS detectada automáticamente.")

col1, col2 = st.columns(2)
with col1:
  user_lat = st.number_input("Latitud", value=float(lat_defecto), format="%.6f")
with col2:
  user_lon = st.number_input(
      "Longitud", value=float(lon_defecto), format="%.6f"
  )

if st.button("🔍 Buscar 3 Estaciones Cercanas", use_container_width=True):
  cercanas = buscar_cercanas(user_lat, user_lon, limite=3)

  st.subheader("🚨 Estaciones más cercanas:")
  for idx, est in enumerate(cercanas, 1):
    st.markdown(
        f"**{idx}. {est['nombre']}** — 📏 **{est['distancia_km']} km** de"
        " distancia"
    )

  df_mapa = pd.DataFrame(
      [{"lat": user_lat, "lon": user_lon}]
      + [{"lat": e["lat"], "lon": e["lon"]} for e in cercanas]
  )
  st.map(df_mapa)
