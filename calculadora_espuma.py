import streamlit as st
import math

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Calculadora de espuma",
    page_icon="🧯",
    layout="centered"
)

# Estilos CSS personalizados para que funcione perfecto en Modo Claro y Modo Oscuro
st.markdown("""
    <style>
    .main {
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        background-color: #d32f2f;
        color: white;
    }
    h1 {
        color: #d32f2f;
        text-align: center;
        font-size: 24px !important;
    }
    .highlight-box {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0px;
        border-left: 5px solid;
    }
    /* Forzamos que el texto de las cajas sea oscuro para que se lea en celulares con modo oscuro */
    .concentrado {
        background-color: #ffebee !important;
        border-left-color: #c62828 !important;
        color: #2c0e0e !important;
    }
    .concentrado h4, .concentrado p, .concentrado b, .concentrado small, .concentrado span {
        color: #2c0e0e !important;
    }
    .agua {
        background-color: #e3f2fd !important;
        border-left-color: #1565c0 !important;
        color: #0b2240 !important;
    }
    .agua h4, .agua p, .agua b, .agua small, .agua span {
        color: #0b2240 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧯 Calculadora de Aplicación de Espuma")
st.markdown("<p style='text-align: center; font-weight: bold; margin-bottom: 5px;'>Desarrollada por el Teniente Brigadier Joaquín Córdova Obal - Salvadora Ica N° 22 - VI Comandancia Departamental Ica</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Herramienta móvil de toma de decisiones para el cálculo de Aplicación de Espuma Contra Incendios</p>", unsafe_allow_html=True)

st.divider()

# Sección 1: Selección de Combustible y Escenario
st.subheader("1. Características del Escenario")
tipo_combustible = st.selectbox(
    "Tipo de Combustible:",
    ["Hidrocarburo", "Solvente Polar"],
    help="Seleccione el tipo de combustible de la emergencia."
)

tipo_derrame = st.selectbox(
    "Tipo de Derrame / Escenario:",
    ["Derrame menor a 1\" de profundidad (Área Plana)", "Derrame mayor a 1\" de profundidad / Tanque"],
    help="Profundidad del líquido inflamable."
)

# Sección 2: Dimensionamiento del área
st.subheader("2. Dimensiones de la Zona de Fuego")
tipo_calculo_area = st.radio(
    "Método para ingresar el área:",
    ["Calcular por dimensiones (Largo/Ancho o Diámetro)", "Ingresar Área Directa (m²)"]
)

area_m2 = 0.0

if tipo_calculo_area == "Calcular por dimensiones (Largo/Ancho o Diámetro)":
    if "menor a 1\"" in tipo_derrame:
        largo = st.number_input("Largo de la zona (metros):", min_value=0.0, value=10.0, step=1.0)
        ancho = st.number_input("Ancho de la zona (metros):", min_value=0.0, value=10.0, step=1.0)
        area_m2 = largo * ancho
        st.info(f"📐 Área Calculada: **{area_m2:.2f} m²**")
    else:
        diametro = st.number_input("Diámetro del tanque (metros):", min_value=0.0, value=15.0, step=0.5)
        area_m2 = math.pi * ((diametro / 2) ** 2)
        st.info(f"📐 Área Circular Calculada: **{area_m2:.2f} m²**")
else:
    area_m2 = st.number_input("Ingrese el área total en metros cuadrados (m²):", min_value=0.0, value=100.0, step=10.0)

# Sección 3: Dosificación de la Espuma
st.subheader("3. Dosificación")
concentrado_opcion = st.selectbox(
    "Concentración de la Espuma (%):",
    ["1%", "3%", "6%"],
    index=1 # Default 3%
)
concentrado_pct = float(concentrado_opcion.replace("%", "")) / 100.0

st.divider()

# ---- CÁLCULOS LOGÍSTICOS ----
if tipo_combustible == "Hidrocarburo":
    if "menor a 1\"" in tipo_derrame:
        tasa = 1.08  # GPM/m²
        tiempo = 15  # minutos
    else:
        tasa = 1.72  # GPM/m²
        tiempo = 65  # minutos
else:  # Solvente Polar
    if "menor a 1\"" in tipo_derrame:
        tasa = 2.10  # GPM/m²
        tiempo = 15  # minutos
    else:
        tasa = 3.20  # GPM/m²
        tiempo = 65  # minutos

# Resultados matemáticos
gpm_solucion = area_m2 * tasa
gpm_concentrado = gpm_solucion * concentrado_pct
gpm_agua = gpm_solucion - gpm_concentrado

galones_concentrado = gpm_concentrado * tiempo
galones_agua = gpm_agua * tiempo
galones_solucion_total = gpm_solucion * tiempo

# ---- PANTALLA DE RESULTADOS ----
st.subheader("📊 Recursos de Extinción Requeridos")

if area_m2 <= 0:
    st.warning("⚠️ Ingrese dimensiones válidas para realizar el cálculo.")
else:
    # Métricas principales
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Caudal de Solución", value=f"{gpm_solucion:.2f} GPM")
    with col2:
        st.metric(label="Tiempo de Operación", value=f"{tiempo} min")

    st.markdown(f"""
    <div class="highlight-box concentrado">
        <h4 style="margin: 0; font-weight: bold;">🧪 CONCENTRADO DE ESPUMA REQUERIDO</h4>
        <p style="margin: 5px 0 0 0; font-size: 18px;">
            <b>{galones_concentrado:.1f} Galones</b> de espumógeno al {concentrado_opcion}
            <br><small>(Caudal de dosificación: {gpm_concentrado:.2f} GPM)</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="highlight-box agua">
        <h4 style="margin: 0; font-weight: bold;">💧 AGUA REQUERIDA</h4>
        <p style="margin: 5px 0 0 0; font-size: 18px;">
            <b>{galones_agua:.1f} Galones</b> de agua de abastecimiento
            <br><small>(Caudal de agua pura: {gpm_agua:.2f} GPM)</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Resumen técnico
    with st.expander("🔍 Ver Detalles y Parámetros Técnicos de la Fuente"):
        st.write(f"**Área de cobertura:** {area_m2:.2f} m²")
        st.write(f"**Tasa de aplicación estándar:** {tasa:.2f} GPM/m²")
        st.write(f"**Volumen total de solución de espuma:** {galones_solucion_total:.1f} Galones")
        st.write("---")
        st.info("💡 **Nota operativa:** Asegúrese de contar con la cantidad de galones calculada en el lugar antes de iniciar la aplicación para garantizar un ataque ininterrumpido conforme a la norma.")
