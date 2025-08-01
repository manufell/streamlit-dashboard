import streamlit as st
import pandas as pd

st.title("Calcolo delle medie per colonne 'count' e 'percentuale'")

uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

if uploaded_file:
    # Carica tutti i fogli in un dizionario
    xls = pd.read_excel(uploaded_file, sheet_name=None)

    # Inizializza contenitori per le medie
    medie_count = {}
    medie_percentuale = {}

    for sheet_name, df in xls.items():
        if sheet_name.lower() == "classificato":
            continue

        # Assicurati che tutte le colonne siano numeriche dove possibile
        df_numeric = df.copy()
        for col in df.columns:
            df_numeric[col] = pd.to_numeric(df[col], errors='coerce')

        media = df_numeric.mean(numeric_only=True)

        # Filtra le medie in base al nome delle colonne
        media_count = media[media.index.str.contains("count", case=False, na=False)]
        media_percentuale = media[media.index.str.contains("percentuale", case=False, na=False)]

        if not media_count.empty:
            medie_count[sheet_name] = media_count
        if not media_percentuale.empty:
            medie_percentuale[sheet_name] = media_percentuale

    st.header("📊 Medie - Colonne 'count'")
    for sheet, media in medie_count.items():
        st.subheader(f"{sheet}")
        st.dataframe(media)

    st.header("📈 Medie - Colonne 'percentuale'")
    for sheet, media in medie_percentuale.items():
        st.subheader(f"{sheet}")
        st.dataframe(media)

    # Crea un file Excel con tutte le medie salvate
    output_file = "medie_separate.xlsx"
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for sheet, media in medie_count.items():
            df_media = media.to_frame().T  # Trasforma la Serie in DataFrame
            df_media.index = [sheet]       # Usa il nome del foglio come indice
            df_media.to_excel(writer, sheet_name=f"Count_{sheet}")

        for sheet, media in medie_percentuale.items():
            df_media = media.to_frame().T
            df_media.index = [sheet]
            df_media.to_excel(writer, sheet_name=f"Percentuale_{sheet}")

    st.success(f"File '{output_file}' creato con successo!")