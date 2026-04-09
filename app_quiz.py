import streamlit as st
import random

# Configurazione Pagina
st.set_page_config(page_title="Quizzeo ARES Elite", page_icon="⚖️", layout="centered")

# --- DATABASE AVANZATO (Basato su ARES 2017-2022) ---
DB_ARES = {
    "Biologie": {
        "Cytologie": [
            {"q": "Quelle est la séquence correcte de la synthèse et de l'exportation d'une protéine ?", "opts": ["Nucléole -> RER -> Appareil de Golgi -> Vésicule de sécrétion", "Noyau -> Ribosome libre -> Lysosome -> Membrane", "RER -> Appareil de Golgi -> Mitochondrie -> Cytosol", "Noyau -> Peroxysome -> Réticulum -> Appareil de Golgi"], "ans": "Nucléole -> RER -> Appareil de Golgi -> Vésicule de sécrétion"},
            {"q": "Quel organite possède une double membrane et des ribosomes 70S ?", "opts": ["La mitochondrie", "L'appareil de Golgi", "Le réticulum endoplasmique lisse", "Le lysosome"], "ans": "La mitochondrie"}
        ],
        "Génétique Moleculaire": [
            {"q": "Si un brin d'ADN a la séquence 5'-ATGCG-3', quel est l'ARNm transcrit ?", "opts": ["5'-AUGCG-3'", "5'-UACGC-3'", "3'-UACGC-5'", "5'-TACGC-3'"], "ans": "3'-UACGC-5'"},
            {"q": "L'expérience di Hershey et Chase a prouvé che :", "opts": ["L'ADN est le support de l'hérédité", "Les protéines portent le code génétique", "L'ARN est monocaténaire", "La réplication est semi-conservative"], "ans": "L'ADN est le support de l'hérédité"}
        ],
        "Biochimie": [
            {"q": "Combien de liaisons hydrogène lient une paire de bases G-C ?", "opts": ["3", "2", "1", "4"], "ans": "3"},
            {"q": "L'hydrolyse complète de l'amidon produit du :", "opts": ["Glucose", "Fructose", "Galactose", "Maltose"], "ans": "Glucose"}
        ],
        "Physiologie Cardiaque": [
            {"q": "Le noeud sinusal est situé dans :", "opts": ["L'oreillette droite", "L'oreillette gauche", "Le ventricule droit", "Le septum"], "ans": "L'oreillette droite"}
        ],
        "Metabolisme": [
            {"q": "Quel est le bilan net en ATP d'une molécule de glucose subissant uniquement la glycolyse ?", "opts": ["2 ATP", "4 ATP", "36 ATP", "0 ATP"], "ans": "2 ATP"}
        ],
        "Hérédité Mendélienne": [
            {"q": "Croisement de deux hétérozygotes (Aa x Aa). Probabilité d'avoir un descendant homozygote récessif ?", "opts": ["25%", "50%", "75%", "100%"], "ans": "25%"}
        ],
        "Histologie": [{"q": "Le tissu conjonctif se caractérise par :", "opts": ["Une matrice extracellulaire abondante", "Des cellules jointives", "L'absence de vaisseaux", "La capacité de contraction"], "ans": "Une matrice extracellulaire abondante"}],
        "Immunologie": [{"q": "Les anticorps sont produits par :", "opts": ["Les plasmocytes", "Les lymphocytes T4", "Les macrophages", "Les globules rouges"], "ans": "Les plasmocytes"}],
        "Microbiologie": [{"q": "Les antibiotiques agissent généralement sur :", "opts": ["La paroi bactérienne", "La capside virale", "Le noyau des eucaryotes", "Les mitochondries"], "ans": "La paroi bactérienne"}],
        "Cycle Cellulaire": [{"q": "Pendant quelle phase les chromosomes sont-ils alignés sur la plaque équatoriale ?", "opts": ["Métaphase", "Prophase", "Anaphase", "Télophase"], "ans": "Métaphase"}]
    },
    "Chimie": {
        "Solutions": [
            {"q": "Masse de NaCl nécessaire pour préparer 500 mL d'une solution à 0,2 mol/L ? (M=58,5 g/mol)", "opts": ["5,85 g", "11,7 g", "2,92 g", "58,5 g"], "ans": "5,85 g"}
        ],
        "pH": [
            {"q": "pH d'une solution de $Ba(OH)_2$ à $5 \cdot 10^{-4}$ mol/L ?", "opts": ["11", "3", "10", "4"], "ans": "11"}
        ],
        "Redox": [
            {"q": "Dans $Cr_2O_7^{2-}$, le nombre d'oxydation du chrome est :", "opts": ["+6", "+7", "+3", "+12"], "ans": "+6"}
        ],
        "Organique": [
            {"q": "L'isomérie de fonction existe entre :", "opts": ["Éthanol et éther diméthylique", "But-1-ène et but-2-ène", "Propan-1-ol et propan-2-ol", "Pentane et isopentane"], "ans": "Éthanol et éther diméthylique"}
        ],
        "Thermodynamique": [{"q": "Une réaction spontanée est caractérisée par :", "opts": ["$\Delta G < 0$", "$\Delta G > 0$", "$\Delta H > 0$", "$\Delta S = 0$"], "ans": "$\Delta G < 0$"}],
        "Equilibre": [{"q": "Si on augmente la pression d'un système gazeux, l'équilibre se déplace vers :", "opts": ["Le côté avec moins de moles de gaz", "Le côté avec plus de moles de gaz", "La droite systématiquement", "Il ne bouge pas"], "ans": "Le côté avec moins de moles de gaz"}],
        "Gaz Parfaits": [{"q": "À pression constante, si la température double (en K), le volume :", "opts": ["Double", "Est divisé par 2", "Reste constant", "Quadruple"], "ans": "Double"}],
        "Orbitales": [{"q": "Configuration électronique du Carbone (Z=6) :", "opts": ["$1s^2 2s^2 2p^2$", "$1s^2 2s^2 2p^4$", "$1s^2 2s^2 2s^2$", "$1s^2 2s^4$"], "ans": "$1s^2 2s^2 2p^2$"}],
        "Liaisons": [{"q": "Laquelle de ces molécules est polaire ?", "opts": ["$NH_3$", "$CH_4$", "$CO_2$", "$O_2$"], "ans": "$NH_3$"}],
        "Cinétique": [{"q": "L'unité d'une constante de vitesse d'ordre 1 est :", "opts": ["$s^{-1}$", "$mol \cdot L^{-1} \cdot s^{-1}$", "$L \cdot mol^{-1} \cdot s^{-1}$", "$mol/L$"], "ans": "$s^{-1}$"}]
    },
    "Physique": {
        "Optique": [{"q": "Un objet est à 10 cm d'une lentille convergente (f = 5 cm). L'image est :", "opts": ["Réelle, renversée et de même taille", "Virtuelle et agrandie", "Réelle et plus petite", "À l'infini"], "ans": "Réelle, renversée et de même taille"}],
        "Mécanique": [{"q": "Travail d'une force de 10N sur 5m avec un angle de 60° ?", "opts": ["25 J", "50 J", "43,3 J", "0 J"], "ans": "25 J"}],
        "Électricité": [{"q": "Résistance totale de deux résistors de 6 $\Omega$ et 3 $\Omega$ en parallèle ?", "opts": ["2 $\Omega$", "9 $\Omega$", "4.5 $\Omega$", "1 $\Omega$"], "ans": "2 $\Omega$"}],
        "Hydrostatique": [{"q": "Différence de pression entre 0m et 20m de profondeur sous l'eau ? ($g=10, \rho=1000$)", "opts": ["200.000 Pa", "20.000 Pa", "2.000 Pa", "20 bar"], "ans": "200.000 Pa"}],
        "Cinématique": [{"q": "Un mobile passe de 0 à 100 km/h en 10s. Accélération moyenne ?", "opts": ["2,78 $m/s^2$", "10 $m/s^2$", "0,1 $m/s^2$", "27,8 $m/s^2$"], "ans": "2,78 $m/s^2$"}],
        "Ondes": [{"q": "Longueur d'onde d'un son de 440 Hz (vitesse = 340 m/s) ?", "opts": ["0,77 m", "1,29 m", "149 km", "1,5 m"], "ans": "0,77 m"}],
        "Radioactivité": [{"q": "Demi-vie = 10 min. Pourcentage restant après 30 min ?", "opts": ["12,5%", "25%", "33%", "50%"], "ans": "12,5%"}],
        "Chaleur": [{"q": "Énergie pour chauffer 1kg d'eau de 10°C à 20°C ? ($c = 4180 J/kg \cdot K$)", "opts": ["41.800 J", "4.180 J", "418.000 J", "10 J"], "ans": "41.800 J"}],
        "Magnétisme": [{"q": "Force d'un champ de 0,5T su un fil de 1m parcouru par 2A (perpendiculaire) ?", "opts": ["1 N", "0,5 N", "2 N", "4 N"], "ans": "1 N"}],
        "Energie": [{"q": "Puissance d'un moteur soulevant 100kg à 2m en 10s ? ($g=10$)", "opts": ["200 W", "2000 W", "20 W", "1000 W"], "ans": "200 W"}]
    },
    "Mathématiques": {
        "Analyse": [{"q": "Dérivée de $f(x) = \sin(2x)$ ?", "opts": ["$2\cos(2x)$", "$\cos(2x)$", "$-2\cos(2x)$", "$2\sin(x)$"], "ans": "$2\cos(2x)$"}],
        "Vecteurs": [{"q": "Produit scalaire de $\vec{u}(3, -1)$ et $\vec{v}(2, 4)$ ?", "opts": ["2", "10", "5", "-2"], "ans": "2"}],
        "Trigo": [{"q": "$\tan(x) = 1$ implique (sur $[0, \pi/2]$) :", "opts": ["$x = \pi/4$", "$x = \pi/6$", "$x = \pi/3$", "$x = 0$"], "ans": "$x = \pi/4$"}],
        "Log": [{"q": "$\log_{10}(1000)$ est égal à :", "opts": ["3", "10", "100", "2"], "ans": "3"}],
        "Suites": [{"q": "Raison d'une suite géométrique où $u_1=3$ et $u_3=12$ ($q>0$) ?", "opts": ["2", "4", "3", "9"], "ans": "2"}],
        "Proba": [{"q": "Probabilité de tirer 2 as consécutivement sans remise dans un jeu de 52 ?", "opts": ["1/221", "1/169", "4/52", "1/13"], "ans": "1/221"}],
        "Limites": [{"q": "Limite de $(x^2-1)/(x-1)$ quand $x \to 1$ ?", "opts": ["2", "1", "0", "Infini"], "ans": "2"}],
        "Géométrie": [{"q": "Surface d'une sphère de rayon R ?", "opts": ["$4\pi R^2$", "$\frac{4}{3}\pi R^3$", "$2\pi R$", "$\pi R^2$"], "ans": "$4\pi R^2$"}],
        "Integrale": [{"q": "Primitive de $e^{2x}$ ?", "opts": ["$\frac{1}{2}e^{2x} + C$", "$2e^{2x} + C$", "$e^{2x} + C$", "$e^{x^2} + C$"], "ans": "$\frac{1}{2}e^{2x} + C$"}],
        "Complexes": [{"q": "Module de $z = 3 + 4i$ ?", "opts": ["5", "7", "25", "1"], "ans": "5"}]
    }
}

