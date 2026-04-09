import streamlit as st
import random

# Configurazione Pagina
st.set_page_config(page_title="Quizzeo - Matteo S.", page_icon="🎓", layout="centered")

# --- DATABASE DOMANDE ORIGINALI ARES (2017-2022) ---
# Ho inserito una selezione rappresentativa. Puoi aggiungere altre righe seguendo lo schema.
ARES_DATABASE = [
    # BIOLOGIA
    {"id": "BIO_01", "cat": "Biologia", "q": "Lequel des organites suivants est délimité par une double membrane et contient son propre ADN ?", "opts": ["La mitochondrie", "Le ribosome", "L'appareil de Golgi", "Le lysosome"], "ans": "La mitochondrie"},
    {"id": "BIO_02", "cat": "Biologia", "q": "Au cours de quelle phase de la mitose les chromatides sœurs se séparent-elles ?", "opts": ["L'anaphase", "La prophase", "La métaphase", "La télophase"], "ans": "L'anaphase"},
    {"id": "BIO_03", "cat": "Biologia", "q": "Quelle molécule est le produit final de la glycolyse en conditions aérobies ?", "opts": ["Le pyruvate", "Le lactate", "L'éthanol", "L'acétyl-CoA"], "ans": "Le pyruvate"},
    {"id": "BIO_04", "cat": "Biologia", "q": "Où se déroule la transcription de l'ADN en ARN messager chez les eucaryotes ?", "opts": ["Le noyau", "Le cytoplasme", "Le ribosome", "Le réticulum endoplasmique"], "ans": "Le noyau"},
    {"id": "BIO_05", "cat": "Biologia", "q": "Quelle est la fonction principale des lysosomes ?", "opts": ["La digestion intracellulaire", "La synthèse des protéines", "La respiration cellulaire", "Le stockage du calcium"], "ans": "La digestion intracellulaire"},

    # CHIMICA
    {"id": "CHM_01", "cat": "Chimica", "q": "Quel est le pH d'une solution d'HCl à $10^{-3}$ mol/L ?", "opts": ["3", "1", "7", "11"], "ans": "3"},
    {"id": "CHM_02", "cat": "Chimica", "q": "Une masse volumique de 1 g/cm³ correspond à :", "opts": ["1000 kg/m³", "1 kg/m³", "10 kg/m³", "100 kg/m³"], "ans": "1000 kg/m³"},
    {"id": "CHM_03", "cat": "Chimica", "q": "Dans la réaction d'oxydoréduction, l'oxydant est une espèce qui :", "opts": ["Capte des électrons", "Cède des électrons", "Capte des protons", "Cède des protons"], "ans": "Capte des électrons"},
    {"id": "CHM_04", "cat": "Chimica", "q": "Quelle est la molarité d'une solution contenant 40g de NaOH (M=40 g/mol) dans 500 mL d'eau ?", "opts": ["2 mol/L", "1 mol/L", "0.5 mol/L", "4 mol/L"], "ans": "2 mol/L"},
    {"id": "CHM_05", "cat": "Chimica", "q": "Quel volume occupe une mole de gaz parfait à 0°C et 1 atm ?", "opts": ["22,4 L", "24,0 L", "11,2 L", "1,0 L"], "ans": "22,4 L"},

    # FISICA
    {"id": "PHY_01", "cat": "Fisica", "q": "Un insecte est posé sur l'eau. La surface forme une dépression concave. L'ombre projetée au fond est :", "opts": ["Plus grande que l'insecte", "Plus petite que l'insecte", "De même taille", "Inexistante"], "ans": "Plus grande que l'insecte"},
    {"id": "PHY_02", "cat": "Fisica", "q": "La loi de Snell-Descartes pour la réfraction s'énonce :", "opts": ["$n_1 \\sin(i_1) = n_2 \\sin(i_2)$", "$n_1 \\cos(i_1) = n_2 \\cos(i_2)$", "$i_1 = i_2$", "$v_1 n_1 = v_2 n_2$"], "ans": "$n_1 \\sin(i_1) = n_2 \\sin(i_2)$"},
    {"id": "PHY_03", "cat": "Fisica", "q": "Quelle est l'unité de la puissance électrique dans le SI ?", "opts": ["Watt", "Joule", "Volt", "Ampère"], "ans": "Watt"},
    {"id": "PHY_04", "cat": "Fisica", "q": "Un objet est placé au foyer objet d'une lentille convergente. L'image se forme :", "opts": ["À l'infini", "Au foyer image", "Au centre optique", "Sur l'objet"], "ans": "À l'infini"},
    {"id": "PHY_05", "cat": "Fisica", "q": "La pression hydrostatique à 10m de profondeur dans l'eau est d'environ :", "opts": ["2 atm", "1 atm", "10 atm", "0.1 atm"], "ans": "2 atm"},

    # MATEMATICA
    {"id": "MAT_01", "cat": "Matematica", "q": "Dans un carré PQRS de côté $L=2$, que vaut le produit scalaire $\\vec{PQ} \\cdot \\vec{RP}$ ?", "opts": ["-4", "-2", "2", "4"], "ans": "-4"},
    {"id": "MAT_02", "cat": "Matematica", "q": "Quelle est la dérivée de la fonction $f(x) = \\ln(x^2 + 1)$ ?", "opts": ["$2x / (x^2 + 1)$", "$1 / (x^2 + 1)$", "$2x (x^2 + 1)$", "$x / (x^2 + 1)$"], "ans": "$2x / (x^2 + 1)$"},
    {"id": "MAT_03", "cat": "Matematica", "q": "Dans un triangle rectangle, si $\\sin(\\theta) = 0,6$, que vaut $\\cos(\\theta)$ ?", "opts": ["0,8", "0,4", "0,36", "1"], "ans": "0,8"},
    {"id": "MAT_04", "cat": "Matematica", "q": "La limite de $(2x^2 + 3) / (x^2 - 1)$ quand $x \\to \\infty$ est :", "opts": ["2", "3", "0", "$\\infty$"], "ans": "2"},
    {"id": "MAT_05", "cat": "Matematica", "q": "Que vaut l'intégrale $\\int_0^1 3x^2 dx$ ?", "opts": ["1", "3", "0,5", "2"], "ans": "1"}
]

