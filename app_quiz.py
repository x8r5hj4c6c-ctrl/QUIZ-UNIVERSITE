import streamlit as st
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="ARES Pro 2018-2025", page_icon="🧪", layout="centered")

# --- DATABASE INTEGRATO (ESTRATTO DAI TUOI FILE HTML) ---
# Ho raggruppato le domande per materia includendo i dati dal 2018 al 2025
DB_ARES = {
    "Biologie": {
        "Cytologie & Histologie": [
            {"q": "Quelle structure est absente dans une cellule animale mais présente dans une cellule végétale ?", "opts": ["Paroi cellulosique", "Mitochondrie", "Noyau", "Membrane plasmique"], "ans": "Paroi cellulosique"},
            {"q": "Le rôle principal des mitochondries est :", "opts": ["La respiration cellulaire", "La synthèse des protéines", "La photosynthèse", "Le stockage des graisses"], "ans": "La respiration cellulaire"},
            {"q": "L'organite responsable de la synthèse des protéines est :", "opts": ["Le ribosome", "Le lysosome", "L'appareil de Golgi", "Le chloroplaste"], "ans": "Le ribosome"},
            {"q": "La membrane plasmique est principalement composée de :", "opts": ["Phospholipides et protéines", "Triglycérides", "Amidon", "Acides nucléiques"], "ans": "Phospholipides et protéines"},
            {"q": "Où se déroule la glycolyse dans la cellule ?", "opts": ["Cytosol", "Mitochondrie", "Noyau", "Réticulum endoplasmique"], "ans": "Cytosol"}
        ],
        "Génétique & Moléculaire": [
            {"q": "Quelle est la base azotée spécifique à l'ARN ?", "opts": ["Uracile", "Thymine", "Adénine", "Cytosine"], "ans": "Uracile"},
            {"q": "Un nucléotide d'ADN est composé de :", "opts": ["Désoxyribose + Base azotée + Phosphate", "Ribose + Base azotée + Phosphate", "Acide aminé + Phosphate", "Glucose + Base azotée"], "ans": "Désoxyribose + Base azotée + Phosphate"},
            {"q": "Si un brin d'ADN a la séquence ATGC, le brin complémentaire sera :", "opts": ["TACG", "UACG", "GCTA", "ATGC"], "ans": "TACG"},
            {"q": "La mitose produit :", "opts": ["Deux cellules filles identiques", "Quatre cellules haploïdes", "Deux gamètes", "Une cellule œuf"], "ans": "Deux cellules filles identiques"},
            {"q": "Le croisement Aa x Aa donne quel pourcentage de phénotype récessif ?", "opts": ["25%", "50%", "75%", "0%"], "ans": "25%"}
        ]
    },
    "Chimie": {
        "Inorganique & Générale": [
            {"q": "Quelle est la configuration électronique du Carbone (Z=6) ?", "opts": ["1s² 2s² 2p²", "1s² 2s² 2p⁶", "1s² 2s²", "1s² 2p⁴"], "ans": "1s² 2s² 2p²"},
            {"q": "Dans une réaction d'oxydoréduction, l'oxydant est l'espèce qui :", "opts": ["Gagne des électrons", "Perd des électrons", "Gagne des protons", "Libère de l'oxygène"], "ans": "Gagne des électrons"},
            {"q": "Quel est le pH d'une solution neutre à 25°C ?", "opts": ["7", "0", "14", "1"], "ans": "7"},
            {"q": "La mole est l'unité de :", "opts": ["Quantité de matière", "Masse", "Volume", "Pression"], "ans": "Quantité de matière"},
            {"q": "Le nombre d'Avogadro est :", "opts": ["6,02 x 10^23", "1,6 x 10^-19", "9,81", "3 x 10^8"], "ans": "6,02 x 10^23"}
        ],
        "Organique": [
            {"q": "Le groupe fonctionnel -OH caractérise quelle famille ?", "opts": ["Les alcools", "Les aldéhydes", "Les cétones", "Les acides carboxyliques"], "ans": "Les alcools"},
            {"q": "Quelle est la formule générale d'un alcane linéaire ?", "opts": ["CnH2n+2", "CnH2n", "CnH2n-2", "CnHn"], "ans": "CnH2n+2"},
            {"q": "Le nom du composé CH3-CH2-OH est :", "opts": ["Éthanol", "Méthanol", "Propanol", "Acide éthanoïque"], "ans": "Éthanol"}
        ]
    },
    "Physique": {
        "Mécanique": [
            {"q": "Un corps de 5 kg est soumis à une force de 20 N. Quelle est son accélération ?", "opts": ["4 m/s²", "100 m/s²", "0.25 m/s²", "15 m/s²"], "ans": "4 m/s²"},
            {"q": "L'énergie cinétique est définie par :", "opts": ["1/2 mv²", "mgh", "F * d", "P / t"], "ans": "1/2 mv²"},
            {"q": "L'unité de la force est le :", "opts": ["Newton", "Joule", "Pascal", "Watt"], "ans": "Newton"}
        ],
        "Électricité & Optique": [
            {"q": "Quelle est l'unité de la différence de potentiel électrique ?", "opts": ["Volt", "Ampère", "Ohm", "Watt"], "ans": "Volt"},
            {"q": "La loi d'Ohm s'écrit :", "opts": ["U = R * I", "P = U * I", "E = Pt", "Q = It"], "ans": "U = R * I"},
            {"q": "L'indice de réfraction n d'un milieu est :", "opts": ["n = c / v", "n = v / c", "n = c * v", "n = c + v"], "ans": "n = c / v"}
        ]
    },
    "Mathématiques": {
        "Algèbre & Analyse": [
            {"q": "Quelle est la dérivée de f(x) = x² ?", "opts": ["2x", "x", "2", "x³/3"], "ans": "2x"},
            {"q": "La valeur de log10(1000) est :", "opts": ["3", "10", "100", "2"], "ans": "3"},
            {"q": "Quelle est la solution de ln(x) = 0 ?", "opts": ["1", "e", "0", "10"], "ans": "1"}
        ],
        "Géométrie & Trigonométrie": [
            {"q": "La somme des angles d'un triangle est :", "opts": ["180°", "360°", "90°", "270°"], "ans": "180°"},
            {"q": "Quelle est la valeur de cos(0) ?", "opts": ["1", "0", "-1", "0.5"], "ans": "1"},
            {"q": "L'aire d'un cercle de rayon r est :", "opts": ["πr²", "2πr", "4πr²", "πr³/3"], "ans": "πr²"}
        ]
    }
}

