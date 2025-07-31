import streamlit as st
import pandas as pd
from io import BytesIO
import re

st.set_page_config(page_title="Unione classificazioni per sezione", layout="wide")
st.title("📊 Unione classificazioni alpha7/beta2 per sezione (una riga per sezione)")

uploaded_files = st.file_uploader(
    "Carica i file Excel da unire (devono avere stessi fogli):",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file caricati correttamente.")

    foglio_classificato = "Classificato"
    fogli_da_pivotare = [
        "Alpha7_stats", "Beta2_stats",
        "Alpha7_Pos", "Beta2_Pos",
        "Double_Pos", "Combinazioni"
    ]

    # Contenitori
    classificato_df_list = []
    fogli_risultato = {sheet: [] for sheet in fogli_da_pivotare}

    for file in uploaded_files:
        nome_file = file.name
        match = re.search(r"(S\d+)", nome_file)
        sezione = match.group(1) if match else nome_file.replace(".xlsx", "")

        excel = pd.ExcelFile(file)

        # Classificato → concatena per righe
        try:
            df_class = excel.parse(foglio_classificato)
            df_class["Sezione"] = sezione
            classificato_df_list.append(df_class)
        except Exception as e:
            st.warning(f"Errore nel foglio '{foglio_classificato}' da {nome_file}: {e}")

        # Altri fogli → pivot per singola riga per sezione
        for sheet in fogli_da_pivotare:
            try:
                df = excel.parse(sheet)

                # Normalizza nomi colonne
                df.columns = [str(col).strip() for col in df.columns]

                # Trasforma: da righe a colonne
                row_dict = {"Sezione": sezione}
                for _, row in df.iterrows():
                    categoria = row[0]  # Prima colonna = categoria (es. Negative)
                    for col in df.columns[1:]:
                        new_col_name = f"{col}_{categoria}".replace(" ", "").replace("-", "")
                        row_dict[new_col_name] = row[col]
                fogli_risultato[sheet].append(row_dict)

            except Exception as e:
                st.warning(f"Errore nel foglio '{sheet}' da {nome_file}: {e}")

    # Finalizza "Classificato"
    fogli_uniti = {}
    if classificato_df_list:
        df_classificato_finale = pd.concat(classificato_df_list, ignore_index=True)
        fogli_uniti[foglio_classificato] = df_classificato_finale
        st.subheader("📄 Classificato (unito per righe)")
        st.dataframe(df_classificato_finale.head())

    # Finalizza gli altri fogli → unione per colonna
    for sheet, lista_dizionari in fogli_risultato.items():
        if lista_dizionari:
            df_finale = pd.DataFrame(lista_dizionari)
            fogli_uniti[sheet] = df_finale
            st.subheader(f"📄 {sheet} (una riga per sezione, colonne = categorie)")
            st.dataframe(df_finale.head())

    # Esporta tutto in un unico Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for nome_foglio, df in fogli_uniti.items():
            df.to_excel(writer, index=False, sheet_name=nome_foglio)
    output.seek(0)

    st.download_button(
        label="📥 Scarica file unificato",
        data=output,
        file_name="classificazione_finale.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("👆 Carica almeno due file Excel con la stessa struttura per iniziare.") 