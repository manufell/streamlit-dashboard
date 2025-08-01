import streamlit as st
import pandas as pd

st.title("Unione dati VIP-positive e VIP-negative (alpha7 + beta2)")

st.header("🔵 VIP-positive")

# Caricamento file VIP-positive
uploaded_alpha7_pos = st.file_uploader("Carica il file Excel per alpha7 (VIP-positive)", type=["xlsx"], key="alpha7_pos")
uploaded_beta2_pos = st.file_uploader("Carica il file Excel per beta2 (VIP-positive)", type=["xlsx"], key="beta2_pos")

if uploaded_alpha7_pos and uploaded_beta2_pos:
    # Leggi i file Excel
    df_alpha7_pos = pd.read_excel(uploaded_alpha7_pos)
    df_beta2_pos = pd.read_excel(uploaded_beta2_pos)

    # Aggiungi suffissi per distinguere le colonne
    df_alpha7_pos = df_alpha7_pos.add_suffix("_alpha7")
    df_beta2_pos = df_beta2_pos.add_suffix("_beta2")

    # Unione orizzontale
    df_unito_pos = pd.concat([df_alpha7_pos, df_beta2_pos], axis=1)

    # Mostra un'anteprima
    st.subheader("Anteprima dati uniti VIP-positive")
    st.dataframe(df_unito_pos.head())

    # Esportazione in Excel
    output_filename_pos = "VIP_positive_unito.xlsx"
    df_unito_pos.to_excel(output_filename_pos, index=False)

    # Download
    with open(output_filename_pos, "rb") as f:
        st.download_button(
            label="📥 Scarica file unito VIP-positive",
            data=f,
            file_name=output_filename_pos,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Carica entrambi i file VIP-positive per procedere con l'unione.")


st.header("🔴 VIP-negative")

# Caricamento file VIP-negative
uploaded_alpha7_neg = st.file_uploader("Carica il file Excel per alpha7 (VIP-negative)", type=["xlsx"], key="alpha7_neg")
uploaded_beta2_neg = st.file_uploader("Carica il file Excel per beta2 (VIP-negative)", type=["xlsx"], key="beta2_neg")

if uploaded_alpha7_neg and uploaded_beta2_neg:
    # Leggi i file Excel
    df_alpha7_neg = pd.read_excel(uploaded_alpha7_neg)
    df_beta2_neg = pd.read_excel(uploaded_beta2_neg)

    # Aggiungi suffissi
    df_alpha7_neg = df_alpha7_neg.add_suffix("_alpha7")
    df_beta2_neg = df_beta2_neg.add_suffix("_beta2")

    # Unione orizzontale
    df_unito_neg = pd.concat([df_alpha7_neg, df_beta2_neg], axis=1)

    # Mostra un'anteprima
    st.subheader("Anteprima dati uniti VIP-negative")
    st.dataframe(df_unito_neg.head())

    # Esportazione in Excel
    output_filename_neg = "VIP_negative_unito.xlsx"
    df_unito_neg.to_excel(output_filename_neg, index=False)

    # Download
    with open(output_filename_neg, "rb") as f:
        st.download_button(
            label="📥 Scarica file unito VIP-negative",
            data=f,
            file_name=output_filename_neg,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Carica entrambi i file VIP-negative per procedere con l'unione.")
