import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Matteo x M3.0", page_icon="🎓", layout="centered")

# --- BASE DE DONNÉES INTÉGRÉE (EXTRAITE DE VOS FICHIERS 2018-2025) ---
DB_ARES = {
    "Biologie": {
        "Cytologie & Génétique": [
            {"q": "Quelle structure est absente dans une cellule animale mais présente dans une cellule végétale ?", "opts": ["Paroi cellulosique", "Mitochondrie", "Noyau", "Membrane plasmique"], "ans": "Paroi cellulosique"},
            {"q": "Le rôle principal des mitochondries est :", "opts": ["La respiration cellulaire", "La synthèse des protéines", "La photosynthèse", "Le stockage des graisses"], "ans": "La respiration cellulaire"},
            {"q": "Quelle est la base azotée spécifique à l'ARN ?", "opts": ["Uracile", "Thymine", "Adénine", "Cytosine"], "ans": "Uracile"},
            {"q": "Un nucléotide d'ADN est composé de :", "opts": ["Désoxyribose + Base azotée + Phosphate", "Ribose + Base azotée + Phosphate", "Acide aminé + Phosphate", "Glucose + Base azotée"], "ans": "Désoxyribose + Base azotée + Phosphate"},
            {"q": "La mitose produit :", "opts": ["Deux cellules filles identiques", "Quatre cellules haploïdes", "Deux gamètes", "Une cellule œuf"], "ans": "Deux cellules filles identiques"},
            {"q": "Où se déroule la synthèse des protéines ?", "opts": ["Dans les ribosomes", "Dans le noyau", "Dans l'appareil de Golgi", "Dans les lysosomes"], "ans": "Dans les ribosomes"}
        ]
    },
    "Chimie": {
        "Générale & Organique": [
            {"q": "Quelle est la configuration électronique du Carbone (Z=6) ?", "opts": ["1s² 2s² 2p²", "1s² 2s² 2p⁶", "1s² 2s²", "1s² 2p⁴"], "ans": "1s² 2s² 2p²"},
            {"q": "Quel est le pH d'une solution neutre à 25°C ?", "opts": ["7", "0", "14", "1"], "ans": "7"},
            {"q": "Le groupe fonctionnel -OH caractérise quelle famille ?", "opts": ["Les alcools", "Les aldéhydes", "Les cétones", "Les acides carboxyliques"], "ans": "Les alcools"},
            {"q": "La mole est l'unité de :", "opts": ["La quantité de matière", "La masse", "Le volume", "La pression"], "ans": "La quantité de matière"},
            {"q": "Quelle est la formule de l'eau oxygénée ?", "opts": ["H2O2", "H2O", "HO2", "H3O+"], "ans": "H2O2"}
        ]
    },
    "Physique": {
        "Mécanique & Électricité": [
            {"q": "Un corps de 5 kg est soumis à une force de 20 N. Quelle est son accélération ?", "opts": ["4 m/s²", "100 m/s²", "0.25 m/s²", "15 m/s²"], "ans": "4 m/s²"},
            {"q": "La loi d'Ohm s'écrit :", "opts": ["U = R * I", "P = U * I", "V = d / t", "E = mc²"], "ans": "U = R * I"},
            {"q": "L'unité de la force dans le Système International est le :", "opts": ["Newton", "Joule", "Watt", "Pascal"], "ans": "Newton"},
            {"q": "L'énergie cinétique est donnée par :", "opts": ["1/2 mv²", "mgh", "F * d", "P * t"], "ans": "1/2 mv²"}
        ]
    },
    "Mathématiques": {
        "Algèbre & Géométrie": [
            {"q": "Quelle est la dérivée de f(x) = x² ?", "opts": ["2x", "x", "2", "x³/3"], "ans": "2x"},
            {"q": "La somme des angles internes d'un triangle est :", "opts": ["180°", "360°", "90°", "270°"], "ans": "180°"},
            {"q": "Quelle est la valeur de log10(100) ?", "opts": ["2", "10", "1", "0"], "ans": "2"},
            {"q": "Quelle est la solution de ln(x) = 0 ?", "opts": ["1", "e", "0", "10"], "ans": "1"}
        ]
    }
}

# --- LOGIQUE DE SESSION ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0
    st.session_state.current_idx = 0
    st.session_state.finished = False
    st.session_state.submitted = False

def start_quiz(materia):
    questions = []
    for cat in DB_ARES[materia]:
        questions.extend(DB_ARES[materia][cat])
    random.shuffle(questions)
    st.session_state.quiz_data = questions[:10]
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.submitted = False

# --- INTERFACE UTILISATEUR ---
st.title("🚀 Matteo x M3.0")
st.subheader("Simulateur Examen ARES")

if not st.session_state.quiz_data or st.session_state.finished:
    with st.expander("Configuration du Quiz", expanded=True):
        materia_scelta = st.selectbox("Choisissez une matière à étudier :", list(DB_ARES.keys()))
        if st.button("Commencer la Simulation", use_container_width=True):
            start_quiz(materia_scelta)
            st.rerun()

else:
    idx = st.session_state.current_idx
    q = st.session_state.quiz_data[idx]
    
    st.write(f"**Question {idx + 1} sur {len(st.session_state.quiz_data)}**")
    st.progress((idx) / len(st.session_state.quiz_data))
    
    # Affichage de la Question
    st.markdown(f"### {q['q']}")

    # Formulaire pour la réponse
    with st.form(key=f"ares_form_{idx}"):
        user_choice = st.radio("Sélectionnez l'option correcte :", q['opts'], key=f"radio_{idx}")
        submit_button = st.form_submit_button("Valider la réponse")

    # Gestion de la réponse (HORS DU FORMULAIRE)
    if submit_button:
        st.session_state.submitted = True
        if user_choice == q['ans']:
            st.session_state.score += 1
            st.toast("Correct !", icon="✅")
        else:
            st.toast("Incorrect !", icon="❌")

    # Feedback et Navigation
    if st.session_state.submitted:
        if user_choice == q['ans']:
            st.success(f"Excellent ! La réponse est correcte.")
        else:
            st.error(f"Dommage. La réponse correcte était : **{q['ans']}**")
        
        if st.button("Question Suivante ➡️", use_container_width=True):
            if idx + 1 < len(st.session_state.quiz_data):
                st.session_state.current_idx += 1
                st.session_state.submitted = False
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

# Fin du Quiz
if st.session_state.finished:
    st.balloons()
    st.header("🏁 Simulation Terminée")
    st.metric("Score Final", f"{st.session_state.score} / {len(st.session_state.quiz_data)}")
    
    if st.button("Recommencer un Quiz", use_container_width=True):
        st.session_state.quiz_data = []
        st.rerun()
