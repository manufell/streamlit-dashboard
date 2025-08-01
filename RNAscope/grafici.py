import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import tempfile
import os

st.title("📊 Visualizzazione grafici e salvataggio in PDF")

uploaded_file = st.file_uploader("Carica un file Excel con le medie", type=["xlsx"])

if uploaded_file:
    sheets = pd.read_excel(uploaded_file, sheet_name=None)

    # File PDF temporaneo
    tmp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmp_dir, "grafici_output.pdf")
    pdf_pages = PdfPages(pdf_path)

    for sheet_name, df in sheets.items():
        st.subheader(f"🧾 Foglio: {sheet_name}")

        df = df.dropna(axis=1, how='all')
        df = df.select_dtypes(include='number')

        if df.empty:
            st.warning("⚠️ Nessun dato numerico trovato.")
            continue

        values = df.iloc[0]

        fig, ax = plt.subplots()

        # Istogrammi per fogli Count_*, escludendo Count_Combinazioni
        if sheet_name.startswith("Count_") and sheet_name != "Count_Combinazioni":
            values.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_ylabel("mean")
            ax.set_title(f"Istogramma - {sheet_name}")

        # Torta per Percentuale_*_stats
        elif sheet_name.startswith("Percentuale_") and sheet_name.endswith("_stats"):
            values.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            ax.set_ylabel("")
            ax.set_title(f"Pie chart - {sheet_name}")

        # Torta per Double_Pos
        elif sheet_name == "Percentuale_Double_Pos":
            percent = values.sum()
            altri = 100 - percent
            ax.pie([percent, altri],
                   labels=["Double_Pos", "non-Double_Pos"],
                   autopct='%1.1f%%',
                   startangle=90)
            ax.set_title("Double_Pos %")

        # Torta per alpha7_Pos
        elif sheet_name == "Percentuale_Alpha7_Pos":
            percent = values.sum()
            altri = 100 - percent
            ax.pie([percent, altri],
                   labels=["alpha7_Pos", "alpha7_Neg"],
                   autopct='%1.1f%%',
                   startangle=90)
            ax.set_title("alpha7_Pos %")

        # Torta per beta2_Pos
        elif sheet_name == "Percentuale_Beta2_Pos":
            percent = values.sum()
            altri = 100 - percent
            ax.pie([percent, altri],
                   labels=["beta2_Pos", "beta2_Neg"],
                   autopct='%1.1f%%',
                   startangle=90)
            ax.set_title("beta2_Pos %")

        else:
            plt.close(fig)
            continue

        # Mostra in Streamlit
        st.pyplot(fig)

        # Salva nel PDF
        pdf_pages.savefig(fig)
        plt.close(fig)

    pdf_pages.close()

    # Offri download del PDF
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Scarica tutti i grafici in PDF", f, file_name="grafici_output.pdf")