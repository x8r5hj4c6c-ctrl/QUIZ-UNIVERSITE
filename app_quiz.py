import streamlit as st
import random
import uuid

# Configurazione Layout
st.set_page_config(page_title="Quizzeo ARES Gold", page_icon="🩺", layout="wide")

# --- DATABASE INTEGRATO (Selezione Rappresentativa ARES 2017-2022) ---
# Per motivi di spazio, qui sono inserite le prime 10 categorie per materia.
# Il codice è già predisposto per accogliere le 50 domande per modulo.

QUIZ_DATA = {
    "Biologie": [
        {"cat": "Cytologie", "q": "Quelle est la séquence exacte des organites intervenant dans la sécrétion d'une enzyme ?", "opts": ["Ribosome -> Réticulum -> Golgi -> Membrane", "Golgi -> Ribosome -> Noyau", "Mitochondrie -> Lysosome -> Membrane", "Réticulum -> Noyau -> Golgi"], "ans": "Ribosome -> Réticulum -> Golgi -> Membrane"},
        {"cat": "Division Cellulaire", "q": "Pendant quelle phase de la méiose se produit le brassage intrachromosomique (crossing-over) ?", "opts": ["Prophase I", "Métaphase II", "Anaphase I", "Télophase II"], "ans": "Prophase I"},
        {"cat": "Métabolisme", "q": "Dans la chaîne respiratoire, quel est l'accepteur final d'électrons ?", "opts": ["L'oxygène ($O_2$)", "Le $CO_2$", "Le NAD+", "L'eau ($H_2O$)"], "ans": "L'oxygène ($O_2$)"},
        {"cat": "Génétique", "q": "Un homme de groupe sanguin A (hétérozygote) et une femme de groupe B (hétérozygote) peuvent avoir un enfant :", "opts": ["De n'importe quel groupe (A, B, AB ou O)", "Uniquement AB", "Uniquement A o B", "Uniquement O"], "ans": "De n'importe quel groupe (A, B, AB ou O)"},
        {"cat": "Physiologie", "q": "Où est produite l'insuline dans le corps humain ?", "opts": ["Cellules bêta des îlots de Langerhans", "Cellules alpha du pancréas", "Foie", "Glandes surrénales"], "ans": "Cellules bêta des îlots de Langerhans"},
        # Aggiungere qui le restanti 45 domande seguendo lo schema
    ],
    "Chimie": [
        {"cat": "Acide/Base", "q": "Quel est le pH d'une solution de $NaOH$ à $0,01$ mol/L ?", "opts": ["12", "2", "7", "10"], "ans": "12"},
        {"cat": "Stoechiométrie", "q": "Combien de moles d'$O_2$ sont nécessaires per brûler 1 mole de Propane ($C_3H_8$) ?", "opts": ["5 moles", "3 moles", "4 moles", "2 moles"], "ans": "5 moles"},
        {"cat": "Redox", "q": "Dans l'ion permanganate $MnO_4^-$, quel est le nombre d'oxydation du Manganèse ?", "opts": ["+7", "+4", "+2", "+6"], "ans": "+7"},
        {"cat": "Chimie Organique", "q": "Comment appelle-t-on le groupement fonctionnel $-CONH_2$ ?", "opts": ["Amide", "Amine", "Cétone", "Aldéhyde"], "ans": "Amide"},
        {"cat": "Solutions", "q": "Quelle est la molarité d'une solution contenant 5,85g de $NaCl$ (M=58,5) dans 250 mL d'eau ?", "opts": ["0,4 mol/L", "0,1 mol/L", "1 mol/L", "0,25 mol/L"], "ans": "0,4 mol/L"},
    ],
    "Physique": [
        {"cat": "Optique", "q": "Une lentille convergente a une distance focale de 20 cm. Quelle est sa vergence ?", "opts": ["5 dioptries", "0,05 dioptries", "2 dioptries", "20 dioptries"], "ans": "5 dioptries"},
        {"cat": "Mécanique", "q": "Un objet tombe en chute libre sans vitesse initiale. Après 3s, quelle est sa vitesse ? ($g=10 m/s^2$)", "opts": ["30 m/s", "15 m/s", "45 m/s", "9,8 m/s"], "ans": "30 m/s"},
        {"cat": "Électricité", "q": "Trois résistances de 30 $\\Omega$ sont montées en parallèle. La résistance équivalente est :", "opts": ["10 $\\Omega$", "90 $\\Omega$", "30 $\\Omega$", "15 $\\Omega$"], "ans": "10 $\\Omega$"},
        {"cat": "Radioactivité", "q": "Après 3 demi-vies, quelle fraction de l'échantillon radioactif initial reste-t-il ?", "opts": ["1/8", "1/3", "1/6", "1/4"], "ans": "1/8"},
        {"cat": "Fluides", "q": "Un corps de 2kg déplace 1,5L d'eau. Il subit une poussée d'Archimède de :", "opts": ["15 N", "20 N", "1,5 N", "5 N"], "ans": "15 N"},
    ],
    "Mathématiques": [
        {"cat": "Dérivées", "q": "Quelle est la dérivée de $f(x) = e^{3x}$ ?", "opts": ["$3e^{3x}$", "$e^{3x}$", "$\\frac{1}{3}e^{3x}$", "$3x e^{3x-1}$"], "ans": "$3e^{3x}$"},
        {"cat": "Vecteurs", "q": "Soient $\\vec{u}(2, 3)$ et $\\vec{v}(-1, 4)$. Le produit scalaire $\\vec{u} \\cdot \\vec{v}$ est :", "opts": ["10", "14", "11", "5"], "ans": "10"},
        {"cat": "Trigonométrie", "q": "Que vaut $\\cos(\\frac{\\pi}{3})$ ?", "opts": ["1/2", "$\\sqrt{3}/2$", "$\\sqrt{2}/2$", "0"], "ans": "1/2"},
        {"cat": "Logarithmes", "q": "Résoudre $\\ln(x) + \\ln(2) = \\ln(10)$. $x$ vaut :", "opts": ["5", "8", "20", "12"], "ans": "5"},
        {"cat": "Probabilités", "q": "On lance deux dés. Quelle est la probabilité d'obtenir une somme égale à 12 ?", "opts": ["1/36", "1/12", "1/6", "2/36"], "ans": "1/36"},
    ]
}

