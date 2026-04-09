import streamlit as st
import random
import math

st.set_page_config(page_title="Simulateur Concours Infini", page_icon="♾️")

# --- FUNZIONI DI GENERAZIONE INFINITA ---

def gen_math_vrai():
    # Modello: Prodotto scalare nel quadrato (Immagine 3)
    L = random.randint(2, 10)
    # Calcolo: PQ * RP = PQ * (RQ + QP) = 0 - PQ^2 = -L^2
    correct = -(L**2)
    q = f"Dans le plan euclidien, on considère un carré PQRS de côtés de longueur {L}. Que vaut le produit scalaire PQ · RP ?"
    wrongs = [L**2, 0, -(L), L]
    return "Mathématiques", q, str(correct), [str(w) for w in wrongs if w != correct][:3]

def gen_chimie_vrai():
    # Modello: Massa Volumica (Immagine 2)
    m_vide = round(random.uniform(10.0, 20.0), 2)
    vol = random.randint(5, 15)
    m_eau = round(m_vide + vol, 2) # densità acqua = 1g/cm3
    densite_X = round(random.uniform(2.0, 8.0), 3)
    m_liquide_X = round(m_vide + (vol * densite_X), 2)
    
    q = f"Un récipient vide de {m_vide}g est rempli d'eau: masse = {m_eau}g. Le même récipient rempli d'un liquide inconnu vaut {m_liquide_X}g. Quelle est la masse volumique du liquide ?"
    correct = f"{densite_X} g/cm³"
    wrongs = [f"{round(densite_X/10, 3)} g/cm³", f"{round(densite_X*2, 3)} g/cm³", f"{round(densite_X+1, 3)} g/cm³"]
    return "Chimie", q, correct, wrongs

def gen_physique_vrai():
    # Modello: Ottica e Ombre (Immagine 4)
    # Qui variamo il contesto ma la logica fisica resta la stessa
    objets = ["une araignée", "une petite branche", "une feuille", "un insecte"]
    obj = random.choice(objets)
    q = f"Un faisceau de lumière vertical éclaire {obj} posé sur l'eau. Si la surface de l'eau s'incurve vers le BAS (concave), l'ombre au fond sera..."
    correct = "Plus grande che l'objet"
    wrongs = ["Plus petite che l'objet", "De même taille", "Inexistante"]
    return "Physique", q, correct, wrongs

def gen_bio_vrai():
    # Modello: Organelli e Funzioni (Immagine 1)
    db = [
        ("le cycle de Krebs", "La mitochondrie", ["Le chloroplaste", "Le noyau", "Le lysosome"]),
        ("la photosynthèse", "Le chloroplaste", ["La mitochondrie", "Le ribosome", "L'appareil de Golgi"]),
        ("la synthèse des protéines", "Le ribosome", ["Le nucléole", "Le centrosome", "La vacuole"]),
        ("le stockage de l'information génétique", "Le noyau", ["Le cytoplasme", "La membrane", "Le réticulum"])
    ]
    item = random.choice(db)
    q = f"Lequel des organites suivants abrite {item[0]} ?"
    return "Biologie", q, item[1], item[2]

# --- LOGICA DELL'APP ---

if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0

st.title("🎓 Concours Universitaire Infini")
st.write("Les questions sont générées mathématiquement à chaque clic.")

# Sceglie una funzione a caso tra le 4
gen_func = random.choice([gen_math_vrai, gen_chimie_vrai, gen_physique_vrai, gen_bio_vrai])
cat, quest, corr, wrngs = gen_func()

st.subheader(f"Matière : {cat}")
st.info(quest)

# Mescola le opzioni
options = wrngs + [corr]
random.shuffle(options)

# Visualizzazione bottoni
col1, col2 = st.columns(2)
for i, opt in enumerate(options):
    with (col1 if i % 2 == 0 else col2):
        if st.button(opt, use_container_width=True):
            st.session_state.total += 1
            if opt == corr:
                st.success("Correct ! ✅")
                st.session_state.score += 1
            else:
                st.error(f"Faux ! La réponse était : {corr} ❌")
            st.button("Question Suivante ➡️")

st.sidebar.metric("Punteggio", f"{st.session_state.score} / {st.session_state.total}")
