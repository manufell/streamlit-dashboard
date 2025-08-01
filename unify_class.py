import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Analisi VIP alpha7/beta2", layout="wide")
st.title("🔬 Analisi comparativa VIP-positive vs VIP-negative")

def carica_e_analizza(alpha7_file, beta2_file):
    df_alpha7 = pd.read_excel(alpha7_file).add_suffix('_alpha7')
    df_beta2 = pd.read_excel(beta2_file).add_suffix('_beta2')
    df = pd.concat([df_alpha7, df_beta2], axis=1)

    # Classificazione
    def classifica(row, prefix):
        if row.get(f'Classify_strongPositive_{prefix}', 0) == 1:
            return 'strongPositive'
        elif row.get(f'Classify_weakPositive_{prefix}', 0) == 1:
            return 'weakPositive'
        elif row.get(f'Classify_negative_{prefix}', 0) == 1:
            return 'negative'
        else:
            return 'unclassified'

    df['classification_alpha7'] = df.apply(lambda r: classifica(r, 'alpha7'), axis=1)
    df['classification_beta2'] = df.apply(lambda r: classifica(r, 'beta2'), axis=1)

    return df

def mostra_analisi(df, titolo):
    st.header(f"📁 Analisi {titolo}")
    
    st.subheader("📄 Anteprima")
    st.dataframe(df.head())

    # Conteggi e percentuali
    counts_a7 = df['classification_alpha7'].value_counts()
    perc_a7 = counts_a7 / len(df) * 100
    counts_b2 = df['classification_beta2'].value_counts()
    perc_b2 = counts_b2 / len(df) * 100

    pos_a7 = df['classification_alpha7'].isin(['weakPositive', 'strongPositive']).sum()
    pos_b2 = df['classification_beta2'].isin(['weakPositive', 'strongPositive']).sum()
    pct_pos_a7 = pos_a7 / len(df) * 100
    pct_pos_b2 = pos_b2 / len(df) * 100

    # Combinazioni
    df['combo'] = df['classification_alpha7'] + " | " + df['classification_beta2']
    combo_counts = df['combo'].value_counts()
    combo_perc = combo_counts / len(df) * 100

    # Doppie positive
    mask_dp = df['classification_alpha7'].isin(['weakPositive', 'strongPositive']) & \
              df['classification_beta2'].isin(['weakPositive', 'strongPositive'])
    pct_dp = mask_dp.sum() / len(df) * 100

    # Grafici
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Alpha7**")
        st.bar_chart(perc_a7)
    with col2:
        st.write("**Beta2**")
        st.bar_chart(perc_b2)

    fig1, ax1 = plt.subplots()
    ax1.pie(perc_a7, labels=perc_a7.index, autopct='%1.1f%%')
    ax1.set_title("Alpha7")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.pie(perc_b2, labels=perc_b2.index, autopct='%1.1f%%')
    ax2.set_title("Beta2")
    st.pyplot(fig2)

    st.subheader("🧬 Combinazioni")
    st.dataframe(pd.DataFrame({'Count': combo_counts, 'Percentuale': combo_perc.round(2)}))
    st.bar_chart(combo_perc)

    fig_dp, ax_dp = plt.subplots()
    ax_dp.pie([mask_dp.sum(), len(df)-mask_dp.sum()],
              labels=["Doppie positive", "Altre"],
              autopct='%1.1f%%', colors=["#4CAF50", "#B0BEC5"])
    ax_dp.set_title("Frazione di doppie positive")
    st.pyplot(fig_dp)

    return df, perc_a7, perc_b2, pct_dp

def confronto_finale(perc_a7_pos, perc_b2_pos, pct_dp_pos, perc_a7_neg, perc_b2_neg, pct_dp_neg):
    st.header("🔁 Confronto VIP-positive vs VIP-negative")

    for marker, pos, neg in zip(
        ['alpha7', 'beta2'],
        [perc_a7_pos, perc_b2_pos],
        [perc_a7_neg, perc_b2_neg]
    ):
        df_comp = pd.DataFrame({
            'VIP-positive': pos,
            'VIP-negative': neg
        }).reindex(['negative', 'weakPositive', 'strongPositive']).fillna(0)

        st.subheader(f"📊 {marker.upper()}")
        st.dataframe(df_comp.round(2))

        fig, ax = plt.subplots()
        df_comp.plot(kind='bar', ax=ax, color=['#2196F3', '#F44336'])
        ax.set_ylabel("Percentuale (%)")
        ax.set_title(f"Classificazione {marker}: VIP-positive vs VIP-negative")
        st.pyplot(fig)

    st.subheader("🧬 Confronto doppie positive")
    df_dp = pd.DataFrame({
        "Tipo": ["VIP-positive", "VIP-negative"],
        "Percentuale doppie positive": [pct_dp_pos, pct_dp_neg]
    })
    st.dataframe(df_dp)

    fig_dp_comp, ax_dp_comp = plt.subplots()
    ax_dp_comp.bar(["VIP-positive", "VIP-negative"],
                   [pct_dp_pos, pct_dp_neg],
                   color=["#4CAF50", "#B0BEC5"])
    ax_dp_comp.set_ylabel("Percentuale (%)")
    ax_dp_comp.set_title("Confronto doppie positive")
    st.pyplot(fig_dp_comp)

