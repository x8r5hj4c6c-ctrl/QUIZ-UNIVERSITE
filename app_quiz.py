import streamlit as st
import random
import math
import uuid

# Configurazione della pagina
st.set_page_config(page_title="Quizzeo - Matteo S.", page_icon="🩺", layout="centered")

# --- MOTORE DI GENERAZIONE AVANZATA (Stile Concorso ARES) ---

def generate_chemistry():
    """Genera problemi di massa volumica con conversioni di unità complesse."""
    m_vide = round(random.uniform(10.0, 25.0), 2)
    vol_cm3 = random.choice([10, 20, 25, 50, 100])
    # Rho reale del liquido in g/cm3
    rho_val = round(random.uniform(0.7, 13.6), 3)
    m_liquide = round(rho_val * vol_cm3, 2)
    m_totale = round(m_vide + m_liquide, 2)
    
    q = (f"Un récipient vide a une masse de {m_vide} g. Lorsqu'il est totalement rempli d'un certain volume d'eau, "
         f"sa masse est de {round(m_vide + vol_cm3, 2)} g. L'expérience est répétée avec un liquide inconnu et "
         f"la masse totale mesurée est de {m_totale} g. (Donnée : $\\rho_{{eau}} = 1.0$ g/cm³)")
    
    # Risposta corretta in diverse unità per complicare
    unit = random.choice(["g/cm3", "kg/m3", "dg/cm3"])
    if unit == "g/cm3":
        ans = f"{rho_val} g/cm³"
        wrong = [f"{round(rho_val/10, 3)} g/cm³", f"{round(rho_val*1.2, 3)} g/cm³", f"{round(rho_val-0.5, 3)} g/cm³"]
    elif unit == "kg/m3":
        ans = f"{round(rho_val * 1000, 1)} kg/m³"
        wrong = [f"{round(rho_val * 100, 1)} kg/m³", f"{rho_val} kg/m³", f"{round(rho_val * 10, 1)} kg/m³"]
    else: # decigrammi/cm3
        ans = f"{round(rho_val * 10, 2)} dg/cm³"
        wrong = [f"{rho_val} dg/cm³", f"{round(rho_val/10, 2)} dg/cm³", f"{round(rho_val*100, 2)} dg/cm³"]
    
    return "Chimie", q, ans, wrong

def generate_math():
    """Vettori e geometria del piano (Quadrato PQRS)."""
    c = random.randint(2, 10)
    variant = random.choice(["PQ_RP", "PQ_RS", "PR_QS", "DIAG"])
    
    if variant == "PQ_RP":
        q = f"Dans le plan euclidien, on considère un carré PQRS de côté {c}. Que vaut le produit scalaire $\\vec{{PQ}} \\cdot \\vec{{RP}}$ ?"
        # PQ è (c, 0), RP è (-c, -c) -> dot = -c^2
        ans = str(-(c**2))
        wrong = ["0", str(c**2), str(c), str(-c)]
    elif variant == "PQ_RS":
        q = f"Soit un carré PQRS de côté {c}. Calculez le produit scalaire $\\vec{{PQ}} \\cdot \\vec{{RS}}$."
        # Vettori opposti: PQ=(c,0), RS=(-c,0) -> dot = -c^2
        ans = str(-(c**2))
        wrong = ["0", str(c**2), str(2*c), str(-2*c)]
    elif variant == "PR_QS":
        q = f"Dans un carré PQRS de côté {c}, que vaut le produit scalaire des diagonales $\\vec{{PR}} \\cdot \\vec{{QS}}$ ?"
        ans = "0"
        wrong = [str(c**2), str(2*(c**2)), str(-(c**2)), "1"]
    else:
        q = f"Quelle est la norme du vecteur $\\vec{{PQ}} + \\vec{{PS}}$ dans un carré PQRS de côté {c} ?"
        # Somma di due lati adjacenti = diagonale = c*sqrt(2)
        ans = f"{c}$\\sqrt{{2}}$"
        wrong = [str(2*c), str(c**2), f"{c/2}$\\sqrt{{2}}$", str(c)]
        
    return "Mathématiques", q, ans, wrong

