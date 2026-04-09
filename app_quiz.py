import streamlit as st
import random

# Configurazione Pagina
st.set_page_config(page_title="Quizzeo - Matteo Sapia", page_icon="⚖️", layout="centered")

# --- DATABASE ELITE (Basato su ARES e le tue immagini) ---
DB_ARES = {
    "Biologie": {
        "Cytologie": [{"q": "L'organite responsable de la modification et de l'emballage des protéines est :", "opts": ["L'appareil de Golgi", "Le réticulum endoplasmique lisse", "Le lysosome", "Le nucléole"], "ans": "L'appareil de Golgi"}],
        "Génétique": [{"q": "Une cellule humaine en fin de prophase de mitose contient :", "opts": ["46 chromosomes à 2 chromatides", "46 chromosomes à 1 chromatide", "23 chromosomes à 2 chromatides", "92 chromosomes à 2 chromatides"], "ans": "46 chromosomes à 2 chromatides"}],
        "Métabolisme": [{"q": "La respiration cellulaire produit du CO2 pendant :", "opts": ["Le cycle de Krebs", "La glycolyse", "La chaîne respiratoire", "La phase S"], "ans": "Le cycle de Krebs"}],
        "Physiologie": [{"q": "Quelle hormone est produite par les cellules alpha du pancréas ?", "opts": ["Le glucagon", "L'insuline", "L'adrénaline", "La thyroxine"], "ans": "Le glucagon"}],
        "Biochimie": [{"q": "L'adénine s'apparie toujours avec la thymine via :", "opts": ["2 liaisons hydrogène", "3 liaisons hydrogène", "1 liaison covalente", "Une liaison ionique"], "ans": "2 liaisons hydrogène"}],
        "Histologie": [{"q": "Le tissu qui assure la conduction des messages est le :", "opts": ["Tissu nerveux", "Tissu conjonctif", "Tissu épithélial", "Tissu musculaire"], "ans": "Tissu nerveux"}],
        "Immunologie": [{"q": "Quel type de cellule produit les anticorps ?", "opts": ["Plasmocyte", "Lymphocyte T8", "Macrophage", "Hématie"], "ans": "Plasmocyte"}],
        "Evolution": [{"q": "L'unité de base de l'évolution est :", "opts": ["La population", "L'individu", "L'écosystème", "La biosphère"], "ans": "La population"}],
        "Botanique": [{"q": "Le processus de transformation de l'énergie lumineuse en énergie chimique est :", "opts": ["La photosynthèse", "La transpiration", "La respiration", "La mitose"], "ans": "La photosynthèse"}],
        "Microbiologie": [{"q": "Un virus est caractérisé par :", "opts": ["L'absence de métabolisme propre", "Une structure cellulaire complète", "Une reproduction par mitose", "La présence de mitochondries"], "ans": "L'absence de métabolisme propre"}]
    },
    "Chimie": {
        "Masse Volumique": [{"q": "Un récipient de 20g contient 50 cm³ d'un liquide. La masse totale est de 60g. Masse volumique ?", "opts": ["0,8 g/cm³", "1,2 g/cm³", "1,0 g/cm³", "0,5 g/cm³"], "ans": "0,8 g/cm³"}],
        "Acide/Base": [{"q": "Quel est le pH d'une solution de $HCl$ à $10^{-2}$ mol/L ?", "opts": ["2", "12", "7", "1"], "ans": "2"}],
        "Redox": [{"q": "L'oxydant est une espèce qui :", "opts": ["Capte des électrons", "Donne des électrons", "Donne des protons", "Ne réagit pas"], "ans": "Capte des électrons"}],
        "Stoechiométrie": [{"q": "Masse molaire de $CaCO_3$ ? (Ca=40, C=12, O=16)", "opts": ["100 g/mol", "68 g/mol", "84 g/mol", "120 g/mol"], "ans": "100 g/mol"}],
        "Organique": [{"q": "Le groupement fonctionnel des alcools est :", "opts": ["-OH", "-CHO", "-COOH", "-NH2"], "ans": "-OH"}],
        "Gaz": [{"q": "À 0°C et 1 atm, le volume molaire d'un gaz parfait est :", "opts": ["22,4 L", "24,0 L", "11,2 L", "1,0 L"], "ans": "22,4 L"}],
        "Liaisons": [{"q": "Quelle molécule possède une liaison triple ?", "opts": ["$N_2$", "$O_2$", "$H_2$", "$Cl_2$"], "ans": "$N_2$"}],
        "Tableau Périodique": [{"q": "L'électronégativité augmente généralement :", "opts": ["Vers le haut et la droite", "Vers le bas et la gauche", "Uniquement vers le bas", "Elle est constante"], "ans": "Vers le haut et la droite"}],
        "Solutions": [{"q": "On dilue 10 fois une solution 1M. La nouvelle concentration est :", "opts": ["0,1 M", "10 M", "0,01 M", "0,5 M"], "ans": "0,1 M"}],
        "Thermodynamique": [{"q": "Une réaction qui libère de la chaleur est dite :", "opts": ["Exothermique", "Endothermique", "Isotherme", "Adiabatique"], "ans": "Exothermique"}]
    },
    "Physique": {
        "Optique": [{"q": "Une lentille convergente a une vergence de 4 dioptries. Sa focale est :", "opts": ["25 cm", "4 cm", "40 cm", "10 cm"], "ans": "25 cm"}],
        "Mécanique": [{"q": "Énergie cinétique d'un corps de 4kg à 3 m/s ?", "opts": ["18 J", "12 J", "36 J", "6 J"], "ans": "18 J"}],
        "Électricité": [{"q": "Puissance dissipée par une résistance de 10 $\Omega$ traversée par 2A ?", "opts": ["40 W", "20 W", "100 W", "5 W"], "ans": "40 W"}],
        "Hydrostatique": [{"q": "Poussée d'Archimède sur un objet de 2L totalement immergé dans l'eau ?", "opts": ["20 N", "2 N", "200 N", "0,2 N"], "ans": "20 N"}],
        "Ondes": [{"q": "La vitesse du son dans l'air est environ :", "opts": ["340 m/s", "300.000 km/s", "1500 m/s", "100 m/s"], "ans": "340 m/s"}],
        "Cinématique": [{"q": "Distance parcourue en 5s à une vitesse constante de 12 m/s ?", "opts": ["60 m", "17 m", "2,4 m", "120 m"], "ans": "60 m"}],
        "Radioactivité": [{"q": "Après 2 demi-vies, il reste :", "opts": ["25% de l'échantillon", "50%", "12,5%", "0%"], "ans": "25% de l'échantillon"}],
        "Chaleur": [{"q": "La température de 0 K correspond à :", "opts": ["-273,15 °C", "0 °C", "100 °C", "-459 °C"], "ans": "-273,15 °C"}],
        "Magnétisme": [{"q": "L'unité du flux magnétique est le :", "opts": ["Weber", "Tesla", "Ampère", "Henry"], "ans": "Weber"}],
        "Forces": [{"q": "Poids d'un objet de 500g sur Terre ($g=10$) ?", "opts": ["5 N", "50 N", "500 N", "0,5 N"], "ans": "5 N"}]
    },
    "Mathématiques": {
        "Vecteurs": [{"q": "Dans un carré ABCD de côté 4, $\\vec{AB} \\cdot \\vec{AC} = $", "opts": ["16", "0", "32", "8"], "ans": "16"}],
        "Dérivées": [{"q": "Dérivée de $f(x) = 5x^3 - 2x$ ?", "opts": ["$15x^2 - 2$", "$5x^2 - 2$", "$15x^2$", "$10x - 2$"], "ans": "$15x^2 - 2$"}],
        "Trigonométrie": [{"q": "$\\cos(60^\\circ)$ vaut :", "opts": ["1/2", "$\\sqrt{3}/2$", "$\\sqrt{2}/2$", "1"], "ans": "1/2"}],
        "Logarithmes": [{"q": "$\\ln(e^3)$ est égal à :", "opts": ["3", "$e$", "1", "0"], "ans": "3"}],
        "Probabilités": [{"q": "Probabilité d'obtenir un chiffre pair avec un dé à 6 faces ?", "opts": ["1/2", "1/3", "1/6", "2/3"], "ans": "1/2"}],
        "Géométrie": [{"q": "Volume d'un cylindre de rayon R e hauteur H ?", "opts": ["$\\pi R^2 H$", "$2\\pi R H$", "$\\frac{1}{3}\\pi R^2 H$", "$\\pi R H^2$"], "ans": "$\\pi R^2 H"}],
        "Algèbre": [{"q": "Si $3x + 9 = 0$, allora $x$ è :", "opts": ["-3", "3", "0", "1"], "ans": "-3"}],
        "Suites": [{"q": "Somme des angles internes d'un hexagone ?", "opts": ["720°", "540°", "360°", "1080°"], "ans": "720°"}],
        "Limites": [{"q": "Limite de $e^{-x}$ quand $x \\to +\\infty$ ?", "opts": ["0", "$+\\infty$", "1", "$-1$"], "ans": "0"}],
        "Analyse": [{"q": "La fonction $f(x) = x^2$ est :", "opts": ["Paire", "Impaire", "Périodique", "Négative"], "ans": "Paire"}]
    }
}

