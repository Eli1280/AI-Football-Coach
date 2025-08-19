import json
import streamlit as st
import matplotlib.pyplot as plt

# Charger la base d’exercices
with open("json", "r", encoding="utf-8") as f:
    exercices = json.load(f)

def generer_seance(categorie, duree, focus):
    seance, total = [], 0
    for ex in exercices:
        if categorie == ex["categorie"] and focus in ex["objectifs"]:
            if total + ex["duree"] <= duree:
                seance.append(ex)
                total += ex["duree"]
    return seance

def dessiner_schema(exercice):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.set_title(exercice["nom"])

    # terrain simplifié
    ax.plot([0, 100, 100, 0, 0], [0, 0, 60, 60, 0], 'g-')
    ax.plot([50, 50], [0, 60], 'k--')

    # joueurs
    for j in range(5):
        ax.plot(20 + j*10, 30, 'ro')  # attaquants
        ax.plot(80 - j*10, 30, 'bo')  # défenseurs

    # flèche tir
    if exercice["tir_cage"]:
        ax.arrow(50, 30, 40, 0, head_width=3, color="red")

    return fig

# Interface Streamlit
st.title("⚽ Générateur de Séances d’Entraînement")

categorie = st.selectbox("Catégorie :", ["U13", "U15", "U17","senior"])
duree = st.slider("Durée de la séance (minutes)", 30, 120, 60, 5)
focus = st.selectbox("Focus :", ["tir", "technique", "jeu collectif"])

if st.button("Générer la séance"):
    seance = generer_seance(categorie, duree, focus)
    if not seance:
        st.warning("Aucun exercice trouvé pour ces paramètres.")
    else:
        for ex in seance:
            st.subheader(f"{ex['nom']} ({ex['duree']} min)")
            st.write(f"Joueurs : {ex['nb_joueurs']}, Matériel : {', '.join(ex['materiel'])}")
            fig = dessiner_schema(ex)
            st.pyplot(fig)
