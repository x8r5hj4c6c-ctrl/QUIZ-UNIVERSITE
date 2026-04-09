import streamlit as st
import random

st.set_page_config(page_title="Concours Universitaire Infini", page_icon="🎓")

# --- INIZIALIZZAZIONE STATO ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = None

# --- FUNZIONI DI GENERAZIONE (LOGICA FISSA) ---
def generate_new_question():
    tipo = random.choice(["math", "chimie", "physique", "bio"])
    
    if tipo == "math":
        L = random.randint(2, 10)
        corr = -(L**2)
        q = f"Dans le plan euclidien, un carré PQRS a des côtés de longueur {L}. Que vaut le produit scalaire PQ · RP ?"
        options = [str(corr), str(L**2), "0", str(-L)]
    
    elif tipo == "chimie":
        m_vide = round(random.uniform(10.0, 20.0), 2)
        vol = random.randint(5, 15)
        m_eau = round(m_vide + vol, 2)
        densite = round(random.uniform(2.0, 5.0), 2)
        m_X = round(m_vide + (vol * densite), 2)
        q = f"Récipient vide: {m_vide}g. Con acqua: {m_eau}g. Con liquido X: {m_X}g. Massa volumica di X (g/cm³)?"
        options = [str(densite), str(round(densite/2, 2)), str(round(densite+1.5, 2)), "1.00"]
        
    elif tipo == "physique":
        q = "Une araignée d'eau déforme la surface vers le BAS (concave). L'ombre au fond est..."
        options = ["Plus grande que l'insecte", "Plus petite que l'insecte", "De même taille", "Inexistante"]
        
    else: # Bio
        items = [("le cycle de Krebs", "Mitochondrie"), ("la photosynthèse", "Chloroplaste"), ("l'ADN", "Noyau")]
        item = random.choice(items)
        q = f"Quel organite abrite {item[0]} ?"
        options = [item[1], "Ribosome", "Appareil de Golgi", "Lysosome"]

    correct = options[0]
    random.shuffle(options)
    return {"question": q, "options": options, "correct": correct}

# --- LOGICA DI NAVIGAZIONE ---
if st.session_state.current_q is None or st.sidebar.button("Nouvelle Question 🔄"):
    st.session_state.current_q = generate_new_question()
    st.session_state.answered = False
    st.rerun()

# --- INTERFACCIA ---
st.title("♾️ Simulateur Concours Infini")
st.sidebar.metric("Score Total", f"{st.session_state.score} / {st.session_state.total}")

q = st.session_state.current_q
st.info(q["question"])

for opt in q["options"]:
    if st.button(opt, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if opt == q["correct"]:
            st.session_state.score += 1
            st.success("Correct ! ✅")
        else:
            st.error(f"Faux ! La réponse était : {q['correct']} ❌")
        st.button("Continuer ➡️") # Cliccando qui ricarica e genera nuova domanda

if st.session_state.answered:
    if st.button("Passer à la question suivante"):
        st.session_state.current_q = generate_new_question()
        st.session_state.answered = False
        st.rerun()
