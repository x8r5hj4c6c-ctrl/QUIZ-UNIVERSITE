import streamlit as st
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Matteo x M3.0", page_icon="🎓", layout="centered")

# --- DATABASE INTEGRATO (ESTRATTO DAI TUOI FILE 2018-2025) ---
DB_ARES = {
    "Biologie": {
        "Cytologie & Génétique": [
            {"q": "Quelle structure est absente dans une cellule animale mais présente dans une cellule végétale ?", "opts": ["Paroi cellulosique", "Mitochondrie", "Noyau", "Membrane plasmique"], "ans": "Paroi cellulosique"},
            {"q": "Le rôle principal des mitochondries est :", "opts": ["La respiration cellulaire", "La synthèse des protéines", "La photosynthèse", "Le stockage des graisses"], "ans": "La respiration cellulaire"},
            {"q": "Quelle est la base azotée spécifique à l'ARN ?", "opts": ["Uracile", "Thymine", "Adénine", "Cytosine"], "ans": "Uracile"},
            {"q": "Un nucléotide d'ADN est composé de :", "opts": ["Désoxyribose + Base azotée + Phosphate", "Ribose + Base azotée + Phosphate", "Acide aminé + Phosphate", "Glucose + Base azotée"], "ans": "Désoxyribose + Base azotée + Phosphate"},
            {"q": "La mitose produit :", "opts": ["Deux cellules filles identiques", "Quatre cellules haploïdes", "Deux gamètes", "Une cellule œuf"], "ans": "Deux cellules filles identiques"}
        ]
    },
    "Chimie": {
        "Générale & Organique": [
            {"q": "Quelle est la configuration électronique du Carbone (Z=6) ?", "opts": ["1s² 2s² 2p²", "1s² 2s² 2p⁶", "1s² 2s²", "1s² 2p⁴"], "ans": "1s² 2s² 2p²"},
            {"q": "Quel est le pH d'une solution neutre à 25°C ?", "opts": ["7", "0", "14", "1"], "ans": "7"},
            {"q": "Le groupe fonctionnel -OH caractérise quelle famille ?", "opts": ["Les alcools", "Les aldéhydes", "Les cétones", "Les acides carboxyliques"], "ans": "Les alcools"},
            {"q": "La mole est l'unité de :", "opts": ["Quantité de matière", "Masse", "Volume", "Pression"], "ans": "Quantité de matière"}
        ]
    },
    "Physique": {
        "Mécanique & Électricité": [
            {"q": "Un corpo di 5 kg è sottoposto a una forza di 20 N. Qual è la sua accelerazione?", "opts": ["4 m/s²", "100 m/s²", "0.25 m/s²", "15 m/s²"], "ans": "4 m/s²"},
            {"q": "La legge di Ohm si scrive:", "opts": ["U = R * I", "P = U * I", "V = d / t", "E = mc²"], "ans": "U = R * I"},
            {"q": "L'unità della forza nel Sistema Internazionale è il:", "opts": ["Newton", "Joule", "Watt", "Pascal"], "ans": "Newton"}
        ]
    },
    "Mathématiques": {
        "Algèbre & Géométrie": [
            {"q": "Qual è la derivata di f(x) = x²?", "opts": ["2x", "x", "2", "x³/3"], "ans": "2x"},
            {"q": "La somma degli angoli interni di un triangolo è:", "opts": ["180°", "360°", "90°", "270°"], "ans": "180°"},
            {"q": "Qual è il valore di log10(100)?", "opts": ["2", "10", "1", "0"], "ans": "2"}
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
st.title("🚀 Matteo x M3.0")
st.subheader("Simulatore ARES Integrato")

if not st.session_state.quiz_data or st.session_state.finished:
    with st.expander("Configurazione Quiz", expanded=True):
        materia_scelta = st.selectbox("Scegli la materia da studiare:", list(DB_ARES.keys()))
        if st.button("Inizia Simulazione", use_container_width=True):
            start_quiz(materia_scelta)
            st.rerun()

else:
    idx = st.session_state.current_idx
    q = st.session_state.quiz_data[idx]
    
    st.write(f"**Domanda {idx + 1} di {len(st.session_state.quiz_data)}**")
    st.progress((idx) / len(st.session_state.quiz_data))
    
    # Visualizzazione Domanda
    st.markdown(f"### {q['q']}")

    # Form per la risposta
    with st.form(key=f"ares_form_{idx}"):
        user_choice = st.radio("Seleziona l'opzione corretta:", q['opts'], key=f"radio_{idx}")
        submit_button = st.form_submit_button("Conferma Risposta")

    # Gestione Risposta (FUORI DAL FORM)
    if submit_button:
        st.session_state.submitted = True
        if user_choice == q['ans']:
            st.session_state.score += 1
            st.toast("Corretto!", icon="✅")
        else:
            st.toast("Sbagliato!", icon="❌")

    # Feedback e Navigazione
    if st.session_state.submitted:
        if user_choice == q['ans']:
            st.success(f"Ottimo! La risposta è corretta.")
        else:
            st.error(f"Sbagliato. La risposta corretta era: **{q['ans']}**")
        
        if st.button("Prossima Domanda ➡️", use_container_width=True):
            if idx + 1 < len(st.session_state.quiz_data):
                st.session_state.current_idx += 1
                st.session_state.submitted = False
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

# Fine Quiz
if st.session_state.finished:
    st.balloons()
    st.header("🏁 Simulazione Conclusa")
    st.metric("Punteggio Finale", f"{st.session_state.score} / {len(st.session_state.quiz_data)}")
    
    if st.button("Riprova un altro Quiz", use_container_width=True):
        st.session_state.quiz_data = []
        st.rerun()
