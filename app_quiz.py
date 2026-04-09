import streamlit as st
import random
import math

# Configurazione Pagina
st.set_page_config(page_title="Quizzeo ARES Infinite", page_icon="🩺", layout="centered")

# --- MOTORE DI GENERAZIONE INFINITA (Stile ARES) ---

def gen_math():
    tipo = random.choice(["vecteurs", "trigo", "derivee", "geometrie"])
    if tipo == "vecteurs":
        c = random.randint(2, 12)
        punti = random.sample(["A","B","C","D","P","Q","R","S"], 4)
        q = f"Dans un carré {punti[0]}{punti[1]}{punti[2]}{punti[3]} de côté {c}, que vaut le produit scalaire $\\vec{{{punti[0]}{punti[1]}}} \\cdot \\vec{{{punti[2]}{punti[1]}}}$ ?"
        ans = "0"
        opts = ["0", str(c), str(c**2), str(-c**2)]
    elif tipo == "derivee":
        a = random.randint(2, 9)
        q = f"Quelle est la dérivée de la fonction $f(x) = {a}x^2 + \\ln(x)$ ?"
        ans = f"${2*a}x + 1/x$"
        opts = [ans, f"${a}x + 1/x$", f"${2*a}x - 1/x^2$", f"${a**2}x + 1$"]
    else:
        val = random.choice([30, 45, 60])
        rad = {30: "1/2", 45: "\\sqrt{2}/2", 60: "\\sqrt{3}/2"}
        q = f"Quelle est la valeur de $\\sin({val}^\\circ)$ ?"
        ans = f"${rad[val]}$"
        opts = [ans, "$1$", "$\\sqrt{3}/3$", "$0$"]
    return q, ans, opts, "Mathématiques"

def gen_chimie():
    tipo = random.choice(["densite", "ph", "stoechio"])
    if tipo == "densite":
        m_v = random.randint(10, 30)
        vol = random.choice([10, 20, 25, 50, 100])
        rho = round(random.uniform(0.6, 2.5), 2)
        m_tot = round(m_v + (rho * vol), 1)
        q = f"Un récipient de {m_v}g contient {vol} cm³ d'un liquide. La masse totale est de {m_tot}g. Quelle est la masse volumique ?"
        ans = f"{rho} g/cm³"
        opts = [ans, f"{round(rho*1.5, 1)} g/cm³", f"{round(rho/2, 1)} g/cm³", "1.0 g/cm³"]
    elif tipo == "ph":
        exp = random.randint(1, 5)
        q = f"Quel est le pH d'une solution d'acide fort concentrée à $10^{{-{exp}}}$ mol/L ?"
        ans = str(exp)
        opts = [ans, str(14-exp), str(exp+1), "7"]
    else:
        q = "Dans une réaction d'oxydoréduction, l'agent réducteur est l'espèce qui :"
        ans = "Perd des électrons (s'oxyde)"
        opts = [ans, "Gagne des électrons", "Perd des protons", "Reste neutre"]
    return q, ans, opts, "Chimie"

def gen_physique():
    tipo = random.choice(["optique", "meca", "elec"])
    if tipo == "optique":
        f = random.choice([10, 20, 25, 50])
        q = f"Quelle est la vergence d'une lentille convergente ayant une distance focale de {f} cm ?"
        ans = f"{100//f} dioptries"
        opts = [ans, f"{f/10} dioptries", "0.5 dioptries", f"{100/f*2} dioptries"]
    elif tipo == "meca":
        m = random.randint(2, 20)
        q = f"Quelle est l'énergie cinétique d'un objet de {m} kg se déplaçant à 4 m/s ?"
        res = 0.5 * m * (4**2)
        ans = f"{int(res)} J"
        opts = [ans, f"{m*4} J", f"{int(res*2)} J", "10 J"]
    else:
        v = random.randint(10, 50)
        r = random.randint(2, 10)
        q = f"Un circuit a une tension de {v}V et une résistance de {r} $\\Omega$. Quelle est l'intensité I ?"
        ans = f"{round(v/r, 2)} A"
        opts = [ans, f"{v*r} A", f"{v+r} A", "0.5 A"]
    return q, ans, opts, "Physique"

