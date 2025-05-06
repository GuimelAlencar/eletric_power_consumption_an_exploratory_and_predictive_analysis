# Electric Power Consumption Analysis Project

## Overview
This project is a comprehensive data analysis initiative designed to explore the **full lifecycle of data processing**, from ingestion to actionable insights, using the [Electric Power Consumption Dataset](https://www.kaggle.com/datasets/fedesoriano/electric-power-consumption) from Kaggle.  

The goal is to **develop professional-grade analytical workflows** while integrating modern tools for documentation, visualization, and deployment. The project structure accommodates:  
- **Data exploration** (EDA, temporal pattern analysis).  
- **Technical documentation** (methodologies, validation processes).  
- **Insight synthesis** (statistical conclusions, business recommendations).  
- **Digital delivery** (interactive dashboard, API for programmatic access).  

---

## Objectives  
### 1. **Data Analysis & Exploration**  
- Perform end-to-end analysis: ingestion, validation, processing, and aggregation.  
- Investigate temporal patterns, external variable impacts, and regional comparisons.  

### 2. **Documentation & Reproducibility**  
- Maintain **technical documentation** for all processes (e.g., data pipelines, validation rules).  
- Publish **insight reports** with actionable conclusions.  

### 3. **Deployment & Accessibility**  
- Build a **[Streamlit](https://streamlit.io/) dashboard** for interactive visualization.  
- Develop a **[FastAPI](https://fastapi.tiangolo.com/)** backend to enable programmatic data access.  

---

## Methodologies  
### Data Pipeline  
- **Ingestion**: Automated data loading (CSV, APIs) with error handling.  
- **Validation**: Schema checks using `pandera` or `pydantic`.  
- **Processing**: Time-series resampling, outlier detection (`scipy`/`statsmodels`).  

### Analysis  
- **Exploratory Data Analysis (EDA)**: Visualizations with `plotly`/`seaborn`.  
- **Statistical Testing**: Hypothesis testing (`scipy.stats`), correlation analysis.  

### Deployment  
- **API**: RESTful endpoints with FastAPI (OpenAPI docs, async support).  
- **Dashboard**: Streamlit with caching (`@st.cache_data`) for performance.  

---

## Frameworks & Tools  
### Core Stack  
- **Python**: `pandas`, `numpy`, `scikit-learn`.  
- **Visualization**: `plotly`, `matplotlib`, `altair`.  
- **Documentation**: `JupyterBook`, `Quarto`, or `MkDocs`.  

### Versioning & Collaboration  
- **Git**: Repository structure following [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).  
  - Branches: `main` (production), `dev` (staging), feature branches.  
  - Hooks: Pre-commit hooks to strip notebook outputs (`nbstripout`).  
- **DVC**: Data versioning for processed datasets.  
- **CI/CD**: GitHub Actions for testing/linting (`ruff`, `black`).  

### Infrastructure  
- **Containerization**: Docker for reproducibility.  
- **API Deployment**: Uvicorn + FastAPI (scalable via `gunicorn`).  

---

## Expected Outcomes  
1. **Technical Artifacts**:  
   - Modular codebase (`notebooks/` for exploration, `src/` for production code).  
   - Automated tests (`pytest`).  
2. **Deliverables**:  
   - Interactive dashboard (Streamlit).  
   - API documentation (Swagger UI via FastAPI).  
3. **Knowledge Outputs**:  
   - Published reports (PDF/HTML via Quarto).  
   - Reusable project template for future analyses.  

---

## Inspiration & References  
- [Netflix Data Engineering Blogs](https://netflixtechblog.com/)  
- [Spotify’s Data Visualization Practices](https://engineering.atspotify.com/)  
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/)  


## Project Structure:
´´´
meu_projeto/
├── data/
│   ├── raw/                   # Dados brutos (imutáveis)
│   ├── processed/             # Dados processados (versionados com DVC)
│   └── external/              # Dados externos (ex: APIs, CSV públicos)
│
├── docs/
│   ├── technical/             # Documentação técnica (Sphinx/MkDocs)
│   └── insights/              # Relatórios de conclusões (JupyterBook/Quarto)
│
├── notebooks/
│   ├── 01_eda/                # Análise exploratória
│   ├── 02_processing/         # Processamento e agregação
│   └── 03_visualization/      # Visualizações e padrões temporais
│
├── src/
│   ├── data_pipeline/         # Scripts de ingestão, validação, etc.
│   ├── dashboard/             # Código do Streamlit
│   ├── api/                   # FastAPI (endpoints)
│   └── utils/                 # Funções auxiliares (ex: plotters, loaders)
│
├── tests/                     # Testes unitários e de integração
├── .github/                   # CI/CD (GitHub Actions)
├── Dockerfile                 # Containerização
├── requirements.txt           # Dependências principais
├── pyproject.toml             # Configuração do Poetry (opcional)
└── README.md                  # Visão geral do projeto
´´´