def generate_physics():
    """Ottica e fenomeni di superficie (Stile Araignée d'eau)."""
    n1 = 1.0 # aria
    n2 = 1.33 # acqua
    q_type = random.choice(["OMBRE", "REFRACTION", "SNELL"])
    
    if q_type == "OMBRE":
        q = ("Une araignée d'eau repose sur la surface d'une mare. La tension superficielle crée une dépression concave "
             "sous ses pattes. Si les rayons du soleil sont verticaux, l'ombre au fond est :")
        ans = "Plus grande que l'insecte"
        wrong = ["Plus petite che l'insecte", "De même taille", "Inexistante (réflexion totale)", "Inversée"]
    elif q_type == "REFRACTION":
        val = random.randint(10, 40)
        q = f"Un rayon lumineux passe de l'air (n=1) à l'eau (n=1.33) avec un angle d'incidence de {val}°. Le rayon réfracté :"
        ans = "Se rapproche de la normale"
        wrong = ["S'éloigne de la normale", "Reste rectiligne", "Est totalement réfléchi", "Disparaît"]
    else:
        q = "L'indice de réfraction d'un milieu transparent est n=2.0. Quelle est la vitesse de la lumière dans ce milieu ?"
        ans = "1,5 x $10^8$ m/s"
        wrong = ["3,0 x $10^8$ m/s", "6,0 x $10^8$ m/s", "2,0 x $10^8$ m/s", "0,75 x $10^8$ m/s"]
        
    return "Physique", q, ans, wrong

def generate_biology():
    """Biologia cellulare e biochimica (Krebs, organelli)."""
    topics = [
        ("Le cycle de Krebs (ou cycle de l'acide citrique) se déroule spécifiquement dans :", "La matrice mitochondriale", ["L'espace intermembranaire", "Le cytosol", "Le stroma", "Le reticulum"]),
        ("Quelle est la fonction principale de l'appareil de Golgi ?", "La maturation et le tri des protéines", ["La synthèse des lipides", "La digestion intracellulaire", "La réplication de l'ADN", "La synthèse de l'ATP"]),
        ("Dans la cellule eucaryote, la traduction de l'ARNm en protéines a lieu au niveau :", "Des ribosomes", ["Du noyau", "Des lysosomes", "Des peroxysomes", "Des centrioles"]),
        ("La glycolyse est une étape du métabolisme énergétique qui a lieu dans :", "Le cytoplasme", ["La mitochondrie", "Le noyau", "Le chloroplaste", "La membrane plasmique"])
    ]
    topic = random.choice(topics)
    return "Biologie", topic[0], topic[1], topic[2]

# --- GESTIONE DELLO STATO (ANTI-RIPETIZIONE) ---

if 'deck' not in st.session_state:
    st.session_state.deck = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

def refresh_deck():
    """Crea un nuovo mazzo di 20 domande uniche."""
    new_questions = []
    generators = [generate_chemistry, generate_math, generate_physics, generate_biology]
    for _ in range(20):
        gen = random.choice(generators)
        cat, q, ans, wrong = gen()
        new_questions.append({
            "id": str(uuid.uuid4()),
            "cat": cat,
            "q": q,
            "ans": ans,
            "options": random.sample([ans] + wrong, 4)
        })
    random.shuffle(new_questions)
    st.session_state.deck = new_questions

def get_next_question():
    if not st.session_state.deck:
        refresh_deck()
    st.session_state.current_question = st.session_state.deck.pop()
    st.session_state.answered = False

# --- INTERFACCIA UTENTE ---

st.markdown("<h1 style='text-align: center;'>Quizzeo - Prodotto da Matteo S.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Simulateur Concours Médecine/Dentisterie (ARES)</p>", unsafe_allow_html=True)
st.divider()

if st.session_state.current_question is None:
    get_next_question()

curr = st.session_state.current_question

# Sidebar statistiche
st.sidebar.title("📈 Performance")
st.sidebar.metric("Précision", f"{st.session_state.score} / {st.session_state.total}")
st.sidebar.write(f"Questions restantes dans le deck: {len(st.session_state.deck)}")
if st.sidebar.button("Réinitialiser le test"):
    st.session_state.score = 0
    st.session_state.total = 0
    refresh_deck()
    get_next_question()
    st.rerun()

# Layout domanda
st.subheader(f"Matière : {curr['cat']}")
st.write(curr['q'])

# Risposte
for opt in curr['options']:
    if st.button(opt, key=f"btn_{curr['id']}_{opt}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if opt == curr['ans']:
            st.session_state.score += 1
            st.success("Correct ! ✨")
        else:
            st.error(f"Faux. La réponse correcte était : {curr['ans']}")

# Navigazione
if st.session_state.answered:
    if st.button("Question Suivante ➡️", type="primary", use_container_width=True):
        get_next_question()
        st.rerun()
