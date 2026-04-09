import streamlit as st
import random
import math

st.set_page_config(page_title="Quiz Universitaire - Matteo S.", page_icon="🎓")

# --- SISTEMA ANTI-RIPETIZIONE ---
if 'seen_questions' not in st.session_state:
    st.session_state.seen_questions = set()

# --- GENERATORI ---

def get_math_expert():
    sub = random.choice(["Trigo", "Analyse", "Vecteurs", "Probabilité"])
    if sub == "Trigo":
        val = random.choice([30, 45, 60])
        rad = {30: "π/6", 45: "π/4", 60: "π/3"}
        q = f"Valeur exacte de sin({rad[val]}) + cos({rad[val]})² ?"
        res = round(math.sin(math.radians(val)) + (math.cos(math.radians(val))**2), 3)
        corr = str(res)
        options = list(set([corr, "1", "1.5", "0.75", "0.5"]))[:4]
    elif sub == "Probabilité":
        n = random.randint(2, 4)
        q = f"On lance une pièce équilibrée {n} fois. Probabilité d'obtenir exactement {n} fois 'Pile' ?"
        corr = f"1/{2**n}"
        options = list(set([corr, f"1/{n*2}", f"1/{n**2}", "1/2", "1/4"]))[:4]
    elif sub == "Analyse":
        a = random.randint(2, 5)
        q = f"Limite de ( {a}x² - 5x ) / ( x² + 1 ) quand x tend vers +∞ ?"
        corr = str(a)
        options = list(set([corr, "0", "∞", "1", "-1"]))[:4]
    else:
        q = "Produit scalaire de u(1, 2, -1) et v(2, -1, 0) ?"
        corr = "0"
        options = ["0", "1", "-1", "2"]
    return "Mathématiques", q, corr, options

def get_physique_expert():
    sub = random.choice(["Cinématique", "Électricité", "Thermodynamique"])
    if sub == "Cinématique":
        v0 = random.randint(10, 20)
        vf = v0 + 30
        q = f"Vitesse finale après 3s de chute libre (v0 = {v0} m/s, g=10m/s²) ?"
        corr = f"{vf} m/s"
        options = list(set([corr, f"{v0} m/s", f"{vf-10} m/s", "30 m/s", "50 m/s"]))[:4]
    elif sub == "Électricité":
        r = random.choice([10, 20, 30])
        q = f"Résistance équivalente de deux résistances di {r}Ω en PARALLÈLE ?"
        corr = f"{r/2} Ω"
        options = [corr, f"{r*2} Ω", f"{r} Ω", "0 Ω"]
    else:
        q = "L'entropie d'un système isolé qui subit une transformation irréversible :"
        corr = "Augmente"
        options = ["Augmente", "Diminue", "Reste constante", "S'annule"]
    return "Physique", q, corr, options

def get_chimie_expert():
    sub = random.choice(["pH", "Organique", "Liaisons"])
    if sub == "pH":
        q = "Le pH d'une solution de NaOH (base forte) à 0,01 mol/L è :"
        corr = "12"
        options = ["12", "2", "10", "14"]
    elif sub == "Organique":
        q = "Quelle est la formule brute de l'éthane ?"
        corr = "C2H6"
        options = ["C2H6", "C2H4", "CH4", "C3H8"]
    else:
        q = "Quelle liaison est la plus forte ?"
        corr = "Liaison covalente"
        options = ["Liaison covalente", "Liaison hydrogène", "Liaison ionique", "Van der Waals"]
    return "Chimie", q, corr, options

def get_biologie_expert():
    sub = random.choice(["Moléculaire", "Génétique", "Cytologie"])
    if sub == "Moléculaire":
        q = "L'enzyme qui synthétise l'ARNm à partir de l'ADN est :"
        corr = "ARN Polymérase"
        options = ["ARN Polymérase", "ADN Polymérase", "Hélicase", "Ligase"]
    elif sub == "Génétique":
        q = "Ratio phénotypique d'un croisement Aa x Aa (dominant:récessif) ?"
        corr = "3:1"
        options = ["3:1", "1:1", "9:3:3:1", "1:2:1"]
    else:
        q = "Les anticorps sont produits par :"
        corr = "Les plasmocytes"
        options = ["Les plasmocytes", "Les lymphocytes T", "Les macrophages", "Les globules rouges"]
    return "Biologie", q, corr, options

# --- LOGICA CORE ---

if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'answered' not in st.session_state: st.session_state.answered = False
if 'current_q' not in st.session_state: st.session_state.current_q = None

def get_unique_question():
    f = random.choice([get_math_expert, get_physique_expert, get_chimie_expert, get_biologie_expert])
    cat, q, corr, opts = f()
    # Rimuove duplicati dalle opzioni
    opts = list(dict.fromkeys(opts)) 
    if len(opts) < 4: return get_unique_question() # Sicurezza
    q_id = f"{cat}-{q}"
    if q_id not in st.session_state.seen_questions:
        st.session_state.seen_questions.add(q_id)
        return cat, q, corr, opts
    return get_unique_question()

if st.session_state.current_q is None:
    cat, q, corr, opts = get_unique_question()
    random.shuffle(opts)
    st.session_state.current_q = {"cat": cat, "q": q, "corr": corr, "opts": opts}

# --- UI ---
st.title("Prodotto da Matteo S.")
st.sidebar.metric("Score", f"{st.session_state.score}/{st.session_state.total}")

curr = st.session_state.current_q
st.subheader(f"Matière : {curr['cat']}")
st.info(curr['q'])

# Risoluzione Errore DuplicateElementId: aggiungiamo una key unica tramite enumerate
for idx, o in enumerate(curr['opts']):
    if st.button(o, key=f"btn_{idx}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if o == curr['corr']:
            st.session_state.score += 1
            st.success("Correct ! ✨")
        else:
            st.error(f"Faux. La réponse était : {curr['corr']}")

if st.session_state.answered:
    if st.button("Question Suivante ➡️", key="next_btn"):
        st.session_state.current_q = None
        st.session_state.answered = False
        st.rerun()

if st.sidebar.button("Réinitialiser", key="reset_btn"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.seen_questions.clear()
    st.rerun()
