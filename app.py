import numpy as np
import pandas as pd
import streamlit as st

st.title("📊 Explorador de CSV sin código")

# 1. Cargar archivo
st.header("1. Cargar datos")
archivo = st.file_uploader("1.1 Subir archivo CSV", type="csv")

if archivo:
    df = pd.read_csv(archivo)
    st.success("✅ Archivo cargado correctamente")

    # 2. Preparación de los datos
    st.header("2. Preparación de los datos")

    if st.checkbox("2.1 Mostrar primeras N líneas"):
        n = st.number_input("Número de líneas a mostrar", min_value=1, value=5)
        st.dataframe(df.head(n))

    with st.expander("2.2 Mostrar últimas N filas"):
        n_final = st.number_input("¿Cuántas filas finales quieres ver?", min_value=1, max_value=len(df), value=5)
        st.dataframe(df.tail(n_final))

    # 2.3 Información básica + temas detectados
    if st.checkbox("2.3 Información básica del CSV"):
        st.subheader("🔍 Información general del archivo CSV")

        filas, columnas_count = df.shape
        st.write(f"📏 Dimensiones del archivo: **{filas} filas** x **{columnas_count} columnas**")

        # Estimar el peso del archivo
        archivo.seek(0, 2)
        size_bytes = archivo.tell()
        archivo.seek(0)
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        if size_mb > 1:
            st.write(f"💾 Peso estimado: **{size_mb:.2f} MB**")
        else:
            st.write(f"💾 Peso estimado: **{size_kb:.2f} KB**")

        temas_probables = []
        columnas = df.columns.str.lower().tolist()
        nombre_archivo = archivo.name.lower()

        posibles_temas = {
            "📌 Información demográfica": ["edad", "años", "genero", "sexo", "fecha de nacimiento"],
            "📌 Datos biométricos o de salud": ["peso", "altura", "masa", "presión", "temperatura"],
            "📌 Datos financieros o laborales": ["salario", "sueldo", "ingreso", "puesto", "empresa", "departamento"],
            "📌 Encuestas de satisfacción": ["satisfacción", "opinión", "recomendaria", "experiencia", "valoración", "calificación", "encuesta"],
            "📌 Rendimiento académico o escolar": ["calificación", "materia", "promedio", "nota", "evaluación", "asignatura"],
            "📌 Ventas o comercio": ["producto", "precio", "venta", "cliente", "factura", "compra", "cantidad", "total"],
            "📌 Registro de tiempos/asistencia": ["fecha", "hora", "asistencia", "entrada", "salida"]
        }

        for tema, palabras_clave in posibles_temas.items():
            if any(palabra in columnas for palabra in palabras_clave):
                temas_probables.append(tema)

        for tema, palabras_clave in posibles_temas.items():
            if any(palabra in nombre_archivo for palabra in palabras_clave):
                if tema not in temas_probables:
                    temas_probables.append(tema)

        if temas_probables:
            st.write("🧠 Posibles temas del archivo basados en columnas y nombre del archivo:")
            for tema in temas_probables:
                st.markdown(f"- {tema}")
        else:
            st.info("No se pudo determinar un tema claro del CSV automáticamente.")

    # 2.4 Estadísticas descriptivas para columnas numéricas
    if st.checkbox("2.4 Estadísticas descriptivas (df.describe())"):
        st.subheader("📊 Estadísticas descriptivas para columnas numéricas")
        st.write(df.describe())

    # 2.5 Forma del dataset (filas, columnas)
    if st.checkbox("2.5 Forma del dataset (df.shape)"):
        st.subheader("📏 Dimensiones del dataset")
        st.write(df.shape)

    # 2.6 Mostrar nombres de columnas
    if st.checkbox("2.6 Mostrar nombres de columnas (df.columns)"):
        st.subheader("🧾 Nombres de columnas en el archivo CSV")
        st.write(df.columns.tolist())

    # 3. Selección de datos
    st.header("3. Selección de datos")

    col_selec = st.selectbox("3.1 Selecciona una columna", df.columns)
    st.dataframe(df[[col_selec]])

    cols_selec = st.multiselect("3.2 Selecciona varias columnas", df.columns)
    if cols_selec:
        st.dataframe(df[cols_selec])

    # 4. Filtro de filas
    st.header("4. Filtro de filas")

    col_filtro = st.selectbox("4.1 Columna para filtrar", df.columns)
    operador = st.selectbox("Operador", [">", "<", "=="])
    valor = st.text_input("Valor para comparar (texto o número)")
    cols_mostrar = st.multiselect("Columnas a mostrar en resultado", df.columns, default=[col_filtro])

    if st.button("Aplicar filtro"):
        try:
            valor_num = None
            try:
                valor_num = float(valor)
            except:
                pass

            if operador == ">":
                if valor_num is None:
                    st.error("Para operador '>' el valor debe ser numérico")
                else:
                    resultado = df[df[col_filtro] > valor_num]
            elif operador == "<":
                if valor_num is None:
                    st.error("Para operador '<' el valor debe ser numérico")
                else:
                    resultado = df[df[col_filtro] < valor_num]
            elif operador == "==":
                if valor_num is not None:
                    resultado = df[df[col_filtro] == valor_num]
                else:
                    resultado = df[df[col_filtro] == valor]

            if not cols_mostrar:
                st.warning("Selecciona al menos una columna para mostrar")
            else:
                st.dataframe(resultado[cols_mostrar])

        except Exception as e:
            st.error(f"⚠ Error: {e}")