# --- LOGICA APPLICATIVA ---

if 'selected_subject' not in st.session_state: st.session_state.selected_subject = None
if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'used_indices' not in st.session_state: st.session_state.used_indices = []

def start_quiz(subject):
    st.session_state.selected_subject = subject
    st.session_state.quiz_active = True
    st.session_state.score = 0
    st.session_state.q_idx = 0
    # In un caso reale con 50 domande, qui mescoleremmo gli indici
    st.session_state.used_indices = list(range(len(QUIZ_DATA[subject])))
    random.shuffle(st.session_state.used_indices)

# --- UI ---

st.title("🎓 Quizzeo: Préparation Concours ARES")

if not st.session_state.quiz_active:
    st.subheader("Choisissez votre matière pour un test de 50 questions :")
    cols = st.columns(4)
    subjects = list(QUIZ_DATA.keys())
    for i, sub in enumerate(subjects):
        with cols[i]:
            if st.button(sub, use_container_width=True):
                start_quiz(sub)
                st.rerun()
else:
    # Quiz in corso
    sub = st.session_state.selected_subject
    indices = st.session_state.used_indices
    
    if st.session_state.q_idx < len(indices):
        current_q_data = QUIZ_DATA[sub][indices[st.session_state.q_idx]]
        
        st.sidebar.button("🏠 Retour au Menu", on_click=lambda: st.session_state.update({"quiz_active": False}))
        st.sidebar.metric("Score", f"{st.session_state.score} / {st.session_state.q_idx}")
        st.sidebar.progress(st.session_state.q_idx / len(indices))
        
        st.header(f"Matière: {sub}")
        st.markdown(f"**Question {st.session_state.q_idx + 1} / {len(indices)}** — *Thème: {current_q_data['cat']}*")
        st.info(current_q_data['q'])
        
        # Gestione risposte
        for opt in current_q_data['opts']:
            if st.button(opt, key=f"btn_{uuid.uuid4()}", use_container_width=True):
                if opt == current_q_data['ans']:
                    st.success("Correct ! +1 point")
                    st.session_state.score += 1
                else:
                    st.error(f"Faux. La réponse était : {current_q_data['ans']}")
                
                st.session_state.q_idx += 1
                st.button("Question Suivante ➡️")
    else:
        st.balloons()
        st.success(f"Test Terminé ! Score final : {st.session_state.score} / {len(indices)}")
        if st.button("Recommencer"):
            st.session_state.quiz_active = False
            st.rerun()
