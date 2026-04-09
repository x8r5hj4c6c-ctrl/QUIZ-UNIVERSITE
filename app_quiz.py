import streamlit as st
import random
import math

st.set_page_config(page_title="Simulateur Concours Élite", page_icon="🏆")

# --- SISTEMA ANTI-RIPETIZIONE ---
if 'seen_questions' not in st.session_state:
    st.session_state.seen_questions = set()

# --- GENERATORI DI ALTO LIVELLO ---

def get_math_expert():
    sub = random.choice(["Trigo", "Analyse", "Vecteurs"])
    if sub == "Trigo":
        # Calcolo di angoli non banali
        val = random.choice([30, 45, 60])
        rad = {30: "π/6", 45: "π/4", 60: "π/3"}
        q = f"Quelle est la valeur exacte de sin({rad[val]}) + cos({rad[val]})² ?"
        res = round(math.sin(math.radians(val)) + (math.cos(math.radians(val))**2), 3)
        corr = str(res)
        options = [corr, "1", "1.5", "0.75"]
    elif sub == "Analyse":
        a = random.randint(2, 5)
        q = f"Calculez la limite de ( {a}x² - 5x ) / ( x² + 1 ) quand x tend vers l'infini."
        corr = str(a)
        options = [corr, "0", "∞", "1"]
    else: # Vecteurs 3D
        q = "Dans un repère orthonormé, soit u(1, 2, -1) et v(2, -1, 0). Que vaut leur produit scalaire ?"
        corr = "0" # 1*2 + 2*(-1) + (-1)*0 = 0
        options = ["0", "1", "-1", "5"]
    return "Mathématiques", q, corr, options

def get_physique_expert():
    sub = random.choice(["Cinématique", "Thermodynamique", "Optique"])
    if sub == "Cinématique":
        v0 = random.randint(10, 20)
        t = 2
        q = f"Un objet est lancé verticalement vers le haut avec v0 = {v0} m/s. Quelle est sa hauteur après {t}s ? (g ≈ 10 m/s²)"
        # y = v0*t - 0.5*g*t^2
        h = v0*t - 0.5*10*(t**2)
        corr = f"{h} m"
        options = [corr, f"{v0*t} m", f"{h+10} m", "5 m"]
    elif sub == "Thermodynamique":
        q = "Selon le deuxième principe de la thermodynamique, dans un système isolé, l'entropie :"
        corr = "Ne peut que croître"
        options = [corr, "Reste constante", "Diminue toujours", "S'annule au zéro absolu"]
    else: # Optique / Snell-Descartes
        q = "Un rayon passe du verre (n=1.5) à l'air (n=1). L'angle limite de réflexion totale est environ :"
        corr = "42°"
        options = ["42°", "30°", "60°", "90°"]
    return "Physique", q, corr, options

def get_chimie_expert():
    sub = random.choice(["pH", "Thermochimie", "Organique"])
    if sub == "pH":
        c = random.choice([0.01, 0.001, 0.0001])
        q = f"Quel est le pH d'une solution d'acide chlorhydrique (acide fort) de concentration {c} mol/L ?"
        corr = str(int(-math.log10(c)))
        options = [corr, str(int(-math.log10(c))+1), "7", "14"]
    elif sub == "Organique":
        q = "Quelle est la configuration d'un carbone lié à 4 groupements différents ?"
        corr = "Chiral"
        options = ["Chiral", "Achromatique", "Isomère plan", "Linéaire"]
    else:
        q = "Dans une réaction exothermique, la variation d'enthalpie (ΔH) est :"
        corr = "Négative (ΔH < 0)"
        options = [corr, "Positive (ΔH > 0)", "Nulle", "Infinie"]
    return "Chimie", q, corr, options

def get_biologie_expert():
    sub = random.choice(["Biologie Moléculaire", "Immunologie", "Évolution"])
    if sub == "Biologie Moléculaire":
        q = "Quelle enzyme est responsable de l'ouverture de la double hélice d'ADN lors de la réplication ?"
        corr = "Hélicase"
        options = ["Hélicase", "ADN Polymérase", "Ligase", "Primase"]
    elif sub == "Immunologie":
        q = "Quelles cellules sont responsables de la production d'anticorps ?"
        corr = "Plasmocytes (Lymphocytes B)"
        options = [corr, "Lymphocytes T4", "Macrophages", "NK Cells"]
    else:
        q = "Quel organite possède son propre ADN circulaire, suggérant une origine endosymbiotique ?"
        corr = "Mitochondrie"
        options = ["Mitochondrie", "Appareil de Golgi", "Réticulum", "Lysosome"]
    return "Biologie", q, corr, options

# --- MOTORE PRINCIPALE ---

if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'answered' not in st.session_state: st.session_state.answered = False

def get_unique_question():
    attempts = 0
    while attempts < 100: # Evita loop infiniti
        f = random.choice([get_math_expert, get_physique_expert, get_chimie_expert, get_biologie_expert])
        cat, q, corr, opts = f()
        q_id = f"{cat}-{q}"
        if q_id not in st.session_state.seen_questions:
            st.session_state.seen_questions.add(q_id)
            return cat, q, corr, opts
        attempts += 1
    # Se tutte sono state viste, resetta la memoria
    st.session_state.seen_questions.clear()
    return get_unique_question()

if st.session_state.current_q is None:
    cat, q, corr, opts = get_unique_question()
    random.shuffle(opts)
    st.session_state.current_q = {"cat": cat, "q": q, "corr": corr, "opts": opts}

# --- UI ---
st.title("🏆 Concours Élite - Mode Expert")
st.sidebar.metric("Précision", f"{st.session_state.score}/{st.session_state.total}")
st.sidebar.write(f"Questions explorées : {len(st.session_state.seen_questions)}")

curr = st.session_state.current_q
st.subheader(f"{curr['cat']}")
st.markdown(f"**{curr['q']}**")

for o in curr['opts']:
    if st.button(o, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if o == curr['corr']:
            st.session_state.score += 1
            st.success("Correct ! Excellent niveau. ✨")
        else:
            st.error(f"Faux. La réponse experte était : {curr['corr']}")

if st.session_state.answered:
    if st.button("Question Suivante ➡️"):
        st.session_state.current_q = None
        st.session_state.answered = False
        st.rerun()
