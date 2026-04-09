import streamlit as st
import random

# Configurazione Pagina
st.set_page_config(page_title="Quizzeo ARES Pro", page_icon="🧬", layout="centered")

# --- DATABASE STRUTTURATO PER SOTTO-ARGOMENTI ---
# Ogni materia ha un dizionario di categorie, ognuna con le sue domande.
DB_ARES = {
    "Biologie": {
        "Cytologie": [{"q": "L'organite responsable de la synthèse protéique est :", "opts": ["Le ribosome", "Le lysosome", "Le nucléole", "Le centrosome"], "ans": "Le ribosome"}],
        "Génétique": [{"q": "Le phénotype d'un individu dépend de :", "opts": ["L'interaction génotype-milieu", "Du génotype uniquement", "Du milieu uniquement", "De l'âge uniquement"], "ans": "L'interaction génotype-milieu"}],
        "Métabolisme": [{"q": "La fermentation lactique produit :", "opts": ["De l'acide lactique et de l'ATP", "Du CO2 e de l'éthanol", "De l'oxygène", "Du glucose"], "ans": "De l'acide lactique et de l'ATP"}],
        "Physiologie": [{"q": "Quelle hormone augmente la réabsorption d'eau par le rein ?", "opts": ["L'ADH (Vasopressine)", "L'insuline", "L'adrénaline", "La thyroxine"], "ans": "L'ADH (Vasopressine)"}],
        "Division Cellulaire": [{"q": "À quelle étape les chromosomes se condensent-ils ?", "opts": ["Prophase", "Métaphase", "Anaphase", "Télophase"], "ans": "Prophase"}],
        "Biochimie": [{"q": "Une liaison peptidique unit deux :", "opts": ["Acides aminés", "Nucléotides", "Acides gras", "Glucides"], "ans": "Acides aminés"}],
        "Évolution": [{"q": "La sélection naturelle favorise :", "opts": ["L'adaptation au milieu", "La mutation aléatoire", "La disparition des espèces", "Le clonage"], "ans": "L'adaptation au milieu"}],
        "Histologie": [{"q": "Le tissu épithélial a pour rôle :", "opts": ["Le revêtement et la protection", "La contraction", "La transmission nerveuse", "Le soutien mécanique"], "ans": "Le revêtement et la protection"}],
        "Immunologie": [{"q": "Les lymphocytes B sont responsables de :", "opts": ["L'immunité humorale", "La phagocytose", "L'immunité cellulaire", "La coagulation"], "ans": "L'immunité humorale"}],
        "Botanique": [{"q": "La sève brute circule dans :", "opts": ["Le xylème", "Le phloème", "Le parenchyme", "L'épiderme"], "ans": "Le xylème"}]
    },
    "Chimie": {
        "Acide/Base": [{"q": "Une solution de pH 5 est :", "opts": ["100 fois plus acide qu'un pH 7", "2 fois plus acide qu'un pH 7", "Basique", "Neutre"], "ans": "100 fois plus acide qu'un pH 7"}],
        "Redox": [{"q": "Dans une réduction, une espèce chimique :", "opts": ["Gagne des électrons", "Perd dei protoni", "Perd des électrons", "Libère de l'oxygène"], "ans": "Gagne des électrons"}],
        "Stoechiométrie": [{"q": "Le volume molaire d'un gaz à 0°C et 1 atm est :", "opts": ["22,4 L/mol", "24,0 L/mol", "1,0 L/mol", "11,2 L/mol"], "ans": "22,4 L/mol"}],
        "Organique": [{"q": "L'éthanol appartient à la famille des :", "opts": ["Alcools", "Aldéhydes", "Cétones", "Acides carboxyliques"], "ans": "Alcools"}],
        "Gaz": [{"q": "La loi de Boyle-Mariotte s'énonce :", "opts": ["PV = constante", "V/T = constante", "P/T = constante", "n/V = constante"], "ans": "PV = constante"}],
        "Solutions": [{"q": "La molarité s'exprime en :", "opts": ["mol/L", "g/L", "mol/kg", "L/mol"], "ans": "mol/L"}],
        "Tableau Périodique": [{"q": "Les gaz rares se trouvent dans la colonne :", "opts": ["18", "1", "17", "2"], "ans": "18"}],
        "Thermodynamique": [{"q": "Une réaction endothermique :", "opts": ["Absorbe de la chaleur", "Libère de l'énergie", "Est toujours rapide", "Refroidit le milieu"], "ans": "Absorbe de la chaleur"}],
        "Liaisons": [{"q": "La liaison dans NaCl est :", "opts": ["Ionique", "Covalente", "Métallique", "Hydrogène"], "ans": "Ionique"}],
        "Cinétique": [{"q": "Un catalyseur :", "opts": ["Abaisse l'énergie d'activation", "Consomme les réactifs", "Arrête la réaction", "Change le pH"], "ans": "Abaisse l'énergie d'activation"}]
    },
    "Physique": {
        "Optique": [{"q": "L'indice de réfraction du vide est :", "opts": ["1,0", "0", "1,33", "1,5"], "ans": "1,0"}],
        "Mécanique": [{"q": "L'accélération de la pesanteur $g$ vaut environ :", "opts": ["9,81 $m/s^2$", "10 $km/h$", "0", "1,6 $m/s^2$"], "ans": "9,81 $m/s^2$"}],
        "Électricité": [{"q": "La puissance s'exprime par la relation :", "opts": ["$P = U \\cdot I$", "$P = U/I$", "$P = R \\cdot I$", "$P = m \\cdot g$"], "ans": "$P = U \\cdot I$"}],
        "Ondes": [{"q": "La fréquence est l'inverse de :", "opts": ["La période", "L'amplitude", "La longueur d'onde", "La célérité"], "ans": "La période"}],
        "Fluides": [{"q": "La pression s'exprime en :", "opts": ["Pascal", "Joule", "Newton", "Watt"], "ans": "Pascal"}],
        "Radioactivité": [{"q": "Une particule Alpha est un noyau de :", "opts": ["Hélium", "Hydrogène", "Carbone", "Plomb"], "ans": "Hélium"}],
        "Énergie": [{"q": "L'énergie potentielle de pesanteur est :", "opts": ["$mgh$", "$\\frac{1}{2}mv^2$", "$UI$", "$RI^2$"], "ans": "$mgh$"}],
        "Thermique": [{"q": "Le zéro absolu correspond à :", "opts": ["-273,15 °C", "0 °C", "100 °C", "-100 °C"], "ans": "-273,15 °C"}],
        "Vitesse": [{"q": "108 km/h correspond à :", "opts": ["30 m/s", "10 m/s", "108 m/s", "300 m/s"], "ans": "30 m/s"}],
        "Magnétisme": [{"q": "L'unité du champ magnétique est le :", "opts": ["Tesla", "Weber", "Volt", "Ohm"], "ans": "Tesla"}]
    },
    "Mathématiques": {
        "Dérivées": [{"q": "La dérivée de $\\sin(x)$ est :", "opts": ["$\\cos(x)$", "$-\\cos(x)$", "$\\sin(x)$", "0"], "ans": "$\\cos(x)$"}],
        "Intégrales": [{"q": "L'intégrale de $1/x$ est :", "opts": ["$\\ln|x| + C$", "$x^2$", "$e^x$", "$-1/x^2$"], "ans": "$\\ln|x| + C$"}],
        "Trigonométrie": [{"q": "$\\sin^2(x) + \\cos^2(x) = $", "opts": ["1", "0", "$\\tan(x)$", "$-1$"], "ans": "1"}],
        "Vecteurs": [{"q": "Si due vecteurs sont perpendiculaires, leur produit scalaire est :", "opts": ["0", "1", "-1", "Infini"], "ans": "0"}],
        "Logarithmes": [{"q": "$\\ln(a \\cdot b) = $", "opts": ["$\\ln(a) + \\ln(b)$", "$\\ln(a) \\cdot \\ln(b)$", "$a+b$", "$e^{a+b}$"], "ans": "$\\ln(a) + \\ln(b)$"}],
        "Probabilités": [{"q": "La probabilité d'un événement certain est :", "opts": ["1", "0", "0,5", "100"], "ans": "1"}],
        "Géométrie": [{"q": "L'aire d'un disque de rayon $R$ est :", "opts": ["$\\pi R^2$", "$2\\pi R$", "$4\\pi R^2$", "$\\pi R$"], "ans": "$\\pi R^2$"}],
        "Algèbre": [{"q": "La solution de $2x - 4 = 0$ est :", "opts": ["2", "-2", "4", "0"], "ans": "2"}],
        "Suites": [{"q": "Une suite où l'on ajoute toujours le même nombre est :", "opts": ["Arithmétique", "Géométrique", "Harmonique", "Constante"], "ans": "Arithmétique"}],
        "Limites": [{"q": "La limite de $1/x$ quand $x \\to \\infty$ est :", "opts": ["0", "1", "$\\infty$", "$-1$"], "ans": "0"}]
    }
}

