import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Analisi VIP-positive", layout="wide")
st.title("🔬 Classificazione e analisi cellule VIP-positive (alpha7 e beta2)")

uploaded_file = st.file_uploader("Carica il file Excel unito:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Classifica le cellule
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

    # 🔢 Conteggi e percentuali singole
    counts_alpha7 = df['classification_alpha7'].value_counts()
    perc_alpha7 = counts_alpha7 / len(df) * 100

    counts_beta2 = df['classification_beta2'].value_counts()
    perc_beta2 = counts_beta2 / len(df) * 100

    # 💥 Somma weak+strong
    alpha7_pos = df['classification_alpha7'].isin(['weakPositive', 'strongPositive']).sum()
    beta2_pos = df['classification_beta2'].isin(['weakPositive', 'strongPositive']).sum()

    alpha7_pos_pct = alpha7_pos / len(df) * 100
    beta2_pos_pct = beta2_pos / len(df) * 100

    # 🔁 Combinazioni miste
    df['combo'] = df['classification_alpha7'] + " | " + df['classification_beta2']
    combo_counts = df['combo'].value_counts()
    combo_perc = combo_counts / len(df) * 100

    # 🧩 Pos+Pos combinato
    pos_combo_mask = df['classification_alpha7'].isin(['weakPositive', 'strongPositive']) & \
                     df['classification_beta2'].isin(['weakPositive', 'strongPositive'])
    pos_combo_pct = pos_combo_mask.sum() / len(df) * 100

    # 📊 GRAFICI
    st.subheader("📊 Distribuzione per classe")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Alpha7**")
        st.bar_chart(perc_alpha7)
    with col2:
        st.write("**Beta2**")
        st.bar_chart(perc_beta2)

    st.subheader("🥧 Grafici a torta")
    fig1, ax1 = plt.subplots()
    ax1.pie(perc_alpha7, labels=perc_alpha7.index, autopct='%1.1f%%')
    ax1.set_title("Alpha7")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.pie(perc_beta2, labels=perc_beta2.index, autopct='%1.1f%%')
    ax2.set_title("Beta2")
    st.pyplot(fig2)

    st.subheader("🧬 Combinazioni miste (alpha7 | beta2)")
    st.dataframe(pd.DataFrame({'Conteggio': combo_counts, 'Percentuale': combo_perc.round(2)}))
    st.bar_chart(combo_perc)
    st.subheader("🧪 Percentuale di doppie positive")

    doppie_positive = pos_combo_mask.sum()
    non_doppie = len(df) - doppie_positive

    fig_dp, ax_dp = plt.subplots()
    ax_dp.pie(
        [doppie_positive, non_doppie],
        labels=["Doppie positive", "Altre cellule"],
        autopct='%1.1f%%',
        colors=["#4CAF50", "#B0BEC5"]
    )
    ax_dp.set_title("Frazione di cellule doppie positive (alpha7 + beta2)")
    st.pyplot(fig_dp)
    # Grafico a barre della percentuale di doppie positive
    st.subheader("📊 Istogramma doppie positive vs altre cellule")

    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(
        ["Doppie positive", "Altre cellule"],
        [doppie_positive / len(df) * 100, non_doppie / len(df) * 100],
        color=["#4CAF50", "#B0BEC5"]
    )
    ax_bar.set_ylabel("Percentuale (%)")
    ax_bar.set_ylim(0, 100)
    ax_bar.set_title("Percentuale cellule doppie positive vs altre")
    st.pyplot(fig_bar)
    st.subheader("📈 Puncta distribution")
    col3, col4 = st.columns(2)
    with col3:
        if 'Count_alpha7' in df.columns:
            fig3, ax3 = plt.subplots()
            df['Count_alpha7'].hist(bins=30, ax=ax3)
            ax3.set_title("Distribuzione puncta Alpha7")
            st.pyplot(fig3)
        else:
            st.warning("Colonna 'Count_alpha7' non trovata.")

    with col4:
        if 'Count_beta2' in df.columns:
            fig4, ax4 = plt.subplots()
            df['Count_beta2'].hist(bins=30, ax=ax4)
            ax4.set_title("Distribuzione puncta Beta2")
            st.pyplot(fig4)
        else:
            st.warning("Colonna 'Count_beta2' non trovata.")

    # 📤 Esportazione Excel con riepilogo
    summary = {
        'alpha7_counts': counts_alpha7,
        'alpha7_perc': perc_alpha7.round(2),
        'beta2_counts': counts_beta2,
        'beta2_perc': perc_beta2.round(2),
        'alpha7_positive_pct': [alpha7_pos_pct],
        'beta2_positive_pct': [beta2_pos_pct],
        'double_positive_pct': [pos_combo_pct],
        'combo_counts': combo_counts,
        'combo_perc': combo_perc.round(2)
    }

    # Crea un file Excel con più fogli
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Classificato")
        pd.DataFrame({'Count': counts_alpha7, 'Percentuale': perc_alpha7}).to_excel(writer, sheet_name="Alpha7_stats")
        pd.DataFrame({'Count': counts_beta2, 'Percentuale': perc_beta2}).to_excel(writer, sheet_name="Beta2_stats")
        pd.DataFrame({'Percentuale_Positive': [alpha7_pos_pct]}, index=["Alpha7"]).to_excel(writer, sheet_name="Alpha7_Pos")
        pd.DataFrame({'Percentuale_Positive': [beta2_pos_pct]}, index=["Beta2"]).to_excel(writer, sheet_name="Beta2_Pos")
        pd.DataFrame({'Percentuale_Doppio_Positive': [pos_combo_pct]}).to_excel(writer, sheet_name="Double_Pos")
        combo_df = pd.DataFrame({'Count': combo_counts, 'Percentuale': combo_perc})
        combo_df.to_excel(writer, sheet_name="Combinazioni")

    output.seek(0)
    st.download_button(
        label="📥 Scarica Excel con tutti i risultati",
        data=output,
        file_name="analisi_vip_positive_completa.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Carica un file Excel con le colonne di classificazione per iniziare.")



