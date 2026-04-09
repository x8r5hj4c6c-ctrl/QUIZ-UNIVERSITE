import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Matteo x M3.0", page_icon="🎓", layout="centered")

# --- BASE DE DONNÉES (QUESTIONS OFFICIELLES ARES) ---
# J'ai structuré les données pour que la réponse correcte soit mélangée dynamiquement
if 'db_ares' not in st.session_state:
    st.session_state.db_ares = {
        "Biologie": [
            {"q": "Quelle structure est absente dans une cellule animale mais présente dans une cellule végétale ?", "opts": ["Paroi cellulosique", "Mitochondrie", "Noyau", "Membrane plasmique"], "ans": "Paroi cellulosique"},
            {"q": "Le rôle principal des mitochondries est :", "opts": ["La respiration cellulaire", "La synthèse des protéines", "La photosynthèse", "Le stockage des graisses"], "ans": "La respiration cellulaire"},
            {"q": "Quelle est la base azotée spécifique à l'ARN ?", "opts": ["Uracile", "Thymine", "Adénine", "Cytosine"], "ans": "Uracile"},
            {"q": "Un nucléotide d'ADN est composé de :", "opts": ["Désoxyribose + Base azotée + Phosphate", "Ribose + Base azotée + Phosphate", "Acide aminé + Phosphate", "Glucose + Base azotée"], "ans": "Désoxyribose + Base azotée + Phosphate"},
            {"q": "La mitose produit :", "opts": ["Deux cellules filles identiques", "Quatre cellules haploïdes", "Deux gamètes", "Une cellule œuf"], "ans": "Deux cellules filles identiques"}
        ],
        "Chimie": [
            {"q": "Quelle est la configuration électronique du Carbone (Z=6) ?", "opts": ["1s² 2s² 2p²", "1s² 2s² 2p⁶", "1s² 2s²", "1s² 2p⁴"], "ans": "1s² 2s² 2p²"},
            {"q": "Quel est le pH d'une solution neutre à 25°C ?", "opts": ["7", "0", "14", "1"], "ans": "7"},
            {"q": "Le groupe fonctionnel -OH caractérise quelle famille ?", "opts": ["Les alcools", "Les aldéhydes", "Les cétones", "Les acides carboxyliques"], "ans": "Les alcools"},
            {"q": "La mole est l'unité de :", "opts": ["La quantité de matière", "La masse", "Le volume", "La pression"], "ans": "La quantité de matière"}
        ],
        "Physique": [
            {"q": "Un corps de 5 kg est soumis à une force de 20 N. Quelle est son accélération ?", "opts": ["4 m/s²", "100 m/s²", "0.25 m/s²", "15 m/s²"], "ans": "4 m/s²"},
            {"q": "La loi d'Ohm s'écrit :", "opts": ["U = R * I", "P = U * I", "V = d / t", "E = mc²"], "ans": "U = R * I"},
            {"q": "L'unité de la force dans le Système International est le :", "opts": ["Newton", "Joule", "Watt", "Pascal"], "ans": "Newton"}
        ],
        "Mathématiques": [
            {"q": "Quelle est la dérivée de f(x) = x² ?", "opts": ["2x", "x", "2", "x³/3"], "ans": "2x"},
            {"q": "La somme des angles internes d'un triangle est :", "opts": ["180°", "360°", "90°", "270°"], "ans": "180°"},
            {"q": "Quelle est la valeur de log10(100) ?", "opts": ["2", "10", "1", "0"], "ans": "2"}
        ]
    }

# --- INITIALISATION DU QUIZ ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0
    st.session_state.current_idx = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.current_options = []

def start_quiz(materia):
    questions = list(st.session_state.db_ares[materia])
    random.shuffle(questions)
    st.session_state.quiz_data = questions[:10]
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    prepare_question()

def prepare_question():
    # Cette fonction mélange les options pour que la bonne réponse ne soit pas toujours la première
    idx = st.session_state.current_idx
    if idx < len(st.session_state.quiz_data):
        opts = list(st.session_state.quiz_data[idx]['opts'])
        random.shuffle(opts)
        st.session_state.current_options = opts

# --- INTERFACE ---
st.title("🚀 Matteo x M3.0")

if not st.session_state.quiz_data or st.session_state.finished:
    st.subheader("Simulateur ARES 2018-2025")
    materia_scelta = st.selectbox("Choisissez votre matière :", list(st.session_state.db_ares.keys()))
    if st.button("Commencer le Quiz", use_container_width=True):
        start_quiz(materia_scelta)
        st.rerun()

else:
    idx = st.session_state.current_idx
    q = st.session_state.quiz_data[idx]
    
    st.write(f"**Question {idx + 1} sur {len(st.session_state.quiz_data)}**")
    st.progress(idx / len(st.session_state.quiz_data))
    st.markdown(f"### {q['q']}")

    # Formulaire de réponse
    with st.form(key=f"form_{idx}"):
        user_choice = st.radio("Options :", st.session_state.current_options)
        submit = st.form_submit_button("Valider la réponse")

    if submit and not st.session_state.submitted:
        st.session_state.submitted = True
        if user_choice == q['ans']:
            st.session_state.score += 1
            st.success("Correct ! ✅")
        else:
            st.error(f"Incorrect. La réponse était : {q['ans']} ❌")

    # Bouton de navigation
    if st.session_state.submitted:
        if st.button("Continuer ➡️", use_container_width=True):
            if idx + 1 < len(st.session_state.quiz_data):
                st.session_state.current_idx += 1
                st.session_state.submitted = False
                prepare_question() # Mélange les options de la question suivante
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

# Écran final
if st.session_state.finished:
    st.balloons()
    st.header("🏁 Score Final")
    st.metric("Résultat", f"{st.session_state.score} / 10")
    if st.button("Retour au menu"):
        st.session_state.quiz_data = []
        st.rerun()
