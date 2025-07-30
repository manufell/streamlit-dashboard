

import pandas as pd

# Carica i due file Excel
df_alpha7 = pd.read_excel("VIP_negative_alpha7.xlsx")
df_beta2 = pd.read_excel("VIP_negative_beta2.xlsx")

# Opzionale: rinomina le colonne duplicate aggiungendo un suffisso
df_alpha7 = df_alpha7.add_suffix("_alpha7")
df_beta2 = df_beta2.add_suffix("_beta2")

# Rimuovi colonne ridondanti duplicate tra i due (se presenti)
# Ad esempio, se entrambi hanno 'ImageNumber_alpha7' e 'ImageNumber_beta2' con lo stesso contenuto, puoi tenerne solo una

# Unisci le due tabelle orizzontalmente (sulle righe)
df_unito = pd.concat([df_alpha7, df_beta2], axis=1)

# Esporta il risultato (opzionale)
df_unito.to_excel("VIP_negative_unito.xlsx", index=False)

# Visualizza le prime righe per controllo
print(df_unito.head())




