import streamlit as st
import random

# Configurazione Pagina
st.set_page_config(page_title="Quizzeo ARES", page_icon="🩺", layout="centered")

# --- DATABASE ESTESO (Esempi reali ARES) ---
# Nota: Ho inserito una base di domande. Puoi espandere ogni lista fino a 100+.
DB = {
    "Biologie": [
        {"q": "Quelle est la phase de la mitose où l'enveloppe nucléaire se reforme ?", "opts": ["Prophase", "Métaphase", "Anaphase", "Télophase"], "ans": "Télophase", "cat": "Cytologie"},
        {"q": "Le crossing-over se produit durant :", "opts": ["La prophase I", "La métaphase II", "L'interphase", "La mitose"], "ans": "La prophase I", "cat": "Génétique"},
        {"q": "L'hormone qui fait baisser la glycémie est :", "opts": ["Le glucagon", "L'insuline", "L'adrénaline", "Le cortisol"], "ans": "L'insuline", "cat": "Physiologie"},
        {"q": "Où se déroule la glycolyse ?", "opts": ["Dans la mitochondrie", "Dans le cytosol", "Dans le noyau", "Sur les ribosomes"], "ans": "Dans le cytosol", "cat": "Métabolisme"},
        {"q": "Quel organite contient des enzymes digestives ?", "opts": ["Le lysosome", "Le centrosome", "L'appareil de Golgi", "Le nucléole"], "ans": "Le lysosome", "cat": "Cytologie"},
        {"q": "La transcription de l'ADN produit :", "opts": ["Un polypeptide", "Un ARNm", "Un lipide", "Un deuxième brin d'ADN"], "ans": "Un ARNm", "cat": "Génétique"},
        {"q": "Les cellules procaryotes ne possèdent pas de :", "opts": ["Membrane plasmique", "Ribosomes", "Noyau", "ADN"], "ans": "Noyau", "cat": "Cytologie"},
        {"q": "Quelle base azotée est absente de l'ARN ?", "opts": ["Uracile", "Adénine", "Thymine", "Guanine"], "ans": "Thymine", "cat": "Biochimie"},
        {"q": "Le cycle de Krebs a lieu dans :", "opts": ["La matrice mitochondriale", "Le cytoplasme", "La paroi", "Le stroma"], "ans": "La matrice mitochondriale", "cat": "Métabolisme"},
        {"q": "Combien de chromosomes possède une cellule somatique humaine ?", "opts": ["23", "46", "92", "44"], "ans": "46", "cat": "Génétique"},
        {"q": "La synthèse des protéines a lieu au niveau :", "opts": ["Des lysosomes", "Des ribosomes", "Des vacuoles", "Des centrioles"], "ans": "Des ribosomes", "cat": "Cytologie"},
        {"q": "L'ATP est produit majoritairement par :", "opts": ["L'ATP synthase", "L'amylase", "L'hélicase", "La polymérase"], "ans": "L'ATP synthase", "cat": "Biochimie"}
    ],
    "Chimie": [
        {"q": "Quel est le pH d'une solution de HCl à $0,001$ mol/L ?", "opts": ["1", "2", "3", "7"], "ans": "3", "cat": "Acide/Base"},
        {"q": "L'oxydation correspond à :", "opts": ["Un gain d'électrons", "Une perte d'électrons", "Un gain de protons", "Une perte de neutrons"], "ans": "Une perte d'électrons", "cat": "Redox"},
        {"q": "La masse molaire de l'eau ($H_2O$) est environ :", "opts": ["16 g/mol", "18 g/mol", "10 g/mol", "20 g/mol"], "ans": "18 g/mol", "cat": "Stoechiométrie"},
        {"q": "Un alcane à 3 carbones s'appelle :", "opts": ["Méthane", "Éthane", "Propane", "Butane"], "ans": "Propane", "cat": "Organique"},
        {"q": "Dans $PV = nRT$, R est :", "opts": ["La constante des gaz parfaits", "Le rayon atomique", "La résistance", "Le rendement"], "ans": "La constante des gaz parfaits", "cat": "Gaz"},
        {"q": "Une solution basique a un pH :", "opts": ["= 7", "< 7", "> 7", "= 0"], "ans": "> 7", "cat": "Acide/Base"},
        {"q": "Le nombre d'Avogadro est environ :", "opts": ["$6,02 \\cdot 10^{23}$", "$1,6 \\cdot 10^{-19}$", "$9,81$", "$3 \\cdot 10^8$"], "ans": "$6,02 \\cdot 10^{23}$", "cat": "Stoechiométrie"},
        {"q": "Quel est l'élément le plus électronégatif ?", "opts": ["Oxygène", "Fluor", "Carbone", "Azote"], "ans": "Fluor", "cat": "Périodique"},
        {"q": "Une réaction exothermique :", "opts": ["Libère de la chaleur", "Absorbe de la chaleur", "Ne change rien", "Glace le milieu"], "ans": "Libère de la chaleur", "cat": "Thermodynamique"},
        {"q": "L'unité de la concentration molaire est :", "opts": ["g/L", "mol/L", "mol/kg", "L/mol"], "ans": "mol/L", "cat": "Solutions"}
    ],
    "Physique": [
        {"q": "L'unité de la force dans le SI est :", "opts": ["Pascal", "Joule", "Newton", "Watt"], "ans": "Newton", "cat": "Mécanique"},
        {"q": "La vitesse de la lumière dans le vide è :", "opts": ["$300.000$ km/s", "$300$ m/s", "$3 \cdot 10^5$ m/s", "$1.000$ km/h"], "ans": "$300.000$ km/s", "cat": "Optique"},
        {"q": "La loi d'Ohm s'écrit :", "opts": ["$P = UI$", "$U = RI$", "$F = ma$", "$E = mc^2$"], "ans": "$U = RI$", "cat": "Électricité"},
        {"q": "Un objet de 10kg sur Terre pèse environ :", "opts": ["10 N", "100 N", "1 N", "980 N"], "ans": "100 N", "cat": "Mécanique"},
        {"q": "La réfraction est le changement de :", "opts": ["Direction de la lumière", "Couleur", "Vitesse du son", "Masse"], "ans": "Direction de la lumière", "cat": "Optique"},
        {"q": "Une lentille divergente :", "opts": ["Écarte les rayons", "Rapproche les rayons", "N'a aucun effet", "Brûle le papier"], "ans": "Écarte les rayons", "cat": "Optique"},
        {"q": "L'énergie cinétique se calcule par :", "opts": ["$mgh$", "$\\frac{1}{2}mv^2$", "$ma$", "$Fd$"], "ans": "$\\frac{1}{2}mv^2$", "cat": "Mécanique"},
        {"q": "La période T est liée alla fréquence f par :", "opts": ["$T = 1/f$", "$T = f^2$", "$T = 2f$", "$T = f$"], "ans": "$T = 1/f$", "cat": "Ondes"},
        {"q": "La pression atmosphérique normale est d'environ :", "opts": ["$1$ bar", "$10$ bars", "$100$ Pa", "$0,1$ atm"], "ans": "$1$ bar", "cat": "Fluides"},
        {"q": "Le son se propage plus vite dans :", "opts": ["L'air", "Le vide", "L'acier", "L'eau"], "ans": "L'acier", "cat": "Ondes"}
    ],
    "Mathématiques": [
        {"q": "La dérivée de $x^2$ est :", "opts": ["$x$", "$2x$", "$2$", "$x/2$"], "ans": "$2x$", "cat": "Calcul"},
        {"q": "$\\cos(0)$ est égal à :", "opts": ["0", "1", "$\\pi$", "0,5"], "ans": "1", "cat": "Trigo"},
        {"q": "Un triangle avec deux côtés égaux è :", "opts": ["Équilatéral", "Isocèle", "Scalène", "Rectangle"], "ans": "Isocèle", "cat": "Géométrie"},
        {"q": "$\\ln(e)$ vaut :", "opts": ["0", "1", "$e$", "10"], "ans": "1", "cat": "Algèbre"},
        {"q": "Le volume d'un cube de côté 3 est :", "opts": ["9", "27", "12", "18"], "ans": "27", "cat": "Géométrie"},
        {"q": "Si $x + 5 = 12$, alors $x$ vaut :", "opts": ["5", "7", "17", "6"], "ans": "7", "cat": "Algèbre"},
        {"q": "La somme des angles d'un triangle est :", "opts": ["90°", "180°", "360°", "270°"], "ans": "180°", "cat": "Géométrie"},
        {"q": "$\\sqrt{144}$ est :", "opts": ["10", "11", "12", "14"], "ans": "12", "cat": "Algèbre"},
        {"q": "Un angle droit mesure :", "opts": ["45°", "90°", "180°", "0°"], "ans": "90°", "cat": "Géométrie"},
        {"q": "La probabilité de pile sur un lancer de pièce est :", "opts": ["0", "1", "0,5", "0,25"], "ans": "0,5", "cat": "Probabilités"}
    ]
}