# --- LOGICA DI NAVIGAZIONE ---

if 'state' not in st.session_state:
    st.session_state.state = "menu"
    st.session_state.score = 0.0
    st.session_state.questions = []
    st.session_state.current_idx = 0
    st.session_state.answered = False

def start_balanced_quiz(subject):
    # 1. Recupera tutti i sotto-argomenti per quella materia
    sub_topics = list(DB_ARES[subject].keys())
    # 2. Mescola i sotto-argomenti
    random.shuffle(sub_topics)
    
    selected_questions = []
    # 3. Prendi una domanda da ogni sotto-argomento (fino a 10)
    for topic in sub_topics[:10]:
        q_pool = DB_ARES[subject][topic]
        selected_q = random.choice(q_pool).copy()
        selected_q['topic'] = topic
        random.shuffle(selected_q['opts'])
        selected_questions.append(selected_q)
    
    st.session_state.questions = selected_questions
    st.session_state.state = "quiz"
    st.session_state.current_idx = 0
    st.session_state.score = 0.0
    st.session_state.answered = False

def submit_answer(choice, correct):
    st.session_state.answered = True
    if choice == correct:
        st.session_state.score += 1.0
    else:
        st.session_state.score -= (1/3)

# --- INTERFACCIA ---

st.title("🩺 Quizzeo ARES - Simulatore Bilanciato")
st.write("Ogni quiz contiene 10 argomenti diversi. Punteggio: +1 Corretta, -1/3 Errata.")
st.divider()

