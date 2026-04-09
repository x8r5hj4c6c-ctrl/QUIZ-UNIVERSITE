import streamlit as st
import random

# Configurazione Pagina
st.set_page_config(page_title="Quiz Universitaire", page_icon="🎓")

# Inizializzazione variabili di sessione (per non perdere il punteggio al refresh)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'question_data' not in st.session_state:
    st.session_state.question_data = None

def generate_question():
    choice = random.choice(["Math", "Phys", "Chim", "Bio"])
    if choice == "Math":
        a, n = random.randint(2, 9), random.randint(2, 5)
        q, c, w = f"Dérivée de f(x) = {a}x^{n} ?", f"{a*n}x^{n-1}", [f"{a}x^{n-1}", f"{a*n}x^{n}", "0"]
    elif choice == "Phys":
        m, a = random.randint(5, 20), random.randint(2, 5)
        q, c, w = f"Force (F) pour m={m}kg et a={a}m/s² ?", f"{m*a} N", [f"{m+a} N", f"{m*a*2} N", "0 N"]
    elif choice == "Chim":
        q, c, w = "Symbole du Potassium ?", "K", ["P", "Po", "Pt"]
    else:
        q, c, w = "Organelle de la respiration ?", "Mitochondrie", ["Ribosome", "Noyau", "Golgi"]
    
    options = [c] + w
    random.shuffle(options)
    return {"cat": choice, "q": q, "c": c, "options": options}

# Titolo e Score
st.title("🎓 Quiz Prépa Universitaire")
st.write(f"**Score : {st.session_state.score} / {st.session_state.total}**")

# Genera la prima domanda se non esiste
if st.session_state.question_data is None:
    st.session_state.question_data = generate_question()

# Mostra Domanda
data = st.session_state.question_data
st.info(f"Domaine : {data['cat']}")
st.subheader(data['q'])

# Bottoni per le risposte
for opt in data['options']:
    if st.button(opt, use_container_width=True):
        st.session_state.total += 1
        if opt == data['c']:
            st.session_state.score += 1
            st.success("Correct ! ✅")
        else:
            st.error(f"Faux ! La réponse était : {data['c']} ❌")
        
        # Rigenera domanda per il prossimo turno
        st.session_state.question_data = generate_question()
        st.button("Question Suivante ➡️")