# --- LOGICA DI STATO ---

if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = "selection" # selection, playing, finished
    st.session_state.score = 0.0
    st.session_state.questions = []
    st.session_state.current_idx = 0
    st.session_state.answered = False

def start_quiz(subject):
    # Pesca 10 domande casuali dal database della materia
    pool = DB[subject]
    # Se ci sono meno di 10 domande, le prende tutte, altrimenti 10 a caso
    n = min(len(pool), 10)
    selected = random.sample(pool, n)
    
    # Mischia le opzioni per ogni domanda
    for q in selected:
        random.shuffle(q['opts'])
        
    st.session_state.questions = selected
    st.session_state.quiz_state = "playing"
    st.session_state.current_idx = 0
    st.session_state.score = 0.0
    st.session_state.answered = False

def handle_answer(choice, correct):
    st.session_state.answered = True
    if choice == correct:
        st.session_state.score += 1.0
        st.session_state.last_result = "correct"
    else:
        # Punteggio ARES: -1/3 per errore
        st.session_state.score -= (1/3)
        st.session_state.last_result = "wrong"

def next_question():
    st.session_state.current_idx += 1
    st.session_state.answered = False
    if st.session_state.current_idx >= len(st.session_state.questions):
        st.session_state.quiz_state = "finished"

# --- INTERFACCIA UTENTE ---

