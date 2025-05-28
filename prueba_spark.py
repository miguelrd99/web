import streamlit as st
import polars as pl
import io

# Cargar el DataFrame desde el archivo CSV con manejo de errores
try:
    ruta_csv = "BBDD_POLIZAS_prueba.csv"
    df = pl.read_csv(ruta_csv, separator=';')
    df = df.with_columns(
        pl.col('POLIZAS').cast(pl.Int64).cast(pl.Utf8).fill_null('').alias('Número_Poliza')
    )
except Exception as e:
    st.error(f"Error al cargar el archivo CSV: {e}")

# Añadir un logo en la parte superior de la barra lateral
st.sidebar.image("bbva_allianz.jpg", use_container_width=True)  # Cambia "bbva_allianz.jpg" por la ruta de tu archivo de imagen

# Configurar la barra lateral para seleccionar la página
st.sidebar.title("Navegación")
seleccion_pagina = st.sidebar.radio("Ir a", ("Buscar por DNI", "Consulta por Póliza"))

# Página para buscar por DNI
if seleccion_pagina == "Buscar por DNI":
    st.title("Consulta de Pólizas por DNI")
    st.markdown("Ingrese el DNI del cliente para buscar sus pólizas. Ejemplo: 12345678A")

    # Entrada de usuario para el DNI
    dni_input = st.text_input("Ingrese el DNI del cliente:")

    # Validación básica del DNI
    if dni_input and len(dni_input) >= 8:
        # Filtrar el DataFrame por el DNI proporcionado
        polizas_cliente = df.filter(pl.col('NIPAGCOM') == dni_input)

        # Mostrar los resultados
        if polizas_cliente.shape[0] > 0:
            st.success(f"Pólizas para el cliente con DNI {dni_input}:")
            st.dataframe(polizas_cliente.to_pandas())
            # Opción para exportar resultados
            csv_buffer = io.StringIO()
            polizas_cliente.write_csv(csv_buffer, separator=';')
            st.download_button(
                label="Descargar resultados",
                data=csv_buffer.getvalue(),
                file_name=f'polizas_{dni_input}.csv',
                mime='text/csv'
            )
        else:
            st.warning(f"No se encontraron pólizas para el DNI {dni_input}.")
    elif dni_input:
        st.error("El DNI ingresado no es válido.")

# Página para filtrar por póliza
elif seleccion_pagina == "Consulta por Póliza":
    st.title("Consulta de pólizas por Número de Póliza")
    st.markdown("Ingrese el número de póliza para buscar la información asociada.")

    # Entrada de usuario para el número de póliza
    poliza_input = st.text_input("Ingrese el número de póliza:")

    # Validación básica del número de póliza
    if poliza_input and poliza_input.isdigit():
        # Filtrar el DataFrame por el número de póliza proporcionado
        clientes_poliza = df.filter(pl.col('Número_Poliza') == poliza_input)

        # Mostrar los resultados
        if clientes_poliza.shape[0] > 0:
            st.success(f"Información de la póliza {poliza_input}:")
            st.dataframe(clientes_poliza.to_pandas())
            # Opción para exportar resultados
            csv_buffer = io.StringIO()
            clientes_poliza.write_csv(csv_buffer, separator=';')
            st.download_button(
                label="Descargar resultados",
                data=csv_buffer.getvalue(),
                file_name=f'info_poliza_{poliza_input}.csv',
                mime='text/csv'
            )
        else:
            st.warning(f"No se encontraron pólizas para el número de póliza {poliza_input}.")
    elif poliza_input:
        st.error("El número de póliza ingresado no es válido.")
