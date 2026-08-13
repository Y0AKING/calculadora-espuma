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
    .friccion {
        background-color: #fff8e1 !important;
        border-left-color: #ffb300 !important;
        color: #3e2723 !important;
    }
    .friccion h4, .friccion p, .friccion b, .friccion small, .friccion span {
        color: #3e2723 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧯 Calculadora de Hidráulica")
# Primera línea: Normal / Regular
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Desarrollada por el Teniente Brigadier Joaquín Córdova Obal - Salvadora Ica N° 22 - VI Comandancia Departamental Ica</p>", unsafe_allow_html=True)
# Segunda línea: En negrita / Bold
st.markdown("<p style='text-align: center; font-weight: bold; font-size: 16px;'>Herramienta móvil de toma de decisiones para el cálculo de Aplicación de Espuma Contra Incendios</p>", unsafe_allow_html=True)

st.divider()

# Creación de Pestañas (Tabs)
tab1, tab2 = st.tabs(["🧯 Aplicación de Espuma", "🌊 Pérdida por Fricción"])

# =========================================================================
# PESTAÑA 1: CÁLCULO DE APLICACIÓN DE ESPUMA
# =========================================================================
with tab1:
    # Sección 1: Selección de Combustible y Escenario
    st.subheader("1. Características del Escenario")
    tipo_combustible = st.selectbox(
        "Tipo de Combustible:",
        ["Hidrocarburo", "Solvente Polar"],
        help="Seleccione el tipo de combustible de la emergencia.",
        key="foam_combustible"
    )

    tipo_derrame = st.selectbox(
        "Tipo de Derrame / Escenario:",
        ["Derrame menor a 1\" de profundidad (Área Plana)", "Derrame mayor a 1\" de profundidad / Tanque"],
        help="Profundidad del líquido inflamable.",
        key="foam_derrame"
    )

    # Sección 2: Dimensionamiento del área
    st.subheader("2. Dimensiones de la Zona de Fuego")
    tipo_calculo_area = st.radio(
        "Método para ingresar el área:",
        ["Calcular por dimensiones (Largo/Ancho o Diámetro)", "Ingresar Área Directa (m²)"],
        key="foam_metodo_area"
    )

    area_m2 = 0.0

    if tipo_calculo_area == "Calcular por dimensiones (Largo/Ancho o Diámetro)":
        if "menor a 1\"" in tipo_derrame:
            largo = st.number_input("Largo de la zona (metros):", min_value=0.0, value=10.0, step=1.0, key="foam_largo")
            ancho = st.number_input("Ancho de la zona (metros):", min_value=0.0, value=10.0, step=1.0, key="foam_ancho")
            area_m2 = largo * ancho
            st.info(f"📐 Área Calculada: **{area_m2:.2f} m²**")
        else:
            diametro = st.number_input("Diámetro del tanque (metros):", min_value=0.0, value=15.0, step=0.5, key="foam_diametro")
            area_m2 = math.pi * ((diametro / 2) ** 2)
            st.info(f"📐 Área Circular Calculada: **{area_m2:.2f} m²**")
    else:
        area_m2 = st.number_input("Ingrese el área total en metros cuadrados (m²):", min_value=0.0, value=100.0, step=10.0, key="foam_area_directa")

    # Sección 3: Dosificación de la Espuma
    st.subheader("3. Dosificación")
    concentrado_opcion = st.selectbox(
        "Concentración de la Espuma (%):",
        ["1%", "3%", "6%"],
        index=1, # Default 3%
        key="foam_concentrado"
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


# =========================================================================
# PESTAÑA 2: CÁLCULO DE PÉRDIDA DE PRESIÓN POR FRICCIÓN
# =========================================================================
with tab2:
    st.subheader("1. Configuración del Tendido")
    
    # Selector de manguera y coeficiente C
    manguera_opcion = st.selectbox(
        "Diámetro de la Manguera / Configuración:",
        [
            "1 ½\" (C = 24)",
            "1 ¾\" (C = 15.5)",
            "2 ½\" (C = 2)",
            "3\" (C = 0.8)",
            "4\" (C = 0.2)",
            "2 Líneas en paralelo de 2 ½\" (C = 0.5)",
            "3 Líneas en paralelo de 2 ½\" (C = 0.22)"
        ],
        index=2, # Default 2 1/2" (C=2)
        help="Seleccione el diámetro de la manguera o configuración en paralelo.",
        key="friccion_manguera"
    )
    
    # Mapeo de coeficientes C basados estrictamente en las Tablas de Pérdida
    mapeo_c = {
        "1 ½\" (C = 24)": 24.0,
        "1 ¾\" (C = 15.5)": 15.5,
        "2 ½\" (C = 2)": 2.0,
        "3\" (C = 0.8)": 0.8,
        "4\" (C = 0.2)": 0.2,
        "2 Líneas en paralelo de 2 ½\" (C = 0.5)": 0.5,
        "3 Líneas en paralelo de 2 ½\" (C = 0.22)": 0.22
    }
    coef_c = mapeo_c[manguera_opcion]

    # Caudal desalojado (Q)
    caudal_gpm = st.number_input(
        "Caudal Desalojado (GPM):",
        min_value=0.0,
        value=250.0,
        step=25.0,
        help="Ingrese el caudal que pasa por la manguera o sistema en Galones por Minuto.",
        key="friccion_caudal"
    )

    st.subheader("2. Longitud de la Línea")
    
    # Selección de método para longitud
    tipo_longitud = st.radio(
        "Método de ingreso de longitud:",
        ["Por Tramos (Paños de 30m / 100 pies)", "Por Metros Directos"],
        key="friccion_metodo_longitud"
    )

    longitud_pies = 0.0

    if tipo_longitud == "Por Tramos (Paños de 30m / 100 pies)":
        tramos = st.number_input(
            "Cantidad de Tramos (Paños):",
            min_value=0.0,
            value=3.0,
            step=1.0,
            key="friccion_tramos"
        )
        longitud_pies = tramos * 100.0
        st.info(f"📏 Longitud Equivalente: **{longitud_pies:.0f} pies** (~{tramos * 30:.0f} metros)")
    else:
        metros = st.number_input(
            "Longitud en Metros:",
            min_value=0.0,
            value=90.0,
            step=10.0,
            key="friccion_metros"
        )
        # 30 metros = 100 pies según convenciones CGBVP en tablas
        longitud_pies = metros * (100.0 / 30.0)
        st.info(f"📏 Longitud Calculada: **{longitud_pies:.1f} pies**")

    st.divider()

    # ---- CÁLULO DE FRICCIÓN ----
    # Fórmula oficial: PF = C * (Q/100)^2 * (L/100)
    q_factor = caudal_gpm / 100.0
    l_factor = longitud_pies / 100.0
    perdida_friccion = coef_c * (q_factor ** 2) * l_factor

    # ---- PANTALLA DE RESULTADOS DE FRICCIÓN ----
    st.subheader("📊 Pérdida de Carga Estimada")

    if caudal_gpm <= 0 or longitud_pies <= 0:
        st.warning("⚠️ Ingrese un caudal y longitud válidos para realizar el cálculo.")
    else:
        st.markdown(f"""
        <div class="highlight-box friccion">
            <h4 style="margin: 0; font-weight: bold;">🌊 PÉRDIDA POR FRICCIÓN TOTAL</h4>
            <p style="margin: 5px 0 0 0; font-size: 20px;">
                <b>{perdida_friccion:.1f} PSI</b> de caída de presión en la línea
                <br><small>(Fórmula: C × [Q/100]² × [L/100])</small>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Recomendaciones de la fuente y parámetros técnicos
        with st.expander("🔍 Ver Detalles y Recomendaciones de Reducción"):
            st.write(f"**Coeficiente de Fricción (C):** {coef_c}")
            st.write(f"**Caudal en centenares (Q/100):** {q_factor:.2f}")
            st.write(f"**Longitud en centenares de pies (L/100):** {l_factor:.2f}")
            st.write("---")
            st.markdown("""
            💡 **Recomendaciones para reducir la pérdida por fricción (Manual CGBVP):**
            * **Líneas más cortas:** Mantenga los tendidos lo más cortos posible.
            * **Mayor diámetro:** Utilice mangueras más anchas (e.g. 2 ½" o 3") para trayectos largos.
            * **Líneas en paralelo:** Cuando necesite caudales altos, use múltiples líneas (paralelo) para dividir el flujo y bajar drásticamente la fricción.
            * **Evite pliegues:** Procure que la manguera no tenga estrangulamientos o dobleces agudos.
            * **Válvulas abiertas:** Mantenga las válvulas y pitones completamente abiertos durante la operación.
            """)