if st.session_state.state == "menu":
    cols = st.columns(2)
    with cols[0]:
        st.button("🧬 Biologia", use_container_width=True, on_click=start_balanced_quiz, args=("Biologie",))
        st.button("🧪 Chimica", use_container_width=True, on_click=start_balanced_quiz, args=("Chimie",))
    with cols[1]:
        st.button("📐 Matematica", use_container_width=True, on_click=start_balanced_quiz, args=("Mathématiques",))
        st.button("⚡ Fisica", use_container_width=True, on_click=start_balanced_quiz, args=("Physique",))

elif st.session_state.state == "quiz":
    q = st.session_state.questions[st.session_state.current_idx]
    
    st.caption(f"Argomento: **{q['topic']}** | Domanda {st.session_state.current_idx + 1} di 10")
    st.progress((st.session_state.current_idx + 1) / 10)
    
    st.subheader(q['q'])
    
    for opt in q['opts']:
        st.button(opt, use_container_width=True, key=f"q{st.session_state.current_idx}_{opt}",
                  disabled=st.session_state.answered, on_click=submit_answer, args=(opt, q['ans']))
    
    if st.session_state.answered:
        if st.button("Prossima Domanda ➡️", type="primary"):
            if st.session_state.current_idx < 9:
                st.session_state.current_idx += 1
                st.session_state.answered = False
                st.rerun()
            else:
                st.session_state.state = "results"
                st.rerun()

elif st.session_state.state == "results":
    st.balloons()
    st.header("🏁 Risultato Finale")
    st.metric("Punteggio ARES", f"{round(st.session_state.score, 2)} / 10")
    if st.button("Torna al Menu"):
        st.session_state.state = "menu"
        st.rerun()