def gen_bio():
    # Database di concetti ARES ad alta variabilità
    concepts = [
        ("La phase S de l'interphase est caractérisée par :", "La réplication de l'ADN", ["La division du cytoplasme", "La condensation des chromosomes", "La synthèse des ribosomes"]),
        ("L'organite responsable de la respiration cellulaire est :", "La mitochondrie", ["Le chloroplaste", "Le lysosome", "Le noyau"]),
        ("Le code génétique est dit 'dégénéré' car :", "Plusieurs codons codent pour le même acide aminé", ["Un codon code pour plusieurs acides aminés", "Il change selon l'espèce", "Il contient des erreurs"]),
        ("Un individu de groupe sanguin O possède :", "Des anticorps anti-A et anti-B", ["Des antigènes A et B", "Aucun anticorps", "Uniquement l'antigène O"]),
        ("La mitose produit :", "Deux cellules filles génétiquement identiques", ["Quatre cellules haploïdes", "Une cellule œuf", "Des gamètes"]),
        ("Où se trouve l'ARN ribosomal ?", "Dans le nucléole", ["Dans la membrane", "Dans les mitochondries", "Dans les vacuoles"])
    ]
    item = random.choice(concepts)
    return item[0], item[1], item[2] + [item[1]], "Biologie"

# --- LOGICA APPLICAZIONE ---

if 'state' not in st.session_state:
    st.session_state.state = "menu"
    st.session_state.score = 0.0
    st.session_state.current_idx = 0
    st.session_state.questions = []
    st.session_state.answered = False

def start_session(subject):
    st.session_state.questions = []
    # Genera 10 domande uniche al volo
    for _ in range(10):
        if subject == "Mathématiques": q, a, o, c = gen_math()
        elif subject == "Chimie": q, a, o, c = gen_chimie()
        elif subject == "Physique": q, a, o, c = gen_physique()
        else: q, a, o, c = gen_bio()
        
        # Mischia le opzioni
        opts = list(set(o)) # rimuove duplicati
        random.shuffle(opts)
        
        st.session_state.questions.append({"q": q, "ans": a, "opts": opts, "cat": c})
    
    st.session_state.state = "quiz"
    st.session_state.current_idx = 0
    st.session_state.score = 0.0
    st.session_state.answered = False

def check_ans(choice, correct):
    st.session_state.answered = True
    if choice == correct:
        st.session_state.score += 1.0
    else:
        st.session_state.score -= (1/3)

# --- UI STREAMLIT ---

st.title("🩺 Quizzeo ARES - Infinite Mode")
st.markdown("---")

if st.session_state.state == "menu":
    st.subheader("Choisissez votre épreuve (10 questions uniques)")
    cols = st.columns(2)
    with cols[0]:
        st.button("🧬 Biologie", use_container_width=True, on_click=start_session, args=("Biologie",))
        st.button("🧪 Chimie", use_container_width=True, on_click=start_session, args=("Chimie",))
    with cols[1]:
        st.button("📐 Mathématiques", use_container_width=True, on_click=start_session, args=("Mathématiques",))
        st.button("⚡ Physique", use_container_width=True, on_click=start_session, args=("Physique",))

elif st.session_state.state == "quiz":
    q_data = st.session_state.questions[st.session_state.current_idx]
    
    # Header e progresso
    st.caption(f"Matière: {q_data['cat']} | Question {st.session_state.current_idx + 1}/10")
    st.progress((st.session_state.current_idx + 1) / 10)
    
    st.subheader(q_data['q'])
    
    # Bottoni Risposta
    for opt in q_data['opts']:
        st.button(opt, use_container_width=True, key=f"opt_{st.session_state.current_idx}_{opt}", 
                  disabled=st.session_state.answered, on_click=check_ans, args=(opt, q_data['ans']))
    
    if st.session_state.answered:
        if st.session_state.score > -100: # Solo per triggerare il refresh visivo
            st.info(f"Réponse correcte: **{q_data['ans']}**")
        
        if st.session_state.current_idx < 9:
            if st.button("Question Suivante ➡️", type="primary"):
                st.session_state.current_idx += 1
                st.session_state.answered = False
                st.rerun()
        else:
            if st.button("Voir le Score Final 🏁", type="primary"):
                st.session_state.state = "result"
                st.rerun()

elif st.session_state.state == "result":
    st.balloons()
    st.header("🏁 Test Terminé !")
    final_score = round(st.session_state.score, 2)
    st.metric("Votre score final (ARES)", f"{final_score} / 10")
    st.write("*(Rappel: +1 pour une bonne réponse, -1/3 pour une mauvaise)*")
    
    if st.button("🔄 Retour au menu principal"):
        st.session_state.state = "menu"
        st.rerun()
