import streamlit as st
import pandas as pd
from io import BytesIO

def convert_csv_to_xlsx(file):
    # Legge il CSV da file upload
    df = pd.read_csv(file)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

st.title("Convertitore CSV -> XLSX")

uploaded_files = st.file_uploader(
    "Carica uno o più file CSV",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} file caricati.")
    for file in uploaded_files:
        st.write(f"File: {file.name}")
        xlsx_data = convert_csv_to_xlsx(file)
        
        st.download_button(
            label=f"Scarica {file.name.replace('.csv', '.xlsx')}",
            data=xlsx_data,
            file_name=file.name.replace('.csv', '.xlsx'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
