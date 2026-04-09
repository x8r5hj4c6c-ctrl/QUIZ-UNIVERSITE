import streamlit as st
import random
import math
from typing import Dict, List, Tuple, Any
import json
from pathlib import Path

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Matteo x M3.0 | Generatore ARES",
    page_icon="🧬",
    layout="centered"
)

# --- CSS ---
st.markdown("""
<style>
    .stButton > button { background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 24px; font-weight: bold; }
    .stButton > button:hover { background-color: #45a049; }
    .correct-answer { padding: 10px; background-color: #d4edda; border-left: 4px solid #28a745; border-radius: 5px; }
    .incorrect-answer { padding: 10px; background-color: #f8d7da; border-left: 4px solid #dc3545; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- MOTORE DI GENERAZIONE PROCEDURALE ---

class QuestionGenerator:
    """Generatore di domande basato su regole e casualità"""
    
    @staticmethod
    def generate_chimica() -> Dict:
        """Genera una domanda di chimica casuale"""
        tipo = random.choice(["stechiometria", "gas", "soluzioni", "atomo", "equilibrio", "redox"])
        
        if tipo == "stechiometria":
            composti = [("NaCl", 58.44), ("H2O", 18.02), ("CO2", 44.01), ("CaCO3", 100.09), ("H2SO4", 98.08)]
            composto, massa_molare = random.choice(composti)
            massa = random.randint(5, 50)
            moli = massa / massa_molare
            corretto = f"{moli:.2f} mol"
            
            domanda = f"Calcola il numero di moli presenti in {massa} g di {composto} (Massa Molare ≈ {massa_molare:.2f} g/mol)."
            distrattori = [
                f"{massa * massa_molare:.2f} mol",
                f"{massa_molare / massa:.2f} mol",
                f"{(massa / massa_molare) * 1000:.2f} mmol"
            ]
            
        elif tipo == "gas":
            R = 0.0821
            scenario = random.choice(["volume", "pressione", "moli"])
            n = random.randint(1, 5)
            T = random.choice([273, 298, 350])
            P = random.uniform(1.0, 5.0)
            V = (n * R * T) / P
            
            if scenario == "volume":
                domanda = f"Calcola il volume (in L) occupato da {n} moli di gas ideale a {T} K e {P:.1f} atm. (R = 0.0821 L·atm/mol·K)"
                corretto = f"{V:.2f} L"
                distrattori = [f"{(n*R*P)/T:.2f} L", f"{(P*V)/(n*R):.2f} L", f"{V*2:.2f} L"]
            else:
                P_var = random.uniform(1.0, 3.0)
                V_var = random.uniform(10.0, 50.0)
                n_calc = (P_var * V_var) / (R * T)
                domanda = f"Quante moli di gas sono contenute in un recipiente di {V_var:.1f} L a {T} K e {P_var:.1f} atm?"
                corretto = f"{n_calc:.2f} mol"
                distrattori = [f"{(P_var*V_var*R)/T:.2f} mol", f"{n_calc*2:.2f} mol", f"{n_calc/2:.2f} mol"]

        elif tipo == "atomo":
            elementi = [("Carbonio", "C", 6), ("Ossigeno", "O", 8), ("Sodio", "Na", 11), ("Cloro", "Cl", 17), ("Calcio", "Ca", 20)]
            nome, simbolo, Z = random.choice(elementi)
            config_map = {6: "1s² 2s² 2p²", 8: "1s² 2s² 2p⁴", 11: "1s² 2s² 2p⁶ 3s¹", 17: "1s² 2s² 2p⁶ 3s² 3p⁵", 20: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s²"}
            domanda = f"Qual è la configurazione elettronica corretta per il {nome} (Z={Z})?"
            corretto = config_map[Z]
            distrattori = [config_map.get(Z+1, "1s² 2s²"), config_map.get(Z-1, "1s² 2s² 2p⁶"), "1s² 2s² 2p⁶ 3s²"]

        else: # Fallback per altri tipi
            domanda = "Bilanciare la reazione: _Fe + _O2 -> _Fe2O3. Qual è il coefficiente stechiometrico del Fe?"
            corretto = "4"
            distrattori = ["2", "3", "1"]

        opts = [corretto] + distrattori[:3]
        random.shuffle(opts)
        return {"q": domanda, "opts": opts, "ans": corretto, "difficulty": "Moyen", "materia": "Chimica"}

    @staticmethod
    def generate_fisica() -> Dict:
        """Genera una domanda di fisica casuale"""
        tipo = random.choice(["cinematica", "dinamica", "ottica", "elettricita"])
        
        if tipo == "cinematica":
            v0 = random.randint(0, 20)
            a = random.uniform(1.0, 5.0)
            t = random.randint(2, 10)
            s = v0*t + 0.5*a*(t**2)
            domanda = f"Un'auto parte con velocità iniziale {v0} m/s e accelera a {a:.1f} m/s² per {t} secondi. Qual è lo spazio percorso?"
            corretto = f"{s:.1f} m"
            distrattori = [f"{v0*t:.1f} m", f"{a*t:.1f} m", f"{v0 + a*t:.1f} m"]
            
        elif tipo == "dinamica":
            m = random.randint(2, 20)
            a = random.uniform(1.0, 8.0)
            F = m * a
            domanda = f"Una forza costante agisce su una massa di {m} kg imprimendole un'accelerazione di {a:.1f} m/s². Quanto vale la forza?"
            corretto = f"{F:.1f} N"
            distrattori = [f"{m/a:.1f} N", f"{m*a*9.81:.1f} N", f"{F/2:.1f} N"]
            
        elif tipo == "ottica":
            f = random.uniform(5.0, 20.0)
            p = random.uniform(10.0, 30.0)
            q = 1 / ((1/f) - (1/p))
            G = -q/p
            domanda = f"Un oggetto è posto a {p:.1f} cm da una lente convergente di focale f = {f:.1f} cm. Qual è l'ingrandimento lineare G?"
            corretto = f"{G:.2f}"
            distrattori = [f"{-G:.2f}", f"{q:.2f}", f"{p/f:.2f}"]
            
        else: # elettricità
            V = random.randint(5, 24)
            R1 = random.randint(10, 100)
            R2 = random.randint(10, 100)
            I_serie = V / (R1 + R2)
            domanda = f"Due resistenze R1={R1}Ω e R2={R2}Ω sono collegate in serie a una batteria da {V}V. Qual è la corrente nel circuito?"
            corretto = f"{I_serie:.3f} A"
            distrattori = [f"{V/(R1*R2/(R1+R2)):.3f} A", f"{V/R1:.3f} A", f"{I_serie*2:.3f} A"]

        opts = [corretto] + distrattori[:3]
        random.shuffle(opts)
        return {"q": domanda, "opts": opts, "ans": corretto, "difficulty": "Moyen", "materia": "Fisica"}

    @staticmethod
    def generate_biologia() -> Dict:
        """Genera una domanda di biologia basata sul programma ARES"""
        domande_fisse = [
            {"q": "Quale struttura differenzia principalmente una cellula vegetale da una animale?", "opts": ["Parete cellulare", "Mitocondri", "Nucleo", "Ribosomi"], "ans": "Parete cellulare"},
            {"q": "In un incrocio tra due eterozigoti (Aa x Aa), qual è la probabilità di ottenere un fenotipo recessivo?", "opts": ["25%", "50%", "75%", "0%"], "ans": "25%"},
            {"q": "Quale dei seguenti è un esempio di selezione naturale?", "opts": ["Resistenza agli antibiotici nei batteri", "Collo delle giraffe secondo Lamarck", "Peso alla nascita nei neonati umani", "Colore dei fiori nei piselli di Mendel"], "ans": "Resistenza agli antibiotici nei batteri"},
            {"q": "Quale livello ecologico rappresenta l'insieme di tutte le popolazioni in una data area?", "opts": ["Comunità", "Ecosistema", "Biosfera", "Habitat"], "ans": "Comunità"},
            {"q": "Quale fase della mitosi segue immediatamente la metafase?", "opts": ["Anafase", "Profase", "Telofase", "Interfase"], "ans": "Anafase"}
        ]
        scelta = random.choice(domande_fisse)
        opts = list(scelta["opts"])
        random.shuffle(opts)
        return {"q": scelta["q"], "opts": opts, "ans": scelta["ans"], "difficulty": "Facile", "materia": "Biologia"}

    @staticmethod
    def generate_matematica() -> Dict:
        """Genera una domanda di matematica casuale"""
        tipo = random.choice(["algebra", "trigonometria", "analisi"])
        
        if tipo == "algebra":
            a = random.randint(1, 5)
            b = random.randint(-5, 5)
            c = random.randint(-10, 10)
            delta = b**2 - 4*a*c
            if delta >= 0:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                domanda = f"Risolvi l'equazione: {a}x² + {b}x + {c} = 0. Qual è una delle soluzioni?"
                corretto = f"{x1:.2f}"
                distrattori = [f"{-x1:.2f}", f"{a*x1:.2f}", f"{b/a:.2f}"]
            else:
                domanda = f"Risolvi l'equazione: {a}x² + {b}x + {c} = 0. Qual è una delle soluzioni?"
                corretto = "Nessuna soluzione reale"
                distrattori = ["0", "1", "-1"]
                
        elif tipo == "trigonometria":
            angolo = random.choice([30, 45, 60, 90, 180])
            func = random.choice(["sin", "cos"])
            valori = {("sin", 30): "1/2", ("cos", 60): "1/2", ("sin", 90): "1", ("cos", 180): "-1"}
            domanda = f"Quanto vale {func}({angolo}°)?"
            corretto = valori.get((func, angolo), "√2/2")
            distrattori = ["0", "1/2", "√3/2"]
            
        else: # analisi
            a = random.randint(2, 5)
            n = random.randint(2, 4)
            derivata = f"{a*n}x^{n-1}"
            domanda = f"Qual è la derivata di f(x) = {a}x^{n}?"
            corretto = derivata
            distrattori = [f"{a}x^{n-1}", f"{a*n}x^{n}", f"{n}x^{a}"]

        opts = [corretto] + distrattori[:3]
        random.shuffle(opts)
        return {"q": domanda, "opts": opts, "ans": corretto, "difficulty": "Moyen", "materia": "Matematica"}

# --- INIZIALIZZAZIONE STATO ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0
    st.session_state.current_idx = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.current_options = []
    st.session_state.answers_history = []

def start_quiz(materia: str, num_questions: int):
    """Genera un nuovo set di domande"""
    st.session_state.quiz_data = []
    generator = QuestionGenerator()
    
    for _ in range(num_questions):
        if materia == "Tutte le materie":
            materia_casuale = random.choice(["Chimica", "Fisica", "Biologia", "Matematica"])
            if materia_casuale == "Chimica": q = generator.generate_chimica()
            elif materia_casuale == "Fisica": q = generator.generate_fisica()
            elif materia_casuale == "Biologia": q = generator.generate_biologia()
            else: q = generator.generate_matematica()
        else:
            if materia == "Chimica": q = generator.generate_chimica()
            elif materia == "Fisica": q = generator.generate_fisica()
            elif materia == "Biologia": q = generator.generate_biologia()
            else: q = generator.generate_matematica()
            
        st.session_state.quiz_data.append(q)
        
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.answers_history = []
    prepare_question()

def prepare_question():
    idx = st.session_state.current_idx
    if idx < len(st.session_state.quiz_data):
        opts = list(st.session_state.quiz_data[idx]['opts'])
        random.shuffle(opts)
        st.session_state.current_options = opts

def calculate_score_ares() -> float:
    score = 0.0
    for ans in st.session_state.answers_history:
        if ans['is_correct']: score += 1
        else: score -= 1/3
    return score

# --- INTERFACCIA UTENTE ---
st.title("🧬 Matte
