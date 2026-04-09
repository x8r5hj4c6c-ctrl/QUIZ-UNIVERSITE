import streamlit as st
import random
import math
import uuid

st.set_page_config(page_title="Master Prépa - Matteo S.", page_icon="🧪", layout="centered")

# --- LOGICA DI MEMORIA ---
if 'seen_questions' not in st.session_state:
    st.session_state.seen_questions = set()
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'answered' not in st.session_state: st.session_state.answered = False

# --- MOTORI DI GENERAZIONE AVANZATA ---

def gen_math():
    sub = random.choice(["Integrali", "Vettori 3D", "Probabilità Condizionata"])
    if sub == "Integrali":
        a = random.randint(2, 5)
        q = f"Calculez l'intégrale de f(x) = {a}x + 1 tra 0 et 2."
        # Integrale di ax + 1 è (a/2)x^2 + x. Valutato tra 0 e 2: (a/2)*4 + 2 = 2a + 2
        res = 2*a + 2
        corr = str(res)
        opts = [corr, str(res+2), str(a**2), str(2*a)]
    elif sub == "Vettori 3D":
        x = random.randint(1, 4)
        q = f"Soient u({x}, 2, -1) et v(2, -{x}, 4). Calculer le produit scalaire u · v."
        # x*2 + 2*(-x) + (-1)*4 = 2x - 2x - 4 = -4
        corr = "-4"
        opts = ["-4", "0", str(2*x), "4"]
    else:
        q = "Si P(A) = 0.4 et P(B|A) = 0.5, quelle est la probabilité de l'intersection P(A ∩ B) ?"
        corr = "0.2"
        opts = ["0.2", "0.9", "0.1", "0.5"]
    return "Mathématiques Supérieures", q, corr, opts

def gen_physique():
    sub = random.choice(["Cinématique", "Thermodynamique", "Optique Snell"])
    if sub == "Cinématique":
        v0 = random.randint(10, 30)
        q = f"Un projectile est lancé à {v0} m/s à 90°. Quelle est sa hauteur maximale ? (g=10 m/s²)"
        # h = v0^2 / 2g
        h = (v0**2) / 20
        corr = f"{h} m"
        opts = [corr, f"{v0} m", f"{v0*2} m", f"{h/2} m"]
    elif sub == "Thermodynamique":
        q = "Le rendement d'une machine de Carnot fonctionnant entre 300K et 600K est :"
        corr = "50%" # 1 - (300/600)
        opts = ["50%", "100%", "33%", "25%"]
    else:
        q = "Un rayon passe du verre (n=1.5) à l'air (n=1). L'angle critique de réfraction totale est :"
        corr = "arcsin(1/1.5) ≈ 42°"
        opts = ["arcsin(1/1.5) ≈ 42°", "arcsin(1.5) ≈ 56°", "30°", "90°"]
    return "Physique Théorique", q, corr, opts

def gen_chimie():
    sub = random.choice(["pH", "Thermochimie", "Organique"])
    if sub == "pH":
        c = random.choice([0.005, 0.01, 0.001])
        q = f"Calculer le pH d'une solution d'acide fort de concentration {c} mol/L."
        res = round(-math.log10(c), 2)
        corr = str(res)
        opts = [corr, str(round(res+1, 2)), "7.0", "1.0"]
    elif sub == "Organique":
        q = "Quel est le produit principal de l'hydratation de l'éthène (CH2=CH2) ?"
        corr = "Éthanol"
        opts = ["Éthanol", "Éthane", "Acide acétique", "Éthanal"]
    else:
        q = "L'enthalpie libre de Gibbs (ΔG) pour une réaction spontanée doit être :"
        corr = "Négative (ΔG < 0)"
        opts = ["Négative (ΔG < 0)", "Positive (ΔG > 0)", "Nulle", "Infinie"]
    return "Chimie Moléculaire", q, corr, opts

def gen_bio():
    sub = random.choice(["Génétique", "Cytologie", "Biochimie"])
    if sub == "Génétique":
        q = "Dans un croisement dihybride (AaBb x AaBb), quelle est la proportion de phénotypes récessifs pour les deux caractères ?"
        corr = "1/16"
        opts = ["1/16", "3/16", "9/16", "1/4"]
    elif sub == "Cytologie":
        q = "Quel organite est responsable de la modification post-traductionnelle des protéines ?"
        corr = "Appareil de Golgi"
        opts = ["Appareil de Golgi", "Réticulum endoplasmique lisse", "Lysosome", "Nucléole"]
    else:
        q = "Combien de molécules d'ATP sont produites nettes par la glycolyse d'une molécule de glucose ?"
        corr = "2 ATP"
        opts = ["2 ATP", "36 ATP", "4 ATP", "38 ATP"]
    return "Biologie Cellulaire", q, corr, opts

# --- LOGICA CORE ---

def load_q():
    f = random.choice([gen_math, gen_physique, gen_chimie, gen_bio])
    cat, quest, corr, opts = f()
    # Anti-duplicati nelle opzioni
    unique_opts = list(dict.fromkeys(opts))
    random.shuffle(unique_opts)
    st.session_state.current_q = {
        "cat": cat, "q": quest, "corr": corr, "opts": unique_opts, "id": str(uuid.uuid4())[:8]
    }
    st.session_state.answered = False

if st.session_state.current_q is None:
    load_q()

# --- INTERFACCIA ---

st.title("🚀 Master Prépa - Prodotto da Matteo S.")
st.write("Simulatore di concorso di alto livello con generazione procedurale.")
st.divider()

st.sidebar.title("Prestazioni")
st.sidebar.metric("Precisione", f"{st.session_state.score} / {st.session_state.total}")
if st.sidebar.button("Reset Totale"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.seen_questions.clear()
    load_q()
    st.rerun()

curr = st.session_state.current_q
st.subheader(f"Matière : {curr['cat']}")
st.info(curr['q'])

# Griglia bottoni
for idx, o in enumerate(curr['opts']):
    if st.button(o, key=f"{curr['id']}_{idx}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if o == curr['corr']:
            st.session_state.score += 1
            st.success("Excellent ! Réponse correcte. ✨")
        else:
            st.error(f"Faux. La réponse attendue était : {curr['corr']}")

if st.session_state.answered:
    if st.button("Question Suivante ➡️", type="primary"):
        load_q()
        st.rerun()
