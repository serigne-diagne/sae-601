import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px



# Configuration de la page avec un layout large
st.set_page_config(layout="wide", page_title="Analyse des Salaires en Data Science")

# Création d'un conteneur pour centrer le contenu
with st.container():
    # Titre principal avec un style accrocheur
    st.markdown("""
        <h1 style='text-align: center; color: #1E88E5; padding: 20px;'>
            🌟 Analyse des Salaires en Data Science 🌟
        </h1>
        """, unsafe_allow_html=True)
    
    # Sous-titre avec les noms des auteurs
    st.markdown("""
        <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px;'>
            <h3>Réalisé par :</h3>
            <p style='font-size: 18px;'>
                <b>BIKOUTA NSINDA Auxane</b> & <b>DIAGNE Pape Serigne</b>
            </p>
        </div>
        <br>
        """, unsafe_allow_html=True)

# Ligne de séparation
st.markdown("---")


# Chargement des données
df = pd.read_csv("ds_salaries.csv")

# Création de la barre de navigation
pages = {
    "📊 Vue d'ensemble": "overview",
    "🇫🇷 Analyse France": "france_analysis",
    "📈 Tendances": "trends",
    "🔗 Corrélations": "correlations",
    "📊 Évolution temporelle": "time_evolution",
    "💼 Analyse par expérience": "experience_analysis",
    "🏢 Télétravail": "remote_analysis",
    "🔍 Filtres avancés": "advanced_filters"
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", list(pages.keys()))

# Vue d'ensemble
if page == "📊 Vue d'ensemble":
    st.title("📊 Visualisation des Salaires en Data Science")
    st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")
    
    st.subheader("📌 Statistiques générales")
    description = df.describe()
    st.dataframe(description)

# Analyse France
elif page == "🇫🇷 Analyse France":
    st.subheader("📈 Distribution des salaires en France")
    df_france = df[df['employee_residence'] == 'FR']
    figfr = px.box(df_france, x='job_title', y='salary_in_usd', color='experience_level',
                   title="Distribution des salaires en France par poste et niveau d'expérience")
    st.plotly_chart(figfr)

# Tendances
elif page == "📈 Tendances":
    st.subheader("📈 Analyse des tendances de salaires par catégorie")
    box = ['experience_level', 'employment_type', 'job_title', 'company_location']
    selected_box = st.selectbox("Sélectionnez une catégorie :", box)
    salaire_moyen = df.groupby(selected_box)['salary_in_usd'].mean().reset_index()
    
    fig = px.bar(salaire_moyen, x=selected_box, y='salary_in_usd',
                 title=f"Salaire moyen par {selected_box}")
    st.plotly_chart(fig)
    st.dataframe(salaire_moyen)

# Corrélations
elif page == "🔗 Corrélations":
    st.subheader("🔗 Corrélations entre variables numériques")
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    st.pyplot(fig)

# Évolution temporelle
elif page == "📊 Évolution temporelle":
    st.subheader("📊 Évolution des salaires pour les postes les plus courants")
    
    # Sélection des 10 postes les plus courants
    top_jobs = df['job_title'].value_counts().nlargest(10).index
    df_top_jobs = df[df['job_title'].isin(top_jobs)]
    
    # Calcul du salaire moyen par an pour chaque poste
    salary_evolution = df_top_jobs.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
    
    fig = px.line(salary_evolution, x='work_year', y='salary_in_usd', color='job_title',
                  title="Évolution des salaires par poste")
    st.plotly_chart(fig)

# Analyse par expérience
elif page == "💼 Analyse par expérience":
    st.subheader("💼 Salaire médian par expérience et taille d'entreprise")
    
    median_salary = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()
    fig = px.bar(median_salary, x='experience_level', y='salary_in_usd', color='company_size',
                 barmode='group', title="Salaire médian par niveau d'expérience et taille d'entreprise")
    st.plotly_chart(fig)

# Analyse du télétravail
elif page == "🏢 Télétravail":
    st.subheader("🏢 Impact du télétravail sur les salaires")
    
    # Calcul du salaire moyen par pays et type de travail
    remote_impact = df.groupby(['company_location', 'remote_ratio'])['salary_in_usd'].mean().reset_index()
    
    # Création d'une catégorie plus lisible pour remote_ratio
    remote_impact['remote_type'] = remote_impact['remote_ratio'].map({
        0: 'Sur site',
        50: 'Hybride',
        100: 'Full remote'
    })
    
    fig = px.bar(remote_impact, x='company_location', y='salary_in_usd', color='remote_type',
                 title="Salaire moyen par pays et type de travail",
                 barmode='group')
    st.plotly_chart(fig)

# Filtres avancés
elif page == "🔍 Filtres avancés":
    st.subheader("🔍 Filtres avancés")
    
    # Filtres par expérience et taille d'entreprise
    col1, col2 = st.columns(2)
    with col1:
        selected_exp = st.multiselect(
            "Sélectionnez le niveau d'expérience",
            options=df['experience_level'].unique(),
            default=df['experience_level'].unique()
        )
    
    with col2:
        selected_size = st.multiselect(
            "Sélectionnez la taille d'entreprise",
            options=df['company_size'].unique(),
            default=df['company_size'].unique()
        )
    
    # Filtre par plage de salaire
    salary_range = st.slider(
        "Sélectionnez une plage de salaire (USD)",
        0, int(df['salary_in_usd'].max()), (0, int(df['salary_in_usd'].max()))
    )
    
    # Application des filtres
    filtered_df = df[
        (df['experience_level'].isin(selected_exp)) &
        (df['company_size'].isin(selected_size)) &
        (df['salary_in_usd'].between(salary_range[0], salary_range[1]))
    ]
    
    st.write(f"Nombre d'entrées filtrées : {len(filtered_df)}")
    st.dataframe(filtered_df)