# --- LOGICA DI NAVIGAZIONE SENZA RIPETIZIONI ---

if 'used_questions' not in st.session_state:
    st.session_state.used_questions = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

def get_new_question():
    # Filtra le domande non ancora usate
    available = [q for q in ARES_DATABASE if q['id'] not in st.session_state.used_questions]
    
    if not available:
        return None # Tutte le domande sono state usate
    
    selected = random.choice(available)
    st.session_state.used_questions.append(selected['id'])
    return selected

# Caricamento prima domanda
if st.session_state.current_q is None:
    st.session_state.current_q = get_new_question()

# --- INTERFACCIA ---

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Quizzeo - Prodotto da Matteo S.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Simulatore Ufficiale MD/Dentisterie (ARES)</b></p>", unsafe_allow_html=True)
st.divider()

# Controllo fine domande
if st.session_state.current_q is None:
    st.balloons()
    st.success("🎉 Hai completato tutte le domande disponibili senza ripetizioni!")
    st.metric("Punteggio Finale", f"{st.session_state.score} / {len(st.session_state.used_questions)}")
    if st.button("Ricomincia da capo"):
        st.session_state.used_questions = []
        st.session_state.score = 0
        st.session_state.current_q = get_new_question()
        st.rerun()
    st.stop()

# Visualizzazione Domanda
q = st.session_state.current_q
st.sidebar.title("Statistiche")
st.sidebar.write(f"Domande risposte: {len(st.session_state.used_questions)} / {len(ARES_DATABASE)}")
st.sidebar.metric("Punteggio Corrente", f"{st.session_state.score}")

st.subheader(f"Materia: {q['cat']}")
st.info(q['q'])

# Gestione Opzioni (Mescolate una sola volta)
if 'current_opts' not in st.session_state or st.session_state.answered == False:
    opts = q['opts'].copy()
    random.shuffle(opts)
    st.session_state.current_opts = opts

# Bottoni
for opt in st.session_state.current_opts:
    if st.button(opt, key=f"{q['id']}_{opt}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        if opt == q['ans']:
            st.session_state.score += 1
            st.success("Risposta Corretta! ✨")
        else:
            st.error(f"Sbagliato. La risposta corretta era: {q['ans']}")

# Prossima Domanda
if st.session_state.answered:
    if st.button("Prossima Domanda ➡️", type="primary"):
        st.session_state.current_q = get_new_question()
        st.session_state.answered = False
        st.rerun()
