import streamlit as st
import random
import math

st.set_page_config(page_title="Simulateur Concours Complet", page_icon="🎓")

# --- DATABASE DI LOGICA E ARGOMENTI ---

def get_math():
    sub = random.choice(["Vecteurs", "Algèbre", "Trigonométrie", "Analyse"])
    if sub == "Vecteurs":
        L = random.randint(2, 8)
        q = f"Dans un carré ABCD de côté {L}, que vaut le produit scalaire AB · CA ?"
        corr = -(L**2) # AB e CA hanno angolo 135° o proiezione opposta
        options = [str(corr), "0", str(L**2), str(round(L*math.sqrt(2), 2))]
    elif sub == "Algèbre":
        x = random.randint(1, 10)
        q = f"Si log2(x) + log2(4) = {2 + int(math.log2(x)) if x%2==0 else 5}, quelle est la valeur de x ?" # Esempio semplificato
        # Facciamo una equazione lineare più gestibile per il generatore
        a, b = random.randint(2, 5), random.randint(10, 30)
        res = a * x + b
        q = f"Résoudre l'équation pour x : {a}x + {b} = {res}"
        corr = str(x)
        options = [corr, str(x+2), str(x-1), "0"]
    else:
        q = "Quelle est la dérivée de f(x) = sin(x) + 3x² ?"
        corr = "cos(x) + 6x"
        options = [corr, "-cos(x) + 6x", "cos(x) + 3x", "sin(x) + 6x"]
    return "Mathématiques", q, corr, options

def get_physique():
    sub = random.choice(["Optique", "Mécanique", "Électricité", "Thermodynamique"])
    if sub == "Optique":
        q = "Un rayon lumineux passe dell'air à l'eau (n_eau > n_air). Le rayon réfracté :"
        corr = "Se rapproche de la normale"
        options = [corr, "S'éloigne de la normale", "Ne dévie pas", "Est totalement réfléchi"]
    elif sub == "Mécanique":
        m = random.randint(1, 10)
        v = random.randint(2, 6)
        ec = 0.5 * m * (v**2)
        q = f"Quelle est l'énergie cinétique d'un corps de {m}kg roulant à {v}m/s ?"
        corr = f"{ec} J"
        options = [corr, f"{m*v} J", f"{0.5*m*v} J", f"{m*(v**2)} J"]
    else:
        q = "Quelle est l'unité de mesure de la résistance électrique ?"
        corr = "Ohm (Ω)"
        options = [corr, "Volt (V)", "Ampère (A)", "Watt (W)"]
    return "Physique", q, corr, options

def get_chimie():
    sub = random.choice(["Stoechiométrie", "Organique", "Atomistique"])
    if sub == "Stoechiométrie":
        q = "Quelle est la masse molaire du glucose (C6H12O6) ? (C=12, H=1, O=16)"
        corr = "180 g/mol"
        options = [corr, "150 g/mol", "120 g/mol", "200 g/mol"]
    elif sub == "Organique":
        q = "Quel est le groupe fonctionnel caractéristique des alcools ?"
        corr = "-OH"
        options = [corr, "-CHO", "-COOH", "-NH2"]
    else:
        q = "Combien d'électrons peut contenir au maximum la sous-couche 'p' ?"
        corr = "6"
        options = ["6", "2", "10", "14"]
    return "Chimie", q, corr, options

def get_biologie():
    sub = random.choice(["Génétique", "Cytologie", "Physiologie"])
    if sub == "Génétique":
        q = "Si un individu est hétérozygote (Aa), quelle est la probabilité de transmettre l'allèle 'a' ?"
        corr = "50%"
        options = ["50%", "25%", "75%", "100%"]
    elif sub == "Cytologie":
        q = "Où se déroule la synthèse des protéines dans la cellule ?"
        corr = "Les ribosomes"
        options = [corr, "Le noyau", "L'appareil de Golgi", "Les lysosomes"]
    else:
        q = "Quelle hormone est responsable de la baisse du taux de glucose dans le sang ?"
        corr = "Insuline"
        options = [corr, "Glucagon", "Adrénaline", "Cortisol"]
    return "Biologie", q, corr, options

# --- MOTORE DELL'APP ---

if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'answered' not in st.session_state: st.session_state.answered = False

def next_question():
    f = random.choice([get_math, get_physique, get_chimie, get_biologie])
    cat, q, corr, opts = f()
    random.shuffle(opts)
    st.session_state.current_q = {"cat": cat, "q": q, "corr": corr, "opts": opts}
    st.session_state.answered = False

if st.session_state.current_q is None:
    next_question()

# UI
st.title("🚀 Master Prépa - Simulation Totale")
st.sidebar.header("Statistiques")
st.sidebar.metric("Score", f"{st.session_state.score} / {st.session_state.total}")

curr = st.session_state.current_q
st.subheader(f"Matière : {curr['cat']}")
st.markdown(f"**{curr['q']}**")

for o in curr['opts']:
    if st.button(o, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if o == curr['corr']:
            st.session_state.score += 1
            st.success("Correct ! ✨")
        else:
            st.error(f"Faux. La réponse était : {curr['corr']}")

if st.session_state.answered:
    if st.button("Question Suivante ➡️"):
        next_question()
        st.rerun()

if st.sidebar.button("Réinitialiser le score"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.rerun()
