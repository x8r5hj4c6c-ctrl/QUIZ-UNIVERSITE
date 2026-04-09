import streamlit as st
import random
import math
import uuid

st.set_page_config(page_title="Quiz Universitaire - Matteo S.", page_icon="🎓")

# --- DATABASE E GENERATORI ---

def get_math():
    sub = random.choice(["Vecteurs", "Trigo", "Analyse"])
    if sub == "Vecteurs":
        L = random.randint(2, 10)
        q, corr = f"Dans un carré ABCD de côté {L}, que vaut le produit scalaire AB · CA ?", str(-(L**2))
        opts = [corr, "0", str(L**2), str(L)]
    elif sub == "Trigo":
        q, corr = "Quelle est la valeur de sin(π/6) + cos(π/3) ?", "1.0"
        opts = ["1.0", "0.5", "1.5", "0"]
    else:
        a = random.randint(2, 6)
        q, corr = f"Quelle est la limite de ({a}x² + 1) / (x² - 3) quand x tend vers l'infini ?", str(a)
        opts = [corr, "0", "1", "∞"]
    return "Mathématiques", q, corr, opts

def get_physique():
    sub = random.choice(["Cinématique", "Optique", "Électricité"])
    if sub == "Cinématique":
        v = random.randint(5, 15)
        q, corr = f"Vitesse finale après 2s de chute libre (v0={v} m/s, g=10) ?", f"{v+20} m/s"
        opts = [corr, f"{v} m/s", "20 m/s", "40 m/s"]
    elif sub == "Optique":
        q, corr = "Si la surface dell'eau est concave vers le BAS, l'ombre au fond est...", "Plus grande"
        opts = ["Plus grande", "Plus petite", "Identique", "Nulle"]
    else:
        q, corr = "Quelle est l'unité de la résistance électrique ?", "Ohm"
        opts = ["Ohm", "Volt", "Ampère", "Watt"]
    return "Physique", q, corr, opts

def get_chimie():
    q, corr = "Quel est le pH d'une solution d'HCl à 0,001 mol/L ?", "3"
    opts = ["3", "1", "7", "11"]
    return "Chimie", q, corr, opts

def get_bio():
    q, corr = "Où se déroule spécifiquement le cycle de Krebs ?", "Mitochondrie"
    opts = ["Mitochondrie", "Noyau", "Ribosome", "Cytoplasme"]
    return "Biologie", q, corr, opts

# --- LOGICA DI SESSIONE ---

if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'answered' not in st.session_state: st.session_state.answered = False
if 'current_q' not in st.session_state: st.session_state.current_q = None

def load_new_question():
    f = random.choice([get_math, get_physique, get_chimie, get_bio])
    cat, q, corr, opts = f()
    unique_opts = list(dict.fromkeys(opts))
    random.shuffle(unique_opts)
    st.session_state.current_q = {
        "cat": cat, "q": q, "corr": corr, "opts": unique_opts, 
        "id": str(uuid.uuid4())[:8]
    }
    st.session_state.answered = False

if st.session_state.current_q is None:
    load_new_question()

# --- INTERFACCIA ---

st.title("Prodotto da Matteo S.")
st.sidebar.metric("Score", f"{st.session_state.score} / {st.session_state.total}")

curr = st.session_state.current_q
st.subheader(f"Matière : {curr['cat']}")
st.info(curr['q'])

# --- BLOCCO CORRETTO DEI BOTTONI ---
for idx, o in enumerate(curr['opts']):
    if st.button(o, key=f"{curr['id']}_{idx}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if o == curr['corr']:
            st.session_state.score += 1
            st.success("Correct ! ✨")
        else:
            st.error(f"Faux. La réponse était : {curr['corr']}")

if st.session_state.answered:
    if st.button("Question Suivante ➡️", key="next_btn"):
        load_new_question()
        st.rerun()

if st.sidebar.button("Réinitialiser le score", key="reset"):
    st.session_state.score = 0
    st.session_state.total = 0
    load_new_question()
    st.rerun()
