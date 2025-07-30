
import streamlit as st
import pandas as pd

st.title("Unione dati VIP-positive (alpha7 + beta2)")

# Caricamento file
uploaded_alpha7 = st.file_uploader("Carica il file Excel per alpha7 (VIP-positive)", type=["xlsx"])
uploaded_beta2 = st.file_uploader("Carica il file Excel per beta2 (VIP-positive)", type=["xlsx"])

if uploaded_alpha7 and uploaded_beta2:
    # Leggi i file Excel
    df_alpha7 = pd.read_excel(uploaded_alpha7)
    df_beta2 = pd.read_excel(uploaded_beta2)

    # Aggiungi suffissi per distinguere le colonne
    df_alpha7 = df_alpha7.add_suffix("_alpha7")
    df_beta2 = df_beta2.add_suffix("_beta2")

    # Unione orizzontale
    df_unito = pd.concat([df_alpha7, df_beta2], axis=1)

    # Mostra un'anteprima
    st.subheader("Anteprima dei dati uniti")
    st.dataframe(df_unito.head())

    # Esportazione in Excel
    output_filename = "VIP_positive_unito.xlsx"
    df_unito.to_excel(output_filename, index=False)

    # Download del file unito
    with open(output_filename, "rb") as f:
        st.download_button(
            label="📥 Scarica file unito",
            data=f,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Carica entrambi i file per procedere con l'unione.")