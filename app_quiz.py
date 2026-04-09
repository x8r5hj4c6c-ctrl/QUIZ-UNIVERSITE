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

# --- BASE DE DONNÉES ÉTENDUE ---
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
             "explanation": "La mitose est une division cellulaire produisant deux cellules filles génétiquement identiques."}
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
             "explanation": "La mole mesure la quantité de matière (6,022 × 10²³ entités)."}
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
             "explanation": "Le Newton (N) est l'unité de force."}
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
             "explanation": "10² = 100, donc log10(100) = 2"}
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

def calculate_percentage() -> float:
    """Calcule le pourcentage de réussite"""
    if len(st.session_state.quiz_data) > 0:
        return (st.session_state.score / len(st.session_state.quiz_data)) * 100
    return 0

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
        if st.button("Sauvegarder", use_container_width=True):
            if st.session_state.quiz_data and not st.session_state.finished:
                save_progress()
                st.success("✅ Progression sauvegardée !")
            else:
                st.warning("⚠️ Pas de quiz en cours")
    with col2:
        if st.button("Charger", use_container_width=True):
            progress = load_progress()
            if progress:
                for key, value in progress.items():
                    st.session_state[key] = value
                st.success("✅ Progression chargée !")
                st.rerun()
            else:
                st.warning("⚠️ Aucune sauvegarde trouvée")

# Zone principale
if not st.session_state.quiz_data or st.session_state.finished:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        materia_scelta = st.selectbox(
            "📚 Choisissez votre matière :", 
            list(st.session_state.db_ares.keys())
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        start_button = st.button(
            "▶️ Commencer le Quiz", 
            use_container_width=True,
            type="primary"
        )
    
    if start_button:
        start_quiz(materia_scelta, st.session_state.num_questions)
        st.rerun()
    
    # Statistiques des questions disponibles
    st.markdown("---")
    st.subheader("📊 Questions disponibles")
    for materia, questions in st.session_state.db_ares.items():
        st.write(f"**{materia}**: {len(questions)} questions")

else:
    idx = st.session_state.current_idx
    q = st.session_state.quiz_data[idx]
    
    # En-tête du quiz
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**{st.session_state.selected_materia}**")
    with col2:
        st.markdown(f"📊 **Score: {st.session_state.score}/{idx}**")
    with col3:
        if st.button("🏠 Menu", use_container_width=True):
            st.session_state.quiz_data = []
            st.session_state.finished = False
            if DATA_FILE.exists():
                DATA_FILE.unlink()
            st.rerun()
    
    # Progression
    progress_value = (idx + 1) / len(st.session_state.quiz_data)
    st.progress(progress_value)
    st.markdown(f"<p class='question-counter'>Question {idx + 1} sur {len(st.session_state.quiz_data)}</p>", 
                unsafe_allow_html=True)
    
    # Question
    st.markdown(f"### {q['q']}")
    if 'difficulty' in q:
        difficulty_color = {"Facile": "🟢", "Moyen": "🟡", "Difficile": "🔴"}.get(q['difficulty'], "")
        st.caption(f"Difficulté: {difficulty_color} {q['difficulty']}")
    
    # Formulaire de réponse
    with st.form(key=f"form_{idx}"):
        user_choice = st.radio(
            "✨ Sélectionnez votre réponse :", 
            st.session_state.current_options,
            key=f"radio_{idx}"
        )
        submit = st.form_submit_button("✅ Valider la réponse", use_container_width=True)
    
    if submit and not st.session_state.submitted:
        st.session_state.submitted = True
        is_correct = user_choice == q['ans']
        
        # Enregistrement de la réponse
        st.session_state.answers_history.append({
            'question': q['q'],
            'user_answer': user_choice,
            'correct_answer': q['ans'],
            'is_correct': is_correct
        })
        
        if is_correct:
            st.session_state.score += 1
            st.success("✅ Correct !")
            if st.session_state.show_explanations and 'explanation' in q:
                st.markdown(f"<div class='correct-answer'>💡 {q['explanation']}</div>", 
                          unsafe_allow_html=True)
        else:
            st.error(f"❌ Incorrect. La réponse était : **{q['ans']}**")
            if st.session_state.show_explanations and 'explanation' in q:
                st.markdown(f"<div class='incorrect-answer'>💡 {q['explanation']}</div>", 
                          unsafe_allow_html=True)
    
    # Navigation
    if st.session_state.submitted:
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("⬅️ Précédent", use_container_width=True) and idx > 0:
                st.session_state.current_idx -= 1
                st.session_state.submitted = False
                prepare_question()
                st.rerun()
        with col2:
            button_text = "Terminer 🏁" if idx + 1 >= len(st.session_state.quiz_data) else "Continuer ➡️"
            if st.button(button_text, use_container_width=True, type="primary"):
                if idx + 1 < len(st.session_state.quiz_data):
                    st.session_state.current_idx += 1
                    st.session_state.submitted = False
                    prepare_question()
                    st.rerun()
                else:
                    st.session_state.finished = True
                    st.rerun()

# --- ÉCRAN FINAL ---
if st.session_state.finished:
    st.balloons()
    st.header("🏁 Résultats du Quiz")
    
    # Score principal
    percentage = calculate_percentage()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{st.session_state.score}/{len(st.session_state.quiz_data)}")
    with col2:
        st.metric("Pourcentage", f"{percentage:.1f}%")