st.title("🩺 Quizzeo ARES - Concours MD")
st.markdown("---")

# 1. SELEZIONE MATERIA
if st.session_state.quiz_state == "selection":
    st.subheader("Sélectionnez une matière pour commencer (10 questions)")
    cols = st.columns(2)
    subjects = list(DB.keys())
    for i, sub in enumerate(subjects):
        with cols[i % 2]:
            if st.button(sub, use_container_width=True, key=f"select_{sub}"):
                start_quiz(sub)
                st.rerun()

# 2. QUIZ IN CORSO
elif st.session_state.quiz_state == "playing":
    q_list = st.session_state.questions
    idx = st.session_state.current_idx
    q = q_list[idx]

    # Progresso
    st.sidebar.metric("Score", f"{st.session_state.score:.2f}")
    st.sidebar.progress((idx + 1) / len(q_list))
    st.sidebar.write(f"Question {idx+1} sur {len(q_list)}")

    st.markdown(f"**Thème : {q['cat']}**")
    st.subheader(q['q'])

    # Bottoni Risposta
    for opt in q['opts']:
        # Se ha già risposto, disabilita i bottoni
        st.button(
            opt, 
            key=f"opt_{idx}_{opt}", 
            use_container_width=True,
            disabled=st.session_state.answered,
            on_click=handle_answer,
            args=(opt, q['ans'])
        )

    # Feedback dopo la risposta
    if st.session_state.answered:
        if st.session_state.last_result == "correct":
            st.success("✨ Correct ! (+1)")
        else:
            st.error(f"❌ Erreur. La réponse était : {q['ans']} (-1/3)")
        
        st.button("Question Suivante ➡️", on_click=next_question, type="primary")

# 3. FINE QUIZ
elif st.session_state.quiz_state == "finished":
    st.balloons()
    st.header("🏁 Quiz Terminé !")
    
    final_score = st.session_state.score
    st.metric("Punteggio Finale", f"{final_score:.2f} / 10")
    
    if final_score >= 6:
        st.success("Excellent travail ! Vous êtes prêt pour le concours.")
    else:
        st.warning("Continuez à réviser, le seuil de réussite est proche.")

    if st.button("🔄 Retour au menu principal"):
        st.session_state.quiz_state = "selection"
        st.rerun()
