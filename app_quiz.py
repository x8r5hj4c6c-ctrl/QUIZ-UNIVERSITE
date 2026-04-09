import streamlit as st
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="ARES Pro 2018-2025", page_icon="🧪", layout="centered")

# --- DATABASE INTEGRATO ---
# Qui ho inserito una selezione rappresentativa estratta dai tuoi file HTML
DB_ARES = {
    "Biologie": {
        "Cytologie & Histologie": [
            {"q": "Quelle structure est absente dans une cellule animale mais présente dans une cellule végétale ?", "opts": ["Paroi cellulosique", "Mitochondrie", "Noyau", "Membrane plasmique"], "ans": "Paroi cellulosique"},
            {"q": "Le rôle principal des mitochondries est :", "opts": ["La respiration cellulaire", "La synthèse des protéines", "La photosynthèse", "Le stockage des graisses"], "ans": "La respiration cellulaire"},
            {"q": "L'organite responsable de la synthèse des protéines est :", "opts": ["Le ribosome", "Le lysosome", "L'appareil de Golgi", "Le chloroplaste"], "ans": "Le ribosome"},
            {"q": "La membrane plasmique est principalement composée de :", "opts": ["Phospholipides et protéines", "Triglycérides", "Amidon", "Acides nucléiques"], "ans": "Phospholipides et protéines"}
        ],
        "Génétique & Moléculaire": [
            {"q": "Quelle est la base azotée spécifique à l'ARN ?", "opts": ["Uracile", "Thymine", "Adénine", "Cytosine"], "ans": "Uracile"},
            {"q": "Un nucléotide d'ADN est composé de :", "opts": ["Désoxyribose + Base azotée + Phosphate", "Ribose + Base azotée + Phosphate", "Acide aminé + Phosphate", "Glucose + Base azotée"], "ans": "Désoxyribose + Base azotée + Phosphate"},
            {"q": "Si un brin d'ADN a la séquence ATGC, le brin complémentaire sera :", "opts": ["TACG", "UACG", "GCTA", "ATGC"], "ans": "TACG"}
        ]
    },
    "Chimie": {
        "Inorganique & Générale": [
            {"q": "Quelle est la configuration électronique du Carbone (Z=6) ?", "opts": ["1s² 2s² 2p²", "1s² 2s² 2p⁶", "1s² 2s²", "1s² 2p⁴"], "ans": "1s² 2s² 2p²"},
            {"q": "Dans une réaction d'oxydoréduction, l'oxydant est l'espèce qui :", "opts": ["Gagne des électrons", "Perd des électrons", "Gagne dei protoni", "Libera ossigeno"], "ans": "Gagne des électrons"},
            {"q": "Quel est le pH d'une solution neutre à 25°C ?", "opts": ["7", "0", "14", "1"], "ans": "7"}
        ]
    },
    "Physique": {
        "Mécanique & Électricité": [
            {"q": "Un corps de 5 kg est soumis à une force de 20 N. Quelle est son accélération ?", "opts": ["4 m/s²", "100 m/s²", "0.25 m/s²", "15 m/s²"], "ans": "4 m/s²"},
            {"q": "La loi d'Ohm s'écrit :", "opts": ["U = R * I", "P = U * I", "V = d / t", "E = mc²"], "ans": "U = R * I"}
        ]
    },
    "Mathématiques": {
        "Analyse & Algèbre": [
            {"q": "Quelle est la dérivée de f(x) = x² ?", "opts": ["2x", "x", "2", "x³/3"], "ans": "2x"},
            {"q": "Quelle est la solution de ln(x) = 0 ?", "opts": ["1", "e", "0", "10"], "ans": "1"}
        ]
    }
}

# --- LOGICA DI SESSIONE ---
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

# --- INTERFACCIA ---
st.title("🎓 ARES Simulator 2018-2025")

if not st.session_state.quiz_data or st.session_state.finished:
    materia_scelta = st.selectbox("Seleziona materia:", list(DB_ARES.keys()))
    if st.button("Inizia Simulazione"):
        start_quiz(materia_scelta)
        st.rerun()

else:
    idx = st.session_state.current_idx
    q = st.session_state.quiz_data[idx]
    
    st.write(f"**Domanda {idx + 1} di 10**")
    st.progress((idx) / 10)
    st.subheader(q['q'])

    # Il Form gestisce SOLO la selezione e la conferma della risposta
    with st.form(key=f"form_{idx}"):
        user_choice = st.radio("Scegli la risposta:", q['opts'])
        submit_button = st.form_submit_button("Conferma Risposta")

    # Logica di controllo fuori dal form per evitare l'errore StreamlitAPIException
    if submit_button and not st.session_state.submitted:
        st.session_state.submitted = True
        if user_choice == q['ans']:
            st.session_state.score += 1
            st.success("Corretto! ✅")
        else:
            st.error(f"Sbagliato! La risposta corretta era: {q['ans']} ❌")

    # Pulsante per andare avanti (appare solo dopo aver risposto)
    if st.session_state.submitted:
        if st.button("Prossima Domanda ➡️"):
            if idx + 1 < len(st.session_state.quiz_data):
                st.session_state.current_idx += 1
                st.session_state.submitted = False
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

if st.session_state.finished:
    st.balloons()
    st.header("🏁 Fine Test")
    st.metric("Punteggio Finale", f"{st.session_state.score} / 10")
    if st.button("Ricomincia"):
        st.session_state.quiz_data = []
        st.rerun()