# --- LOGICA APP ---

if 'state' not in st.session_state:
    st.session_state.state = "menu"
    st.session_state.score = 0.0
    st.session_state.questions = []
    st.session_state.current_idx = 0
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
        st.session_state.feedback = ("error", f"❌ Faux. La réponse était : {correct}")

# --- UI ---

st.title("⚖️ Quizzeo ARES Elite")
st.markdown("*Simulation avancée avec pénalité -1/3*")

if st.session_state.state == "menu":
    cols = st.columns(2)
    with cols[0]:
        st.button("🧬 Biologie (Elite)", use_container_width=True, on_click=start_quiz, args=("Biologie",))
        st.button("🧪 Chimie (Elite)", use_container_width=True, on_click=start_quiz, args=("Chimie",))
    with cols[1]:
        st.button("📐 Mathématiques (Elite)", use_container_width=True, on_click=start_quiz, args=("Mathématiques",))
        st.button("⚡ Physique (Elite)", use_container_width=True, on_click=start_quiz, args=("Physique",))

elif st.session_state.state == "quiz":
    q = st.session_state.questions[st.session_state.current_idx]
    st.caption(f"Topic: {q['topic']} | Q {st.session_state.current_idx + 1}/10")
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
    st.metric("Score Final", f"{round(st.session_state.score, 2)} / 10")
    if st.button("Menu"):
        st.session_state.state = "menu"
        st.rerun()