# --- LOGICA DI NAVIGAZIONE ---

if 'state' not in st.session_state:
    st.session_state.state = "menu"
    st.session_state.score = 0.0
    st.session_state.current_idx = 0
    st.session_state.questions = []
    st.session_state.answered = False
    st.session_state.feedback = None

def start_quiz(subject):
    topics = list(DB_ARES[subject].keys())
    random.shuffle(topics)
    selected_qs = []
    for t in topics[:10]:
        q_data = random.choice(DB_ARES[subject][t]).copy()
        q_data['topic'] = t
        random.shuffle(q_data['opts'])
        selected_qs.append(q_data)
    st.session_state.questions = selected_qs
    st.session_state.state = "quiz"
    st.session_state.current_idx = 0
    st.session_state.score = 0.0
    st.session_state.answered = False
    st.session_state.feedback = None

def submit(choice, correct):
    st.session_state.answered = True
    if choice == correct:
        st.session_state.score += 1.0
        st.session_state.feedback = ("success", "✅ Bien joué !")
    else:
        st.session_state.score -= (1/3)
        st.session_state.feedback = ("error", f"❌ Faux. La réponse était : **{correct}**")

# --- UI ---

st.title("Quizzeo - Prodotto da Matteo Sapia")
st.markdown("---")

if st.session_state.state == "menu":
    st.subheader("Sélectionnez votre épreuve (10 questions uniques)")
    cols = st.columns(2)
    with cols[0]:
        st.button("🧬 Biologie", use_container_width=True, on_click=start_quiz, args=("Biologie",))
        st.button("🧪 Chimie", use_container_width=True, on_click=start_quiz, args=("Chimie",))
    with cols[1]:
        st.button("📐 Mathématiques", use_container_width=True, on_click=start_quiz, args=("Mathématiques",))
        st.button("⚡ Physique", use_container_width=True, on_click=start_quiz, args=("Physique",))

elif st.session_state.state == "quiz":
    q = st.session_state.questions[st.session_state.current_idx]
    st.caption(f"Thème: {q['topic']} | Question {st.session_state.current_idx + 1}/10")
    st.progress((st.session_state.current_idx + 1) / 10)
    
    st.subheader(q['q'])
    
    for opt in q['opts']:
        st.button(opt, use_container_width=True, key=f"q{st.session_state.current_idx}_{opt}",
                  disabled=st.session_state.answered, on_click=submit, args=(opt, q['ans']))
    
    if st.session_state.answered:
        tipo, msg = st.session_state.feedback
        st.success(msg) if tipo == "success" else st.error(msg)
        
        if st.button("Suivant ➡️", type="primary"):
            if st.session_state.current_idx < 9:
                st.session_state.current_idx += 1
                st.session_state.answered = False
                st.rerun()
            else:
                st.session_state.state = "results"
                st.rerun()

elif st.session_state.state == "results":
    st.balloons()
    st.header("🏁 Résultat Final")
    st.metric("Score ARES", f"{round(st.session_state.score, 2)} / 10")
    if st.button("Retour au Menu"):
        st.session_state.state = "menu"
        st.rerun()
