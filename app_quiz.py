import streamlit as st
import random
from typing import Dict, List, Optional
import json
from pathlib import Path

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Matteo x M3.0 | Simulateur ARES",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLES CSS PERSONNALISÉS ---
st.markdown("""
<style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .correct-answer {
        padding: 10px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
    }
    .incorrect-answer {
        padding: 10px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 5px;
    }
    .score-display {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
    }
    .question-counter {
        color: #7f8c8d;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- GESTION PERSISTANCE DES DONNÉES ---
DATA_FILE = Path("quiz_progress.json")

def save_progress():
    """Sauvegarde la progression du quiz"""
    progress_data = {
        "quiz_data": st.session_state.quiz_data,
        "score": st.session_state.score,
        "current_idx": st.session_state.current_idx,
        "finished": st.session_state.finished,
        "submitted": st.session_state.submitted,
        "answers_history": st.session_state.answers_history,
        "selected_materia": st.session_state.selected_materia
    }
    DATA_FILE.write_text(json.dumps(progress_data))

def load_progress() -> Optional[Dict]:
    """Charge la progression sauvegardée"""
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return None

# --- BASE DE DONNÉES ÉTENDUE (Questions inspirées des annales ARES) ---
def init_database():
    """Initialise la base de données des questions"""
    return {
        "Biologie": [
            {"q": "Quelle structure est absente dans une cellule animale mais présente dans une cellule végétale ?", 
             "opts": ["Paroi cellulosique", "Mitochondrie", "Noyau", "Membrane plasmique"], 
             "ans": "Paroi cellulosique",
             "difficulty": "Facile",
             "explanation": "La paroi cellulosique est une structure rigide présente uniquement chez les cellules végétales."},
            {"q": "Le rôle principal des mitochondries est :", 
             "opts": ["La respiration cellulaire", "La synthèse des protéines", "La photosynthèse", "Le stockage des graisses"], 
             "ans": "La respiration cellulaire",
             "difficulty": "Facile",
             "explanation": "Les mitochondries sont les centrales énergétiques de la cellule."},
            {"q": "Quelle est la base azotée spécifique à l'ARN ?", 
             "opts": ["Uracile", "Thymine", "Adénine", "Cytosine"], 
             "ans": "Uracile",
             "difficulty": "Moyen",
             "explanation": "L'uracile remplace la thymine dans l'ARN."},
            {"q": "Un nucléotide d'ADN est composé de :", 
             "opts": ["Désoxyribose + Base azotée + Phosphate", "Ribose + Base azotée + Phosphate", "Acide aminé + Phosphate", "Glucose + Base azotée"], 
             "ans": "Désoxyribose + Base azotée + Phosphate",
             "difficulty": "Moyen",
             "explanation": "Le désoxyribose est le sucre spécifique de l'ADN."},
            {"q": "La mitose produit :", 
             "opts": ["Deux cellules filles identiques", "Quatre cellules haploïdes", "Deux gamètes", "Une cellule œuf"], 
             "ans": "Deux cellules filles identiques",
             "difficulty": "Facile",
             "explanation": "La mitose est une division cellulaire produisant deux cellules filles génétiquement identiques."},
            {"q": "Qu'illustre le fait que les moustiques résistants aux insecticides prédominent dans les régions traitées ?",
             "opts": ["Le créationnisme", "La macro-évolution", "La sélection naturelle", "La théorie de Lamarck"],
             "ans": "La sélection naturelle",
             "difficulty": "Moyen",
             "explanation": "C'est un exemple classique de pression de sélection exercée par l'environnement (ici, l'insecticide) [citation:1]."}
        ],
        "Chimie": [
            {"q": "Quelle est la configuration électronique du Carbone (Z=6) ?", 
             "opts": ["1s² 2s² 2p²", "1s² 2s² 2p⁶", "1s² 2s²", "1s² 2p⁴"], 
             "ans": "1s² 2s² 2p²",
             "difficulty": "Moyen",
             "explanation": "Le carbone a 6 électrons répartis en 1s² 2s² 2p²."},
            {"q": "Quel est le pH d'une solution neutre à 25°C ?", 
             "opts": ["7", "0", "14", "1"], 
             "ans": "7",
             "difficulty": "Facile",
             "explanation": "À 25°C, le pH neutre est 7."},
            {"q": "Le groupe fonctionnel -OH caractérise quelle famille ?", 
             "opts": ["Les alcools", "Les aldéhydes", "Les cétones", "Les acides carboxyliques"], 
             "ans": "Les alcools",
             "difficulty": "Facile",
             "explanation": "Le groupe hydroxyle (-OH) est caractéristique des alcools."},
            {"q": "La mole est l'unité de :", 
             "opts": ["La quantité de matière", "La masse", "Le volume", "La pression"], 
             "ans": "La quantité de matière",
             "difficulty": "Facile",
             "explanation": "La mole mesure la quantité de matière (6,022 × 10²³ entités)."},
            {"q": "Dans la réaction du permanganate de potassium avec l'iodure de potassium en milieu acide, combien de molécules d'eau faut-il ajouter pour équilibrer ?",
             "opts": ["8 à droite", "4 à gauche", "8 à gauche", "Aucune"],
             "ans": "8 à droite",
             "difficulty": "Difficile",
             "explanation": "La réaction d'oxydoréduction nécessite 8 H₂O pour équilibrer les oxygènes et hydrogènes en milieu acide [citation:1]."}
        ],
        "Physique": [
            {"q": "Un corps de 5 kg est soumis à une force de 20 N. Quelle est son accélération ?", 
             "opts": ["4 m/s²", "100 m/s²", "0.25 m/s²", "15 m/s²"], 
             "ans": "4 m/s²",
             "difficulty": "Moyen",
             "explanation": "F = ma → a = F/m = 20/5 = 4 m/s²"},
            {"q": "La loi d'Ohm s'écrit :", 
             "opts": ["U = R * I", "P = U * I", "V = d / t", "E = mc²"], 
             "ans": "U = R * I",
             "difficulty": "Facile",
             "explanation": "U = R × I est la loi fondamentale de l'électricité."},
            {"q": "L'unité de la force dans le Système International est le :", 
             "opts": ["Newton", "Joule", "Watt", "Pascal"], 
             "ans": "Newton",
             "difficulty": "Facile",
             "explanation": "Le Newton (N) est l'unité de force."},
            {"q": "Quelle doit être la section d'un fil de résistivité 1,6.10⁻⁸ Ωm pour que sa résistance soit de 1Ω ? (longueur estimée à 20m)",
             "opts": ["0,32 mm²", "3,2 mm²", "32 mm²", "320 mm²"],
             "ans": "32 mm²",
             "difficulty": "Difficile",
             "explanation": "R = ρ*L/S => S = ρ*L/R. Le calcul nécessite de connaître la longueur du fil (ici, 200 spires de cadre mobile) [citation:1]."}
        ],
        "Mathématiques": [
            {"q": "Quelle est la dérivée de f(x) = x² ?", 
             "opts": ["2x", "x", "2", "x³/3"], 
             "ans": "2x",
             "difficulty": "Facile",
             "explanation": "La dérivée de x^n est n·x^(n-1)"},
            {"q": "La somme des angles internes d'un triangle est :", 
             "opts": ["180°", "360°", "90°", "270°"], 
             "ans": "180°",
             "difficulty": "Facile",
             "explanation": "La somme des angles d'un triangle est toujours 180°."},
            {"q": "Quelle est la valeur de log10(100) ?", 
             "opts": ["2", "10", "1", "0"], 
             "ans": "2",
             "difficulty": "Facile",
             "explanation": "10² = 100, donc log10(100) = 2"},
            {"q": "Dans un repère orthonormé, A(0;3), B(3;6), C(4;4). Que vaut le cosinus de l'angle ABC ?",
             "opts": ["√6/6", "√8/8", "√10/10", "√12/12"],
             "ans": "√10/10",
             "difficulty": "Difficile",
             "explanation": "Calcul vectoriel avec BA et BC. cos(θ) = (BA·BC) / (||BA|| * ||BC||) [citation:1]."}
        ],
        "Communication & Raisonnement": [
            {"q": "Consultation : 'Bonjour Mme D., que puis-je faire pour vous aujourd'hui ?' Pourquoi cette phrase est-elle la plus adaptée ?",
             "opts": ["Car elle est la plus rapide", "Car c'est une question ouverte qui laisse la patiente s'exprimer", "Car elle rappelle le motif de consultation", "Car elle impose le sujet de l'hypertension"],
             "ans": "Car c'est une question ouverte qui laisse la patiente s'exprimer",
             "difficulty": "Facile",
             "explanation": "En médecine, une question ouverte permet de ne pas présupposer du motif de consultation [citation:1]."},
            {"q": "Votre mère fumeuse dit en public avoir arrêté, ce qui est faux. Quelle est la réaction la plus appropriée ?",
             "opts": ["Ne rien dire", "Faire de grands yeux réprobateurs", "En parler en privé après le dîner", "La reprendre ironiquement devant les invités"],
             "ans": "En parler en privé après le dîner",
             "difficulty": "Facile",
             "explanation": "Il est préférable de ne pas humilier ou confronter un proche en public, mais d'aborder le sujet en privé [citation:1]."},
            {"q": "Votre ami a mauvaise haleine. Vous devez :",
             "opts": ["Lui faire la remarque poliment", "Lui proposer un chewing-gum sans rien dire", "Parler d'un autre problème dentaire", "Ne rien dire"],
             "ans": "Lui faire la remarque poliment",
             "difficulty": "Moyen",
             "explanation": "L'honnêteté avec tact est souvent la meilleure approche pour un ami [citation:1]."},
            {"q": "Face à une patiente nécessitant une opération urgente de l'aorte, quelle est l'attitude la plus empathique ?",
             "opts": ["Appeler le bloc en sa présence", "Écouter ses inquiétudes tout en expliquant l'urgence", "Rester focalisé sur la maladie", "Lui conseiller de réfléchir et de rappeler"],
             "ans": "Écouter ses inquiétudes tout en expliquant l'urgence",
             "difficulty": "Moyen",
             "explanation": "L'empathie consiste à reconnaître les émotions du patient tout en assurant sa prise en charge médicale [citation:1]."}
        ]
    }

# --- INITIALISATION SESSION STATE ---
if 'db_ares' not in st.session_state:
    st.session_state.db_ares = init_database()

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.quiz_data = []
    st.session_state.score = 0
    st.session_state.current_idx = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.current_options = []
    st.session_state.answers_history = []
    st.session_state.selected_materia = None
    st.session_state.num_questions = 10
    st.session_state.show_explanations = True

# --- FONCTIONS UTILITAIRES ---
def start_quiz(materia: str, num_questions: int = 10):
    """Démarre un nouveau quiz"""
    questions = list(st.session_state.db_ares[materia])
    random.shuffle(questions)
    st.session_state.quiz_data = questions[:min(num_questions, len(questions))]
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.answers_history = []
    st.session_state.selected_materia = materia
    prepare_question()

def prepare_question():
    """Prépare la question courante avec options mélangées"""
    idx = st.session_state.current_idx
    if idx < len(st.session_state.quiz_data):
        opts = list(st.session_state.quiz_data[idx]['opts'])
        random.shuffle(opts)
        st.session_state.current_options = opts

def calculate_score_ares() -> float:
    """Calcule le score selon la méthode ARES (+1 pour une bonne réponse, -1/3 pour une erreur)"""
    score = 0.0
    for answer in st.session_state.answers_history:
        if answer['is_correct']:
            score += 1
        else:
            score -= 1/3
    return score

def get_feedback_message(percentage: float) -> str:
    """Retourne un message de feedback personnalisé"""
    if percentage >= 90:
        return "Excellent ! 🌟 Vous maîtrisez parfaitement le sujet !"
    elif percentage >= 70:
        return "Très bien ! 👍 Continuez comme ça !"
    elif percentage >= 50:
        return "Pas mal ! 📚 Un peu plus de révision et ce sera parfait !"
    else:
        return "Continuez à vous entraîner ! 💪 La pratique fait le maître !"

# --- INTERFACE PRINCIPALE ---
st.title("🚀 Matteo x M3.0")
st.markdown("### Simulateur ARES 2018-2025")

# Sidebar avec options
with st.sidebar:
    st.header("⚙️ Paramètres")
    st.session_state.num_questions = st.slider(
        "Nombre de questions", 
        min_value=5, 
        max_value=20, 
        value=st.session_state.num_questions
    )
    st.session_state.show_explanations = st.checkbox(
        "Afficher les explications", 
        value=st.session_state.show_explanations
    )
    
    # Sauvegarde/Chargement
    st.header("💾 Progression")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sauvegarder", use_container_width=True