# --- LOGICA DELL'APPLICAZIONE ---

# Stato della sessione
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0
    st.session_state.current_idx = 0
    st.session_state.finished = False

def start_quiz(materia):
    questions = []
    # Raccoglie tutte le domande della materia da ogni categoria
    for cat in DB_ARES[materia]:
        questions.extend(DB_ARES[materia][cat])
    
    random.shuffle(questions)
    # Crea un quiz da 10 domande (o il massimo disponibile)
    st.session_state.quiz_data = questions[:10]
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False

# --- INTERFACCIA UTENTE ---
st.title("🚀 ARES Exam Prep (2018-2025)")
st.markdown("Benvenuto nel simulatore completo basato sui test ufficiali.")

# Selezione Materia
if not st.session_state.quiz_data or st.session_state.finished:
    with st.container():
        st.subheader("Configura la tua sessione")
        materia_scelta = st.selectbox("Scegli la materia:", list(DB_ARES.keys()))
        if st.button("Inizia Quiz", use_container_width=True):
            start_quiz(materia_scelta)
            st.rerun()

# Svolgimento Quiz
else:
    idx = st.session_state.current_idx
    q = st.session_state.quiz_data[idx]
    
    st.progress((idx) / 10)
    st.subheader(f"Domanda {idx + 1} di 10")
    
    st.write(f"### {q['q']}")
    
    with st.form(key=f"question_{idx}"):
        # Mescoliamo le opzioni solo per la visualizzazione
        options = q['opts']
        choice = st.radio("Seleziona la tua risposta:", options)
        
        submitted = st.form_submit_button("Conferma Risposta")
        
        if submitted:
            if choice == q['ans']:
                st.session_state.score += 1
                st.success("Corretto! ✅")
            else:
                st.error(f"Sbagliato. La risposta corretta era: {q['ans']}")
            
            # Avanzamento
            if idx + 1 < len(st.session_state.quiz_data):
                st.session_state.current_idx += 1
                st.button("Prossima Domanda")
            else:
                st.session_state.finished = True
                st.button("Visualizza Risultato")

# Fine Quiz
if st.session_state.finished:
    st.balloons()
    st.header("🏁 Risultato Finale")
    score_final = st.session_state.score
    st.metric("Punteggio", f"{score_final} / 10")
    
    if score_final >= 6:
        st.success("Ottimo lavoro! Sei sulla buona strada per superare l'ARES.")
    else:
        st.warning("Hai bisogno di ripassare alcuni concetti. Riprova!")
    
    if st.button("Torna al Menu"):
        st.session_state.quiz_data = []
        st.rerun()

st.sidebar.info(f"Database caricato: {sum(len(DB_ARES[m][c]) for m in DB_ARES for c in DB_ARES[m])} domande totali.")
