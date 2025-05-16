import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from importer import load_dataset_from_kaggle
from checker import check_dataset
from processor import process_dataframe


@st.cache_data
def load_data():
    df = load_dataset_from_kaggle(
        dataset_address="fedesoriano/electric-power-consumption",
        file_name="powerconsumption.csv",
    )
    return df


@st.cache_data
def process_data(df, freq):
    processed_df = process_dataframe(df, freq)
    return processed_df


st.header("Dashboard")

raw_data = load_data()

processed_data = process_data(raw_data, "7d")

if st.checkbox("Show raw data"):
    tab1, tab2 = st.tabs(["Raw Data", "Processed Data"])

    with tab1:
        raw_data = load_data()
        st.write(raw_data)

    with tab2:
        processed_data_report = check_dataset(processed_data, [10, 15, 10])

        # Pre-calcular todos os dados estatísticos necessários para evitar redundância
        columns_without_datetime = [
            k for k in processed_data_report["describe"] if k != "Datetime"
        ]
        stats_data = {}
        percentiles_data = {}
        histograms_data = {}

        for col in columns_without_datetime:
            stats_data[col] = processed_data_report["describe"][col]
            percentiles_data[col] = {
                "q1": np.percentile(processed_data[col], 25),
                "median": np.median(processed_data[col]),
                "q3": np.percentile(processed_data[col], 75),
            }
            histograms_data[col] = np.histogram(processed_data[col], bins=30)[0]

        st.write(processed_data)

        if st.checkbox("Show data report"):
            # 1 - Metadados como expander com column_config para melhor visualização
            with st.expander("📦 Metadados do Dataset"):
                st.header("📦 Metadados do Dataset")

                # Criar um DataFrame para exibir metadados com column_config
                metadata_df = pd.DataFrame(
                    {
                        "Métrica": ["Linhas", "Colunas", "Data Inicial", "Data Final"],
                        "Valor": [
                            f"{processed_data_report['shape'][0]:,}",
                            f"{processed_data_report['shape'][1]}",
                            processed_data_report["samples"]["head"][0]["Datetime"],
                            processed_data_report["samples"]["tail"][-1]["Datetime"],
                        ],
                    }
                )

                # Configuração de coluna para melhor exibição
                st.dataframe(
                    metadata_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Métrica": st.column_config.TextColumn(
                            "Informação",
                            help="Metadados do conjunto de dados",
                            width="medium",
                        ),
                        "Valor": st.column_config.TextColumn("Valor", width="medium"),
                    },
                )

            # 2 - Amostras de Dados como expander
            with st.expander("📄 Amostras de Dados"):
                st.header("📄 Amostras de Dados")
                tab1, tab2, tab3 = st.tabs(["Início", "Meio", "Fim"])
                with tab1:
                    st.dataframe(
                        pd.DataFrame(processed_data_report["samples"]["head"]),
                        height=250,
                    )
                with tab2:
                    st.dataframe(
                        pd.DataFrame(processed_data_report["samples"]["body"]),
                        height=250,
                    )
                with tab3:
                    st.dataframe(
                        pd.DataFrame(processed_data_report["samples"]["tail"]),
                        height=250,
                    )

            # 4 - Qualidade de Dados contendo também os detalhes de outliers
            with st.expander("🧼 Qualidade de Dados"):
                st.header("Qualidade de Dados")

                # Seção de Métricas principais - com títulos mais descritivos
                st.subheader("Resumo")

                # Métricas de qualidade em cards com cores e descrições
                col1, col2, col3 = st.columns(3)
                with col1:
                    with st.container(border=True):
                        st.metric(
                            "Total de Dados Ausentes",
                            processed_data_report["missing_values"]["total"],
                        )
                        st.caption(
                            f"Representa {processed_data_report['missing_values'].get('percent', '0%')} do conjunto de dados"
                        )

                with col2:
                    with st.container(border=True):
                        st.metric(
                            "Total de Duplicatas",
                            processed_data_report["duplicates"]["total"],
                        )
                        st.caption(
                            f"Representa {processed_data_report['duplicates'].get('percent', '0%')} do conjunto de dados"
                        )

                with col3:
                    with st.container(border=True):
                        st.metric(
                            "Colunas com Outliers",
                            len(processed_data_report["outliers"]),
                        )
                        total_outliers = (
                            sum(
                                info["outliers"]
                                for info in processed_data_report["outliers"].values()
                            )
                            if processed_data_report["outliers"]
                            else 0
                        )
                        st.caption(
                            f"Total de {total_outliers} pontos de dados identificados como outliers"
                        )
                # Se não existirem outliers, informar ao usuário com destaque
                if len(processed_data_report["outliers"]) == 0:
                    st.success(
                        "✅ Não foram encontrados outliers nos dados. Isso sugere uma distribuição adequada dos valores."
                    )
                else:
                    # Criar DataFrame para exibir outliers com column_config
                    outliers_data = []
                    for col, info in processed_data_report["outliers"].items():
                        outliers_data.append(
                            {
                                "Coluna": col,
                                "Quantidade": info["outliers"],
                                "Percentual": info["percent"],
                                "Limite Inferior": info["limits"][0],
                                "Limite Superior": info["limits"][1],
                            }
                        )

                    if outliers_data:
                        outliers_df = pd.DataFrame(outliers_data)

                        # Ordenar por quantidade de outliers (decrescente)
                        outliers_df = outliers_df.sort_values(
                            by="Quantidade", ascending=False
                        )

                        st.dataframe(
                            outliers_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Coluna": st.column_config.TextColumn(
                                    "Coluna",
                                    help="Nome da coluna com outliers",
                                    width="medium",
                                ),
                                "Quantidade": st.column_config.NumberColumn(
                                    "Total",
                                    help="Número de outliers encontrados",
                                    format="%d",
                                    width="small",
                                ),
                                "Percentual": st.column_config.NumberColumn(
                                    "Porcentagem",
                                    help="Percentual de outliers em relação ao total de dados",
                                    width="small",
                                    format="percent",
                                ),
                                "Limite Inferior": st.column_config.NumberColumn(
                                    "Limite Inferior",
                                    help="Valores abaixo deste limite são considerados outliers",
                                    format="localized",
                                    width="small",
                                ),
                                "Limite Superior": st.column_config.NumberColumn(
                                    "Limite Superior",
                                    help="Valores acima deste limite são considerados outliers",
                                    format="localized",
                                    width="small",
                                ),
                            },
                        )

            # 3 - Análise Estatística como expander com duas colunas (info e gráfico)
            with st.expander("📈 Análise Estatística"):
                col_left, col_right = st.columns([1, 2])

                with col_left:
                    # Identificar colunas que não são de data/hora
                    columns_without_datetime = []
                    for col in processed_data.columns:
                        # Verifica se a coluna não é do tipo datetime
                        if not pd.api.types.is_datetime64_any_dtype(
                            processed_data[col]
                        ):
                            columns_without_datetime.append(col)

                    selected_col = st.selectbox(
                        "Selecione a coluna:", options=columns_without_datetime
                    )

                    if selected_col:
                        stats_dict = {
                            "🟪 Média": stats_data[selected_col]["mean"],
                            "🟧 Moda": processed_data[selected_col].mode()[0],
                            "🟦 Mediana": percentiles_data[selected_col]["median"],
                            " Desvio Padrão": stats_data[selected_col]["std"],
                            "🟩 Mínimo": stats_data[selected_col]["min"],
                            "🟥 Máximo": stats_data[selected_col]["max"],
                            "🟫 Q1": percentiles_data[selected_col]["q1"],
                            "🟨 Q3": percentiles_data[selected_col]["q3"],
                        }

                        stats_df = pd.DataFrame(
                            {
                                "Estatística": list(stats_dict.keys()),
                                "Valor": [
                                    f"{value:.2f}" for value in stats_dict.values()
                                ],
                            }
                        )
                        st.dataframe(
                            stats_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Estatística": st.column_config.TextColumn(
                                    "Métrica", help="Medidas estatísticas", width=100
                                ),
                                "Valor": st.column_config.TextColumn(
                                    "Valor", width=100
                                ),
                            },
                        )

                with col_right:
                    # Gráfico ocupando todo o espaço da coluna
                    st.subheader("Distribuição")
                    hist_data = histograms_data[selected_col]

                    # Verificando o tipo de dados do histograma e adaptando conforme necessário
                    if isinstance(hist_data, np.ndarray):
                        # Se for array numpy, precisamos calcular os bins para o histograma
                        counts, bins = np.histogram(
                            processed_data[selected_col].dropna(), bins=20
                        )
                        # Usando o centro de cada bin como valor x
                        bin_centers = 0.5 * (bins[:-1] + bins[1:])
                        # Criando DataFrame para Plotly
                        hist_df = pd.DataFrame(
                            {"valor": bin_centers, "contagem": counts}
                        )
                    else:
                        # Caso já seja um DataFrame ou Series
                        hist_df = pd.DataFrame(
                            {"valor": hist_data.index, "contagem": hist_data.values}
                        )

                    fig = make_subplots()

                    # Adicionando barras do histograma
                    fig.add_trace(
                        go.Bar(
                            x=hist_df["valor"],
                            y=hist_df["contagem"],
                            marker_color="white",
                        )
                    )

                    # Cores para as linhas verticais (correspondendo aos emojis)
                    line_colors = {
                        "🟪 Média": "purple",
                        "🟧 Moda": "orange",
                        "🟦 Mediana": "blue",
                        "🟩 Mínimo": "green",
                        "🟥 Máximo": "red",
                        "🟫 Q1": "brown",
                        "🟨 Q3": "gold",
                    }

                    # Adicionando linhas verticais para cada estatística (exceto desvio padrão)
                    for stat_name, stat_value in stats_dict.items():
                        if (
                            "Desvio Padrão" not in stat_name
                        ):  # Não incluímos o desvio padrão como linha vertical
                            fig.add_vline(
                                x=stat_value,
                                line_color=line_colors.get(stat_name, "gray"),
                            )

                    # Configurando o layout
                    fig.update_layout(
                        height=400,
                    )

                    # Exibindo o gráfico
                    st.plotly_chart(fig, use_container_width=True)

            with st.expander("🔄 Análise de Correlação"):
                st.header("Matriz de Correlação de Pearson")

                # Calcular a matriz de correlação apenas para colunas numéricas
                numeric_cols = processed_data.select_dtypes(include=[np.number]).columns
                corr_matrix = processed_data[numeric_cols].corr()

                # Criar heatmap com plotly
                fig = go.Figure(
                    data=go.Heatmap(
                        z=corr_matrix,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale="RdBu",
                        zmin=-1,
                        zmax=1,
                        text=np.round(corr_matrix, 2),
                        texttemplate="%{text}",
                        textfont={"size": 10},
                        hoverongaps=False,
                    )
                )

                fig.update_layout(
                    height=600,
                    width=800,
                )

                st.plotly_chart(fig, use_container_width=True)

# Create visualization for zones consumption
st.header("Consumo de Energia por Zona")
# Prepare the data
fig = go.Figure()
# Add bars for each zone
zones = ["Zone1", "Zone2", "Zone3"]
colors = ["green", "orange", "blue"]
line_colors = ["darkgreen", "darkorange", "darkblue"]
# Add mean lines (valores por período)
for zone, color in zip(zones, line_colors):
    fig.add_trace(
        go.Scatter(
            name=f"Média {zone}",
            x=processed_data["Datetime"],
            y=processed_data[f"TotalPowerConsumption_{zone}"],  # Coluna corrigida
            mode="lines",
            line=dict(color=color, width=1),
            showlegend=True,
        )
    )
# Update layout
fig.update_layout(
    barmode="group",
    xaxis_title="Data",
    yaxis_title="Consumo de Energia (kW)",
    legend_title="Zonas",
)
st.plotly_chart(fig, use_container_width=True)
