import streamlit as st
import random
import math
import uuid

st.set_page_config(page_title="Quizzeo - Matteo S.", page_icon="🎓", layout="centered")

# --- MOTORE DI GENERAZIONE INFINITA ---

def gen_math_pro():
    # Varianti: Prodotto scalare, Norme, Angoli, Punti medi
    tipo = random.choice(["scalaire", "norme", "angle", "point_m"])
    pts = ["P", "Q", "R", "S", "A", "B", "C", "D"]
    random.shuffle(pts)
    c = random.randint(2, 50)
    
    if tipo == "scalaire":
        q = f"Dans un carré {pts[0]}{pts[1]}{pts[2]}{pts[3]} de côté {c}, que vaut il produit scalaire {pts[0]}{pts[1]} · {pts[1]}{pts[2]} ?"
        corr, opts = "0", ["0", str(c), str(c**2), "1"]
    elif tipo == "norme":
        q = f"Quelle est la longueur de la diagonale d'un carré de côté {c} ?"
        res = f"{c}√2"
        corr, opts = res, [res, str(c*2), str(c**2), f"{c}√3"]
    else:
        q = f"Dans un plan euclidien, le produit scalaire de deux vecteurs orthogonaux de norme {c} est sempre :"
        corr, opts = "0", ["0", str(c), "1", "Dépend du côté"]
    return "Mathématiques", q, corr, opts

def gen_chimie_pro():
    # Varianti: Massa volumica con numeri casuali (Migliaia di combinazioni)
    m_vide = round(random.uniform(10.0, 30.0), 2)
    vol = random.randint(10, 100)
    rho_liquide = round(random.uniform(0.5, 15.0), 3)
    m_total = round(m_vide + (vol * rho_liquide), 2)
    
    tipo_unita = random.choice(["g/cm³", "kg/m³", "dg/cm³"])
    
    q = f"Un récipient vide pèse {m_vide}g. Rempli avec {vol}cm³ d'un liquide inconnu, sa masse totale est {m_total}g. Quelle est la masse volumique ?"
    
    if tipo_unita == "g/cm³":
        corr = f"{rho_liquide} g/cm³"
    else:
        corr = f"{rho_liquide * 10} dg/cm³" # Esempio conversione
        
    opts = [corr, f"{round(rho_liquide/2, 2)} g/cm³", f"{round(rho_liquide+2, 2)} g/cm³", "1.0 g/cm³"]
    return "Chimie", q, corr, opts

def gen_physique_pro():
    # Varianti: Ottica, Rifrazione, Tensioni
    val = random.randint(30, 60)
    temi = [
        ("Si la surface de l'eau est concave, l'ombre au fond est...", "Plus grande que l'insecte", ["Plus grande que l'insecte", "Plus petite", "Identique", "Nulle"]),
        (f"Un rayon passe de l'air (n=1) à un liquide (n=1.5) con un angle de {val}°. Le rayon réfracté est...", "Plus proche de la normale", ["Plus proche de la normale", "Plus éloigné", "Parallèle", "Réfléchi"]),
        ("La tension superficielle de l'eau diminue si on ajoute...", "Du savon", ["Du savon", "Du sel", "De la glace", "Du sable"])
    ]
    t = random.choice(temi)
    return "Physique", t[0], t[1], t[2]

def gen_bio_pro():
    # Varianti: Organelli e Funzioni
    bio_pool = [
        ("Où se déroule le cycle de Krebs ?", "La mitochondrie", ["La mitochondrie", "Le noyau", "Le chloroplaste", "Le ribosome"]),
        ("Quel organite synthétise les protéines ?", "Le ribosome", ["Le ribosome", "Le lysosome", "L'appareil de Golgi", "La vacuole"]),
        ("Où se trouve l'ADN nucléaire ?", "Le noyau", ["Le noyau", "Le cytoplasme", "La mitochondrie", "Le centrosome"]),
        ("La photosynthèse a lieu dans...", "Le chloroplaste", ["Le chloroplaste", "La paroi", "Le noyau", "La mitochondrie"])
    ]
    b = random.choice(bio_pool)
    return "Biologie", b[0], b[1], b[2]

# --- LOGICA APPLICAZIONE ---

if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'answered' not in st.session_state: st.session_state.answered = False

def next_question():
    # Sceglie un generatore a caso
    f = random.choice([gen_math_pro, gen_chimie_pro, gen_physique_pro, gen_bio_pro])
    cat, q, corr, opts = f()
    
    # Evita duplicati nelle opzioni e mescola
    unique_opts = list(dict.fromkeys(opts))
    if corr not in unique_opts: unique_opts.append(corr)
    random.shuffle(unique_opts)
    
    st.session_state.current_q = {
        "cat": cat, "q": q, "corr": corr, "opts": unique_opts, "id": str(uuid.uuid4())
    }
    st.session_state.answered = False

if st.session_state.current_q is None:
    next_question()

# --- INTERFACCIA ---
st.title("Quizzeo - Prodotto da Matteo S.")
st.write("Generatore di domande infinito basato sui tuoi argomenti.")
st.divider()

curr = st.session_state.current_q

st.sidebar.metric("Punteggio", f"{st.session_state.score} / {st.session_state.total}")
if st.sidebar.button("Reset"):
    st.session_state.score = 0
    st.session_state.total = 0
    next_question()
    st.rerun()

st.subheader(f"Matière: {curr['cat']}")
st.info(curr['q'])

# Bottoni risposte
for idx, opt in enumerate(curr['opts']):
    if st.button(opt, key=f"{curr['id']}_{idx}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if opt == curr['corr']:
            st.session_state.score += 1
            st.success("Correct ! ✨")
        else:
            st.error(f"Faux. La réponse était : {curr['corr']}")

if st.session_state.answered:
    if st.button("Prossima Domanda ➡️", type="primary"):
        next_question()
        st.rerun()
