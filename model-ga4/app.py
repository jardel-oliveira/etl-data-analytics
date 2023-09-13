import pandas as pd

# Carregando arquivo do google analytics
data = pd.read_csv("")

# Promovendo cabecalhos
data = data.set_index(["Date", "Campaign", "Source", "Medium", "Ad content"])

# Converter os tipos
data["Sessions"] = pd.to_numeric(data["Sessions"])
data["Bounce rate"] = pd.to_numeric(data["Bounce rate"])
data["Users"] = pd.to_numeric(data["Users"])
data["New users"] = pd.to_numeric(data["New users"])
data["Pageviews"] = pd.to_numeric(data["Pageviews"])
data["Avg. time on page (sec)"] = pd.to_numeric(data["Avg. time on page (sec)"])

# Filtrando dados por ad content
filtered_data = data[data["Ad content"].str.contains("criterio_ad_content")]

# Convertendo as colunas de origem
filtered_data["Source"] = filtered_data["Source"].str.upper()

# Normalizando nomenclatura
filtered_data["Source"] = filtered_data["Source"].replace("Facebook", "Meta")
filtered_data["Source"] = filtered_data["Source"].replace("Instagram", "Meta")

# Duplicando colunas
duplicated_data = filtered_data.copy()
duplicated_data["Ad content - Copiar"] = duplicated_data["Ad content"]

# Split Ad content por caracter (-)
split_data = duplicated_data.set_index("Ad content - Copiar").unstack(fill_value=0)

# Conversão de tipo 
split_data["Ad content - Copiar.1"] = pd.to_string(split_data["Ad content - Copiar.1"])
split_data["Ad content - Copiar.2"] = pd.to_numeric(split_data["Ad content - Copiar.2"])

# Add coluna com a fase (estágio da campanha)
split_data["Fase da Campanha"] = pd.Series(
    [
        "Fase 1" if value < 93 else "Fase 2"
        for value in split_data["Ad content - Copiar.2"]
    ]
)

# Removendo dados
final_data = split_data.drop(["Ad content - Copiar.1", "Ad content - Copiar.2"], axis=1)

# Análise dos dados
print(final_data)