# --------------------
# CARICAMENTO FILE
# --------------------

st.sidebar.subheader("📥 Carica i 4 file Excel")

uploaded_alpha7_pos = st.sidebar.file_uploader("alpha7 - VIP-positive", type=["xlsx"])
uploaded_beta2_pos  = st.sidebar.file_uploader("beta2 - VIP-positive", type=["xlsx"])
uploaded_alpha7_neg = st.sidebar.file_uploader("alpha7 - VIP-negative", type=["xlsx"])
uploaded_beta2_neg  = st.sidebar.file_uploader("beta2 - VIP-negative", type=["xlsx"])

if uploaded_alpha7_pos and uploaded_beta2_pos and uploaded_alpha7_neg and uploaded_beta2_neg:
    # ANALISI VIP-POSITIVE
    df_pos = carica_e_analizza(uploaded_alpha7_pos, uploaded_beta2_pos)
    df_pos, perc_a7_pos, perc_b2_pos, pct_dp_pos = mostra_analisi(df_pos, "VIP-positive")

    # ANALISI VIP-NEGATIVE
    df_neg = carica_e_analizza(uploaded_alpha7_neg, uploaded_beta2_neg)
    df_neg, perc_a7_neg, perc_b2_neg, pct_dp_neg = mostra_analisi(df_neg, "VIP-negative")

    # CONFRONTO
    confronto_finale(perc_a7_pos, perc_b2_pos, pct_dp_pos, perc_a7_neg, perc_b2_neg, pct_dp_neg)

       # ESPORTAZIONE DATI COMPLETI
    st.header("📤 Esporta file Excel con tutte le tabelle")

    export_all = BytesIO()
    with pd.ExcelWriter(export_all, engine='openpyxl') as writer:
        # VIP-positive
        df_pos.to_excel(writer, index=False, sheet_name="VIP_Positive_Classificato")
        perc_a7_pos.to_frame("Percentuale").to_excel(writer, sheet_name="Alpha7_stats_Pos")
        perc_b2_pos.to_frame("Percentuale").to_excel(writer, sheet_name="Beta2_stats_Pos")
        df_pos['combo'].value_counts().to_frame("Count").assign(Percentuale=lambda df: df['Count'] / df['Count'].sum() * 100)\
            .to_excel(writer, sheet_name="Combinazioni_Pos")
        pd.DataFrame({"Percentuale_Doppie_Pos": [pct_dp_pos]}).to_excel(writer, sheet_name="Double_Pos_Pos")

        # VIP-negative
        df_neg.to_excel(writer, index=False, sheet_name="VIP_Negative_Classificato")
        perc_a7_neg.to_frame("Percentuale").to_excel(writer, sheet_name="Alpha7_stats_Neg")
        perc_b2_neg.to_frame("Percentuale").to_excel(writer, sheet_name="Beta2_stats_Neg")
        df_neg['combo'].value_counts().to_frame("Count").assign(Percentuale=lambda df: df['Count'] / df['Count'].sum() * 100)\
            .to_excel(writer, sheet_name="Combinazioni_Neg")
        pd.DataFrame({"Percentuale_Doppie_Pos": [pct_dp_neg]}).to_excel(writer, sheet_name="Double_Pos_Neg")

        # Confronto Alpha7
        pd.DataFrame({
            'VIP-positive': perc_a7_pos,
            'VIP-negative': perc_a7_neg
        }).reindex(['negative', 'weakPositive', 'strongPositive']).fillna(0)\
         .to_excel(writer, sheet_name="Confronto_Alpha7")

        # Confronto Beta2
        pd.DataFrame({
            'VIP-positive': perc_b2_pos,
            'VIP-negative': perc_b2_neg
        }).reindex(['negative', 'weakPositive', 'strongPositive']).fillna(0)\
         .to_excel(writer, sheet_name="Confronto_Beta2")

        # Confronto doppie positive
        pd.DataFrame({
            "Tipo": ["VIP-positive", "VIP-negative"],
            "Percentuale_doppie_positive": [pct_dp_pos, pct_dp_neg]
        }).to_excel(writer, sheet_name="Confronto_Double_Pos", index=False)

    st.download_button(
        label="📥 Scarica Excel riepilogativo completo",
        data=export_all.getvalue(),
        file_name="Analisi_VIP_completa.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
