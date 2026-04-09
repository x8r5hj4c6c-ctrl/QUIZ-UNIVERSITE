import streamlit as st
import random
import math
from typing import Dict, List, Tuple, Any

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Matteo x M3.0 | Générateur ARES",
    page_icon="🧬",
    layout="centered"
)

# --- STYLES CSS ---
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
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
    }
    .explication-box {
        background-color: #e7f3ff;
        padding: 12px;
        border-radius: 8px;
        margin-top: 15px;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# --- MOTEUR DE GÉNÉRATION PROCÉDURALE EN FRANÇAIS ---

class GenerateurQuestions:
    """Générateur de questions basé sur le programme officiel ARES"""
    
    @staticmethod
    def generer_chimie() -> Dict:
        """Génère une question de chimie aléatoire"""
        type_question = random.choice([
            "stoechiometrie", "gaz", "solutions", "atome", 
            "equilibre", "redox", "liaisons", "molarite"
        ])
        
        if type_question == "stoechiometrie":
            composes = [
                ("NaCl", 58.44, "chlorure de sodium"),
                ("H₂O", 18.02, "eau"),
                ("CO₂", 44.01, "dioxyde de carbone"),
                ("CaCO₃", 100.09, "carbonate de calcium"),
                ("H₂SO₄", 98.08, "acide sulfurique"),
                ("NaOH", 40.00, "hydroxyde de sodium"),
                ("C₆H₁₂O₆", 180.16, "glucose")
            ]
            compose, masse_molaire, nom = random.choice(composes)
            masse = round(random.uniform(5, 100), 1)
            moles = masse / masse_molaire
            
            question = f"Calculez le nombre de moles présentes dans {masse} g de {nom} ({compose}). (Masse molaire ≈ {masse_molaire:.2f} g/mol)"
            correct = f"{moles:.3f} mol"
            distracteurs = [
                f"{masse * masse_molaire:.3f} mol",
                f"{masse_molaire / masse:.3f} mol",
                f"{(masse / masse_molaire) * 1000:.3f} mmol"
            ]
            explication = f"n = m / M = {masse} g / {masse_molaire:.2f} g/mol = {moles:.3f} mol"
            
        elif type_question == "gaz":
            R = 0.0821
            scenario = random.choice(["volume", "pression", "moles"])
            n = random.randint(1, 5)
            T = random.choice([273, 298, 310, 350])
            P = round(random.uniform(1.0, 5.0), 2)
            V = (n * R * T) / P
            
            if scenario == "volume":
                question = f"Calculez le volume (en L) occupé par {n} mole(s) de gaz parfait à {T} K et {P} atm. (R = 0,0821 L·atm·mol⁻¹·K⁻¹)"
                correct = f"{V:.2f} L"
                distracteurs = [
                    f"{(n * R * P) / T:.2f} L",
                    f"{(P * V) / (n * R):.2f} L",
                    f"{V * 1.5:.2f} L"
                ]
                explication = f"PV = nRT → V = nRT/P = {n} × 0,0821 × {T} / {P} = {V:.2f} L"
            elif scenario == "pression":
                V_var = round(random.uniform(5.0, 20.0), 1)
                P_calc = (n * R * T) / V_var
                question = f"Quelle est la pression (en atm) exercée par {n} mole(s) de gaz parfait à {T} K dans un volume de {V_var} L ?"
                correct = f"{P_calc:.2f} atm"
                distracteurs = [
                    f"{(n * R * V_var) / T:.2f} atm",
                    f"{P_calc * 2:.2f} atm",
                    f"{P_calc / 2:.2f} atm"
                ]
                explication = f"PV = nRT → P = nRT/V = {n} × 0,0821 × {T} / {V_var} = {P_calc:.2f} atm"
            else:
                P_var = round(random.uniform(1.0, 3.0), 2)
                V_var = round(random.uniform(10.0, 50.0), 1)
                n_calc = (P_var * V_var) / (R * T)
                question = f"Combien de moles de gaz sont contenues dans un récipient de {V_var} L à {T} K et {P_var} atm ?"
                correct = f"{n_calc:.3f} mol"
                distracteurs = [
                    f"{(P_var * V_var * R) / T:.3f} mol",
                    f"{n_calc * 1.5:.3f} mol",
                    f"{n_calc / 1.5:.3f} mol"
                ]
                explication = f"PV = nRT → n = PV/RT = {P_var} × {V_var} / (0,0821 × {T}) = {n_calc:.3f} mol"
                
        elif type_question == "solutions":
            type_sol = random.choice(["molarite", "dilution", "fraction"])
            
            if type_sol == "molarite":
                solute = random.choice(["NaCl", "KCl", "NaOH", "HCl", "H₂SO₄"])
                masses = {"NaCl": 58.44, "KCl": 74.55, "NaOH": 40.00, "HCl": 36.46, "H₂SO₄": 98.08}
                M = masses[solute]
                masse = round(random.uniform(1, 20), 2)
                volume = round(random.uniform(0.1, 1.0), 2)
                C = masse / (M * volume)
                question = f"On dissout {masse} g de {solute} dans de l'eau pour obtenir {volume} L de solution. Quelle est la concentration molaire ?"
                correct = f"{C:.3f} mol/L"
                distracteurs = [
                    f"{masse / volume:.3f} mol/L",
                    f"{masse * M / volume:.3f} mol/L",
                    f"{C * 2:.3f} mol/L"
                ]
                explication = f"C = n/V = (m/M)/V = ({masse}/{M})/{volume} = {C:.3f} mol/L"
                
            elif type_sol == "dilution":
                C1 = round(random.uniform(1.0, 5.0), 2)
                V1 = round(random.uniform(10, 50), 1)
                V2 = round(random.uniform(100, 500), 1)
                C2 = (C1 * V1) / V2
                question = f"On dilue {V1} mL d'une solution de concentration {C1} mol/L dans un volume final de {V2} mL. Quelle est la nouvelle concentration ?"
                correct = f"{C2:.4f} mol/L"
                distracteurs = [
                    f"{C1 * V2 / V1:.4f} mol/L",
                    f"{(C1 * V1) / (V2 - V1):.4f} mol/L",
                    f"{C1:.4f} mol/L"
                ]
                explication = f"C₁V₁ = C₂V₂ → C₂ = C₁V₁/V₂ = {C1} × {V1} / {V2} = {C2:.4f} mol/L"
                
            else:  # fraction molaire
                n1 = random.randint(1, 5)
                n2 = random.randint(1, 10)
                frac = n1 / (n1 + n2)
                question = f"Un mélange contient {n1} mole(s) d'éthanol et {n2} moles d'eau. Quelle est la fraction molaire de l'éthanol ?"
                correct = f"{frac:.3f}"
                distracteurs = [
                    f"{n1 / n2:.3f}",
                    f"{n2 / (n1 + n2):.3f}",
                    f"{(n1 + n2) / n1:.3f}"
                ]
                explication = f"x₁ = n₁ / (n₁ + n₂) = {n1} / ({n1} + {n2}) = {frac:.3f}"

        elif type_question == "atome":
            elements = [
                ("Carbone", "C", 6, "1s² 2s² 2p²"),
                ("Oxygène", "O", 8, "1s² 2s² 2p⁴"),
                ("Sodium", "Na", 11, "1s² 2s² 2p⁶ 3s¹"),
                ("Chlore", "Cl", 17, "1s² 2s² 2p⁶ 3s² 3p⁵"),
                ("Calcium", "Ca", 20, "1s² 2s² 2p⁶ 3s² 3p⁶ 4s²"),
                ("Fer", "Fe", 26, "1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶"),
                ("Magnésium", "Mg", 12, "1s² 2s² 2p⁶ 3s²")
            ]
            nom, symbole, Z, config = random.choice(elements)
            
            sous_type = random.choice(["config", "valence", "octet"])
            
            if sous_type == "config":
                question = f"Quelle est la configuration électronique correcte du {nom} (Z = {Z}) ?"
                correct = config
                configs_fausses = [
                    "1s² 2s² 2p⁶ 3s² 3p⁶",
                    "1s² 2s² 2p⁶ 3s²",
                    "1s² 2s² 2p⁶"
                ]
                distracteurs = [c for c in configs_fausses if c != config][:3]
                explication = f"Le {nom} a {Z} électrons. Sa configuration est {config}."
            elif sous_type == "valence":
                valence = config.count('s') + config.count('p')
                if Z <= 2: valence = Z
                elif Z <= 10: valence = Z - 2 if Z > 2 else Z
                question = f"Combien d'électrons de valence possède un atome de {nom} (Z = {Z}) ?"
                nb_valence = config.split()[-1].count('s') * 2 + config.split()[-1].count('p') * 6
                nb_valence = sum(int(c) for c in config.split()[-1] if c.isdigit())
                correct = str(nb_valence)
                distracteurs = [str(nb_valence + 1), str(nb_valence - 1), str(nb_valence + 2)]
                explication = f"Les électrons de valence sont ceux de la dernière couche. Pour {config}, la couche de valence contient {nb_valence} électrons."
            else:
                question = f"Pour respecter la règle de l'octet, combien d'électrons un atome de {nom} (Z = {Z}) doit-il gagner ou perdre ?"
                if Z in [1, 3, 11, 19]:
                    correct = "Perdre 1 électron"
                    explication = f"Le {nom} a 1 électron de valence. Il tend à le perdre pour obtenir la configuration du gaz noble précédent."
                elif Z in [8, 16]:
                    correct = "Gagner 2 électrons"
                    explication = f"Le {nom} a 6 électrons de valence. Il tend à en gagner 2 pour obtenir un octet."
                elif Z in [17, 9]:
                    correct = "Gagner 1 électron"
                    explication = f"Le {nom} a 7 électrons de valence. Il tend à en gagner 1 pour obtenir un octet."
                else:
                    correct = "Gagner 2 électrons" if Z == 8 else "Perdre 2 électrons"
                    explication = f"Le {nom} ajuste ses électrons pour atteindre la configuration d'un gaz noble."
                distracteurs = ["Gagner 1 électron", "Perdre 2 électrons", "Gagner 3 électrons"]

        elif type_question == "equilibre":
            reaction = random.choice([
                "N₂ + 3H₂ ⇌ 2NH₃",
                "2SO₂ + O₂ ⇌ 2SO₃",
                "PCl₅ ⇌ PCl₃ + Cl₂",
                "H₂ + I₂ ⇌ 2HI",
                "CO + H₂O ⇌ CO₂ + H₂"
            ])
            
            type_eq = random.choice(["constante", "deplacement"])
            
            if type_eq == "constante":
                if reaction == "N₂ + 3H₂ ⇌ 2NH₃":
                    Kc = round(random.uniform(0.01, 10), 2)
                    conc_N2 = round(random.uniform(0.1, 1.0), 2)
                    conc_H2 = round(random.uniform(0.1, 1.0), 2)
                    conc_NH3 = math.sqrt(Kc * conc_N2 * conc_H2**3)
                    question = f"Soit l'équilibre : {reaction}. À l'équilibre, [N₂] = {conc_N2} M, [H₂] = {conc_H2} M. Calculez [NH₃] si Kc = {Kc}."
                    correct = f"{conc_NH3:.3f} M"
                    distracteurs = [
                        f"{Kc * conc_N2 * conc_H2:.3f} M",
                        f"{math.sqrt(Kc * conc_N2 * conc_H2):.3f} M",
                        f"{conc_NH3 * 2:.3f} M"
                    ]
                    explication = f"Kc = [NH₃]² / ([N₂][H₂]³) → [NH₃] = √(Kc × [N₂] × [H₂]³) = √({Kc} × {conc_N2} × {conc_H2}³) = {conc_NH3:.3f} M"
                else:
                    question = f"Pour la réaction {reaction}, comment s'écrit la constante d'équilibre Kc ?"
                    correct = "Kc = [produits] / [réactifs] avec coefficients en exposants"
                    distracteurs = [
                        "Kc = [réactifs] / [produits]",
                        "Kc = [produits] × [réactifs]",
                        "Kc = [produits] + [réactifs]"
                    ]
                    explication = "Kc est le rapport des concentrations des produits sur celles des réactifs, chaque concentration étant élevée à la puissance de son coefficient stœchiométrique."
            else:
                perturbation = random.choice(["pression", "température", "concentration"])
                if perturbation == "pression":
                    question = f"Pour l'équilibre {reaction}, quel est l'effet d'une augmentation de pression ?"
                    if reaction in ["N₂ + 3H₂ ⇌ 2NH₃", "2SO₂ + O₂ ⇌ 2SO₃"]:
                        correct = "Déplacement vers la droite"
                        explication = "Le principe de Le Chatelier : une augmentation de pression favorise le côté avec moins de moles gazeuses."
                    elif reaction == "PCl₅ ⇌ PCl₃ + Cl₂":
                        correct = "Déplacement vers la gauche"
                        explication = "Le principe de Le Chatelier : une augmentation de pression favorise le côté avec moins de moles gazeuses (1 mole à gauche, 2 à droite)."
                    else:
                        correct = "Aucun déplacement"
                        explication = "Le nombre de moles gazeuses est identique des deux côtés."
                    distracteurs = ["Déplacement vers la gauche", "Déplacement vers la droite", "Aucun déplacement"]
                else:
                    question = f"Pour l'équilibre {reaction}, quel est l'effet d'une augmentation de la concentration des réactifs ?"
                    correct = "Déplacement vers la droite"
                    distracteurs = ["Déplacement vers la gauche", "Aucun déplacement", "Augmentation de Kc"]
                    explication = "Le principe de Le Chatelier : l'ajout de réactifs déplace l'équilibre vers les produits."

        else:  # redox ou autre
            oxydants = ["MnO₄⁻", "Cr₂O₇²⁻", "H₂O₂", "Cl₂"]
            reducteurs = ["Fe²⁺", "I⁻", "SO₃²⁻", "H₂S"]
            ox = random.choice(oxydants)
            red = random.choice(reducteurs)
            question = f"Dans la réaction d'oxydoréduction entre {ox} et {red}, quel est le rôle de {ox} ?"
            correct = "Oxydant"
            distracteurs = ["Réducteur", "Catalyseur", "Spectateur"]
            explication = f"{ox} est un oxydant car il capte des électrons et est réduit lors de la réaction."

        # Mélanger les options
        opts = [correct] + distracteurs[:3]
        random.shuffle(opts)
        
        return {
            "q": question,
            "opts": opts,
            "ans": correct,
            "difficulte": random.choice(["Facile", "Moyen", "Difficile"]),
            "matiere": "Chimie",
            "explication": explication
        }

    @staticmethod
    def generer_physique() -> Dict:
        """Génère une question de physique aléatoire"""
        type_question = random.choice([
            "cinematique", "dynamique", "statique", "travail_energie",
            "ondes", "optique", "electricite", "magnetisme"
        ])
        
        if type_question == "cinematique":
            sous_type = random.choice(["mrua", "chute", "projectile"])
            
            if sous_type == "mrua":
                v0 = random.randint(0, 30)
                a = round(random.uniform(1.0, 8.0), 1)
                t = random.randint(2, 15)
                s = v0 * t + 0.5 * a * t**2
                vf = v0 + a * t
                
                ce_quon_demande = random.choice(["distance", "vitesse"])
                if ce_quon_demande == "distance":
                    question = f"Une voiture roule à {v0} m/s et accélère de {a} m/s² pendant {t} secondes. Quelle distance parcourt-elle ?"
                    correct = f"{s:.1f} m"
                    distracteurs = [
                        f"{v0 * t:.1f} m",
                        f"{a * t**2:.1f} m",
                        f"{v0 + a * t:.1f} m"
                    ]
                    explication = f"d = v₀t + ½at² = {v0}×{t} + ½×{a}×{t}² = {s:.1f} m"
                else:
                    question = f"Une voiture roule à {v0} m/s et accélère de {a} m/s² pendant {t} secondes. Quelle est sa vitesse finale ?"
                    correct = f"{vf:.1f} m/s"
                    distracteurs = [
                        f"{v0:.1f} m/s",
                        f"{a * t:.1f} m/s",
                        f"{vf * 2:.1f} m/s"
                    ]
                    explication = f"v = v₀ + at = {v0} + {a}×{t} = {vf:.1f} m/s"
                    
            elif sous_type == "chute":
                h = random.randint(10, 100)
                g = 9.81
                t_chute = math.sqrt(2 * h / g)
                v_impact = g * t_chute
                
                demande = random.choice(["temps", "vitesse"])
                if demande == "temps":
                    question = f"Un objet est lâché d'une hauteur de {h} m. Combien de temps met-il pour atteindre le sol ? (g = 9,81 m/s²)"
                    correct = f"{t_chute:.2f} s"
                    distracteurs = [
                        f"{h / g:.2f} s",
                        f"{math.sqrt(h / g):.2f} s",
                        f"{t_chute * 1.5:.2f} s"
                    ]
                    explication = f"h = ½gt² → t = √(2h/g) = √(2×{h}/9,81) = {t_chute:.2f} s"
                else:
                    question = f"Un objet est lâché d'une hauteur de {h} m. Quelle est sa vitesse juste avant l'impact ? (g = 9,81 m/s²)"
                    correct = f"{v_impact:.2f} m/s"
                    distracteurs = [
                        f"{g * h:.2f} m/s",
                        f"{v_impact / 2:.2f} m/s",
                        f"{math.sqrt(g * h):.2f} m/s"
                    ]
                    explication = f"v = gt et t = √(2h/g) → v = g√(2h/g) = √(2gh) = √(2×9,81×{h}) = {v_impact:.2f} m/s"
                    
            else:  # projectile
                v0 = random.randint(10, 30)
                angle = random.choice([30, 45, 60])
                g = 9.81
                portee = (v0**2 * math.sin(2 * math.radians(angle))) / g
                question = f"Un projectile est lancé avec une vitesse initiale de {v0} m/s sous un angle de {angle}°. Quelle est sa portée ? (g = 9,81 m/s²)"
                correct = f"{portee:.1f} m"
                distracteurs = [
                    f"{(v0**2 * math.sin(math.radians(angle))) / g:.1f} m",
                    f"{v0**2 / g:.1f} m",
                    f"{portee * 1.2:.1f} m"
                ]
                explication = f"Portée = (v₀² × sin(2θ)) / g = ({v0}² × sin({2*angle}°)) / 9,81 = {portee:.1f} m"

        elif type_question == "dynamique":
            m = random.randint(2, 25)
            a = round(random.uniform(1.0, 10.0), 1)
            F = m * a
            
            scenario = random.choice(["force", "acceleration", "masse"])
            if scenario == "force":
                question = f"Une force constante agit sur une masse de {m} kg et lui communique une accélération de {a} m/s². Quelle est l'intensité de cette force ?"
                correct = f"{F:.1f} N"
                distracteurs = [
                    f"{m / a:.1f} N",
                    f"{m * 9.81:.1f} N",
                    f"{F / 2:.1f} N"
                ]
                explication = f"F = m × a = {m} × {a} = {F:.1f} N"
            elif scenario == "acceleration":
                question = f"Une force de {F:.1f} N agit sur une masse de {m} kg. Quelle est l'accélération ?"
                correct = f"{a:.1f} m/s²"
                distracteurs = [
                    f"{F * m:.1f} m/s²",
                    f"{m / F:.1f} m/s²",
                    f"{a * 9.81:.1f} m/s²"
                ]
                explication = f"a = F / m = {F:.1f} / {m} = {a:.1f} m/s²"
            else:
                question = f"Une force de {F:.1f} N communique une accélération de {a} m/s² à un objet. Quelle est sa masse ?"
                correct = f"{m:.1f} kg"
                distracteurs = [
                    f"{F * a:.1f} kg",
                    f"{a / F:.1f} kg",
                    f"{m / 2:.1f} kg"
                ]
                explication = f"m = F / a = {F:.1f} / {a} = {m:.1f} kg"

        elif type_question == "travail_energie":
            m = random.randint(5, 50)
            h = random.randint(2, 20)
            g = 9.81
            Ep = m * g * h
            Ec = 0.5 * m * (random.randint(5, 15))**2
            
            type_e = random.choice(["potentielle", "cinetique"])
            if type_e == "potentielle":
                question = f"Calculez l'énergie potentielle gravitationnelle d'un objet de {m} kg placé à {h} m de hauteur. (g = 9,81 m/s²)"
                correct = f"{Ep:.1f} J"
                distracteurs = [
                    f"{m * h:.1f} J",
                    f"{m * g:.1f} J",
                    f"{Ep * 2:.1f} J"
                ]
                explication = f"Ep = m × g × h = {m} × 9,81 × {h} = {Ep:.1f} J"
            else:
                v = random.randint(5, 20)
                Ec = 0.5 * m * v**2
                question = f"Calculez l'énergie cinétique d'un objet de {m} kg se déplaçant à {v} m/s."
                correct = f"{Ec:.1f} J"
                distracteurs = [
                    f"{m * v:.1f} J",
                    f"{m * v**2:.1f} J",
                    f"{Ec / 2:.1f} J"
                ]
                explication = f"Ec = ½ × m × v² = ½ × {m} × {v}² = {Ec:.1f} J"

        elif type_question == "optique":
            f = round(random.uniform(5.0, 25.0), 1)
            p = round(random.uniform(8.0, 40.0), 1)
            
            if p != f:
                q = 1 / ((1/f) - (1/p))
                G = -q / p
                
                demande = random.choice(["position", "grandissement"])
                if demande == "position":
                    question = f"Un objet est placé à {p} cm d'une lentille convergente de distance focale f' = {f} cm. Où se forme l'image ?"
                    correct = f"{q:.1f} cm"
                    if q > 0:
                        correct += " (image réelle)"
                    else:
                        correct += " (image virtuelle)"
                    distracteurs = [
                        f"{f:.1f} cm",
                        f"{p * f / (p + f):.1f} cm",
                        f"{-q:.1f} cm"
                    ]
                    explication = f"1/f' = 1/p' - 1/p → 1/p' = 1/f' + 1/p = 1/{f} + 1/{p} → p' = {q:.1f} cm"
                else:
                    question = f"Un objet est placé à {p} cm d'une lentille convergente de focale {f} cm. Quel est le grandissement ?"
                    correct = f"{G:.2f}"
                    distracteurs = [
                        f"{-G:.2f}",
                        f"{abs(G)*2:.2f}",
                        f"{p/f:.2f}"
                    ]
                    explication = f"γ = p'/p = {q:.1f}/{p} = {G:.2f}"

        elif type_question == "electricite":
            circuit = random.choice(["serie", "parallele", "ohm"])
            
            if circuit == "serie":
                V = random.randint(5, 24)
                R1 = random.randint(10, 100)
                R2 = random.randint(10, 100)
                R_eq = R1 + R2
                I = V / R_eq
                V1 = R1 * I
                question = f"Deux résistances R₁ = {R1} Ω et R₂ = {R2} Ω sont branchées en série à une pile de {V} V. Quelle est la tension aux bornes de R₁ ?"
                correct = f"{V1:.2f} V"
                distracteurs = [
                    f"{V:.2f} V",
                    f"{V * R1 / R2:.2f} V",
                    f"{V / 2:.2f} V"
                ]
                explication = f"I = V / (R₁+R₂) = {V}/{R_eq} = {I:.3f} A ; V₁ = R₁ × I = {R1} × {I:.3f} = {V1:.2f} V"
                
            elif circuit == "parallele":
                V = random.randint(5, 24)
                R1 = random.randint(10, 100)
                R2 = random.randint(10, 100)
                R_eq = (R1 * R2) / (R1 + R2)
                I1 = V / R1
                I2 = V / R2
                I_total = I1 + I2
                question = f"Deux résistances R₁ = {R1} Ω et R₂ = {R2} Ω sont branchées en parallèle à une source de {V} V. Quel est le courant total ?"
                correct = f"{I_total:.3f} A"
                distracteurs = [
                    f"{V / (R1 + R2):.3f} A",
                    f"{V * (R1 + R2):.3f} A",
                    f"{I1:.3f} A"
                ]
                explication = f"I₁ = V/R₁ = {V}/{R1} = {I1:.3f} A ; I₂ = V/R₂ = {V}/{R2} = {I2:.3f} A ; I_total = I₁ + I₂ = {I_total:.3f} A"
                
            else:  # ohm
                V = random.randint(5, 30)
                I = round(random.uniform(0.1, 3.0), 2)
                R = V / I
                question = f"Une tension de {V} V produit un courant de {I} A dans un circuit. Quelle est la résistance ?"
                correct = f"{R:.2f} Ω"
                distracteurs = [
                    f"{V * I:.2f} Ω",
                    f"{I / V:.2f} Ω",
                    f"{R * 2:.2f} Ω"
                ]
                explication = f"Loi d'Ohm : R = V / I = {V} / {I} = {R:.2f} Ω"

        else:  # ondes ou autre
            f = random.randint(100, 1000)
            lambda_onde = random.randint(1, 10)
            v = f * lambda_onde
            question = f"Une onde a une fréquence de {f} Hz et une longueur d'onde de {lambda_onde} m. Quelle est sa célérité ?"
            correct = f"{v} m/s"
            distracteurs = [
                f"{f / lambda_onde} m/s",
                f"{lambda_onde / f} m/s",
                f"{v * 2} m/s"
            ]
            explication = f"v = λ × f = {lambda_onde} × {f} = {v} m/s"

        opts = [correct] + distracteurs[:3]
        random.shuffle(opts)
        
        return {
            "q": question,
            "opts": opts,
            "ans": correct,
            "difficulte": random.choice(["Facile", "Moyen", "Difficile"]),
            "matiere": "Physique",
            "explication": explication
        }

    @staticmethod
    def generer_biologie() -> Dict:
        """Génère une question de biologie basée sur le programme ARES"""
        themes = [
            # Cellule
            {
                "q": "Quelle structure différencie principalement une cellule végétale d'une cellule animale ?",
                "opts": ["Paroi cellulosique", "Mitochondries", "Noyau", "Ribosomes"],
                "ans": "Paroi cellulosique",
                "expl": "La paroi cellulosique est une structure rigide présente uniquement chez les cellules végétales, leur conférant forme et protection."
            },
            {
                "q": "Quel est le rôle principal des mitochondries ?",
                "opts": ["Respiration cellulaire", "Synthèse des protéines", "Photosynthèse", "Stockage des lipides"],
                "ans": "Respiration cellulaire",
                "expl": "Les mitochondries sont les centrales énergétiques de la cellule, siège de la respiration cellulaire produisant l'ATP."
            },
            {
                "q": "Dans quelle phase de la mitose les chromosomes se placent-ils à l'équateur de la cellule ?",
                "opts": ["Métaphase", "Prophase", "Anaphase", "Télophase"],
                "ans": "Métaphase",
                "expl": "En métaphase, les chromosomes s'alignent sur la plaque équatoriale, attachés aux fibres du fuseau mitotique."
            },
            # Génétique
            {
                "q": "Dans un croisement entre deux hétérozygotes (Aa × Aa), quelle est la probabilité d'obtenir un phénotype récessif ?",
                "opts": ["25%", "50%", "75%", "0%"],
                "ans": "25%",
                "expl": "Croisement Aa × Aa → 1/4 AA, 1/2 Aa, 1/4 aa. Le phénotype récessif (aa) apparaît dans 25% des cas."
            },
            {
                "q": "Qu'est-ce qu'un allèle ?",
                "opts": ["Une version alternative d'un gène", "Un chromosome entier", "Une protéine", "Une mutation"],
                "ans": "Une version alternative d'un gène",
                "expl": "Un allèle est une forme particulière d'un gène, occupant le même locus sur des chromosomes homologues."
            },
            {
                "q": "Une maladie récessive liée à l'X affecte principalement :",
                "opts": ["Les hommes", "Les femmes", "Les deux sexes également", "Uniquement les enfants"],
                "ans": "Les hommes",
                "expl": "Les hommes n'ayant qu'un chromosome X, un seul allèle muté suffit pour exprimer la maladie récessive."
            },
            # Évolution
            {
                "q": "Quel phénomène est illustré par la résistance des bactéries aux antibiotiques ?",
                "opts": ["Sélection naturelle", "Dérive génétique", "Mutation dirigée", "Équilibre de Hardy-Weinberg"],
                "ans": "Sélection naturelle",
                "expl": "Les antibiotiques exercent une pression sélective : les bactéries résistantes survivent et se reproduisent davantage."
            },
            {
                "q": "Selon la théorie de Lamarck, les caractères acquis :",
                "opts": ["Sont transmis à la descendance", "Ne sont pas héréditaires", "Sont le fruit du hasard", "Disparaissent toujours"],
                "ans": "Sont transmis à la descendance",
                "expl": "Lamarck postulait l'hérédité des caractères acquis, théorie aujourd'hui réfutée au profit de la sélection naturelle."
            },
            # Écologie
            {
                "q": "Qu'est-ce qu'une niche écologique ?",
                "opts": ["Le rôle et la position d'une espèce dans l'écosystème", "L'habitat physique de l'espèce", "La population totale", "Un microclimat"],
                "ans": "Le rôle et la position d'une espèce dans l'écosystème",
                "expl": "La niche écologique inclut les conditions de vie, les ressources utilisées et les interactions avec d'autres espèces."
            },
            {
                "q": "Quel niveau trophique occupe un producteur primaire ?",
                "opts": ["Premier niveau", "Deuxième niveau", "Troisième niveau", "Quatrième niveau"],
                "ans": "Premier niveau",
                "expl": "Les producteurs primaires (plantes, phytoplancton) sont à la base de la chaîne alimentaire, au premier niveau trophique."
            },
            {
                "q": "Lequel de ces cycles est un cycle biogéochimique ?",
                "opts": ["Cycle du carbone", "Cycle cellulaire", "Cycle cardiaque", "Cycle de vie"],
                "ans": "Cycle du carbone",
                "expl": "Les cycles biogéochimiques (carbone, azote, eau) décrivent la circulation des éléments entre vivant et non-vivant."
            },
            # Physiologie et autres
            {
                "q": "Quelle est la base azotée spécifique à l'ARN ?",
                "opts": ["Uracile", "Thymine", "Adénine", "Guanine"],
                "ans": "Uracile",
                "expl": "L'uracile (U) remplace la thymine (T) dans l'ARN et s'apparie avec l'adénine."
            },
            {
                "q": "Qu'est-ce qu'un virus ?",
                "opts": ["Un parasite intracellulaire obligatoire", "Une bactérie primitive", "Une cellule sans noyau", "Un champignon microscopique"],
                "ans": "Un parasite intracellulaire obligatoire",
                "expl": "Les virus ne peuvent se reproduire qu'en infectant une cellule hôte et en détournant sa machinerie cellulaire."
            }
        ]
        
        question_data = random.choice(themes)
        opts = list(question_data["opts"])
        random.shuffle(opts)
        
        return {
            "q": question_data["q"],
            "opts": opts,
            "ans": question_data["ans"],
            "difficulte": random.choice(["Facile", "Moyen"]),
            "matiere": "Biologie",
            "explication": question_data["expl"]
        }

    @staticmethod
    def generer_mathematiques() -> Dict:
        """Génère une question de mathématiques aléatoire"""
        type_question = random.choice([
            "algebre", "geometrie", "trigonometrie", "analyse", "statistiques"
        ])
        
        if type_question == "algebre":
            a = random.randint(1, 5)
            b = random.randint(-8, 8)
            c = random.randint(-15, 15)
            
            if b**2 - 4*a*c >= 0:
                delta = b**2 - 4*a*c
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                
                question = f"Résolvez l'équation : {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0. Quelle est la plus grande solution ?"
                correct = f"{max(x1, x2):.2f}"
                distracteurs = [
                    f"{min(x1, x2):.2f}",
                    f"{a * max(x1, x2):.2f}",
                    f"{-max(x1, x2):.2f}"
                ]
                explication = f"Δ = {b}² - 4×{a}×{c} = {delta}. x = (-{b} ± √{delta}) / (2×{a}) → x₁ = {x1:.2f}, x₂ = {x2:.2f}"
            else:
                question = f"Résolvez l'équation : {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0."
                correct = "Aucune solution réelle"
                distracteurs = ["0", "1", "-1"]
                explication = f"Δ = {b}² - 4×{a}×{c} < 0, donc pas de solution réelle."
                
        elif type_question == "geometrie":
            type_geo = random.choice(["pythagore", "droite", "vecteur"])
            
            if type_geo == "pythagore":
                a = random.randint(3, 8)
                b = random.randint(4, 10)
                c = math.sqrt(a**2 + b**2)
                question = f"Dans un triangle rectangle, les côtés de l'angle droit mesurent {a} cm et {b} cm. Quelle est la longueur de l'hypoténuse ?"
                correct = f"{c:.2f} cm"
                distracteurs = [
                    f"{a + b} cm",
                    f"{abs(a - b):.2f} cm",
                    f"{c * 1.2:.2f} cm"
                ]
                explication = f"Théorème de Pythagore : c² = a² + b² = {a}² + {b}² = {a**2 + b**2} → c = {c:.2f} cm"
                
            elif type_geo == "droite":
                x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
                x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
                while x2 == x1:
                    x2 = random.randint(-5, 5)
                pente = (y2 - y1) / (x2 - x1)
                question = f"Quelle est la pente de la droite passant par les points A({x1}; {y1}) et B({x2}; {y2}) ?"
                correct = f"{pente:.2f}"
                distracteurs = [
                    f"{(x2 - x1) / (y2 - y1):.2f}" if y2 != y1 else "0.00",
                    f"{-pente:.2f}",
                    f"{abs(pente * 2):.2f}"
                ]
                explication = f"Pente m = (y₂ - y₁) / (x₂ - x₁) = ({y2} - {y1}) / ({x2} - {x1}) = {pente:.2f}"
                
            else:  # vecteur
                x1, y1 = random.randint(1, 5), random.randint(1, 5)
                norme = math.sqrt(x1**2 + y1**2)
                question = f"Quelle est la norme du vecteur \u20D7u({x1}; {y1}) ?"
                correct = f"{norme:.2f}"
                distracteurs = [
                    f"{x1 + y1}",
                    f"{abs(x1 - y1):.2f}",
                    f"{norme * 1.5:.2f}"
                ]
                explication = f"||\u20D7u|| = √(x² + y²) = √({x1}² + {y1}²) = √{x1**2 + y1**2} = {norme:.2f}"

        elif type_question == "trigonometrie":
            angle = random.choice([0, 30, 45, 60, 90, 180, 270])
            func = random.choice(["sin", "cos", "tan"])
            
            valeurs = {
                ("sin", 0): "0", ("sin", 30): "1/2", ("sin", 45): "√2/2", ("sin", 60): "√3/2", ("sin", 90): "1",
                ("cos", 0): "1", ("cos", 30): "√3/2", ("cos", 45): "√2/2", ("cos", 60): "1/2", ("cos", 90): "0",
                ("tan", 0): "0", ("tan", 45): "1"
            }
            
            if (func, angle) in valeurs:
                correct = valeurs[(func, angle)]
                question = f"Quelle est la valeur de {func}({angle}°) ?"
                distracteurs = ["0", "1", "√3/2", "1/2"]
                distracteurs = [d for d in distracteurs if d != correct][:3]
                explication = f"{func}({angle}°) = {correct} (valeur remarquable du cercle trigonométrique)"
            else:
                question = f"Quelle est la valeur de {func}({angle}°) ?"
                correct = "Non définie" if (func == "tan" and angle == 90) else "0"
                distracteurs = ["0", "1", "Infini"]
                explication = f"tan(90°) n'est pas définie car cos(90°) = 0."

        elif type_question == "analyse":
            a = random.randint(2, 5)
            n = random.randint(2, 4)
            derivee = f"{a * n}x^{n-1}" if n-1 > 1 else f"{a * n}x" if n-1 == 1 else f"{a * n}"
            
            question = f"Quelle est la dérivée de f(x) = {a}x^{n} ?"
            correct = derivee
            distracteurs = [
                f"{a}x^{n-1}",
                f"{n}x^{a}",
                f"{a * n}x^{n}"
            ]
            explication = f"f'(x) = {a} × {n} × x^({n}-1) = {derivee}"
            
        else:  # statistiques
            serie = [random.randint(1, 20) for _ in range(5)]
            moyenne = sum(serie) / len(serie)
            variance = sum((x - moyenne)**2 for x in serie) / len(serie)
            ecart_type = math.sqrt(variance)
            
            question = f"Soit la série statistique : {', '.join(map(str, serie))}. Quelle est la moyenne ?"
            correct = f"{moyenne:.1f}"
            distracteurs = [
                f"{median(serie):.1f}",
                f"{max(serie)}",
                f"{moyenne * 1.2:.1f}"
            ]
            explication = f"Moyenne = ({'+'.join(map(str, serie))}) / {len(serie)} = {moyenne:.1f}"

        opts = [correct] + distracteurs[:3]
        random.shuffle(opts)
        
        return {
            "q": question,
            "opts": opts,
            "ans": correct,
            "difficulte": random.choice(["Facile", "Moyen", "Difficile"]),
            "matiere": "Mathématiques",
            "explication": explication
        }

def median(lst):
    """Calcule la médiane d'une liste"""
    n = len(lst)
    s = sorted(lst)
    return s[n//2] if n % 2 else (s[n//2 - 1] + s[n//2]) / 2

# --- INITIALISATION DE L'ÉTAT DE SESSION ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0
    st.session_state.current_idx = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.current_options = []
    st.session_state.answers_history = []
    st.session_state.show_explication = True

def demarrer_quiz(matiere: str, nb_questions: int):
    """Génère un nouveau quiz avec des questions aléatoires"""
    st.session_state.quiz_data = []
    generateur = GenerateurQuestions()
    
    for _ in range(nb_questions):
        if matiere == "Toutes les matières":
            matiere_alea = random.choice(["Chimie", "Physique", "Biologie", "Mathématiques"])
            if matiere_alea == "Chimie":
                q = generateur.generer_chimie()
            elif matiere_alea == "Physique":
                q = generateur.generer_physique()
            elif matiere_alea == "Biologie":
                q = generateur.generer_biologie()
            else:
                q = generateur.generer_mathematiques()
        else:
            if matiere == "Chimie":
                q = generateur.generer_chimie()
            elif matiere == "Physique":
                q = generateur.generer_physique()
            elif matiere == "Biologie":
                q = generateur.generer_biologie()
            else:
                q = generateur.generer_mathematiques()
        
        st.session_state.quiz_data.append(q)
    
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.submitted = False
    st.session_state.answers_history = []
    preparer_question()

def preparer_question():
    """Prépare les options de la question courante"""
    idx = st.session_state.current_idx
    if idx < len(st.session_state.quiz_data):
        opts = list(st.session_state.quiz_data[idx]['opts'])
        random.shuffle(opts)
        st.session_state.current_options = opts

def calculer_score_ares() -> float:
    """Calcule le score selon la méthode ARES (+1 bonne réponse, -1/3 erreur)"""
    score = 0.0
    for reponse in st.session_state.answers_history:
        if reponse['is_correct']:
            score += 1
        else:
            score -= 1/3
    return score

# --- INTERFACE PRINCIPALE ---
st.title("🧬 Matteo x M3.0 | Générateur ARES")
st.markdown("### Simulateur procédural basé sur le programme officiel de médecine (Belgique)")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration du Quiz")
    matiere_choisie = st.selectbox(
        "Matière",
        ["Toutes les matières", "Chimie", "Physique", "Biologie", "Mathématiques"]
    )
    nb_questions = st.slider("Nombre de questions", 5, 30, 10)
    
    st.markdown("---")
    st.markdown("### 💡 Système de notation")
    st.info("**+1 point** pour une réponse correcte\n\n**-1/3 point** pour une erreur\n\n(Conforme au système ARES)")
    
    st.markdown("---")
    if st.button("🚀 Générer un nouveau quiz", use_container_width=True, type="primary"):
        demarrer_quiz(matiere_choisie, nb_questions)
        st.rerun()

# Zone principale
if not st.session_state.quiz_data:
    st.info("👈 Sélectionnez une matière et cliquez sur **Générer un nouveau quiz** pour commencer !")
    
    st.markdown("---")
    st.markdown("### 📚 Programme couvert")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Chimie**")
        st.markdown("- États de la matière et gaz parfaits")
        st.markdown("- Molarité, fractions molaires et massiques")
        st.markdown("- Structure atomique et classification périodique")
        st.markdown("- Réactions chimiques et stœchiométrie")
        st.markdown("- Équilibre chimique")
        
        st.markdown("**Physique**")
        st.markdown("- Cinématique et dynamique")
        st.markdown("- Statique et équilibre")
        st.markdown("- Travail, énergie, puissance")
        st.markdown("- Ondes et optique géométrique")
        st.markdown("- Électricité et électromagnétisme")
    
    with col2:
        st.markdown("**Biologie**")
        st.markdown("- La cellule : unité fonctionnelle du vivant")
        st.markdown("- Génétique et hérédité")
        st.markdown("- Diversité, évolution, adaptabilité")
        st.markdown("- Écologie et écosystèmes")
        
        st.markdown("**Mathématiques**")
        st.markdown("- Algèbre et équations")
        st.markdown("- Géométrie et trigonométrie")
        st.markdown("- Analyse (dérivées, intégrales)")
        st.markdown("- Statistiques descriptives")

else:
    if st.session_state.finished:
        st.balloons()
        st.header("🏁 Quiz terminé !")
        
        score_final = calculer_score_ares()
        nb_total = len(st.session_state.quiz_data)
        nb_correct = sum(1 for r in st.session_state.answers_history if r['is_correct'])
        nb_incorrect = nb_total - nb_correct
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score ARES", f"{score_final:.2f} / {nb_total}")
        with col2:
            st.metric("Réponses correctes", f"{nb_correct} / {nb_total}")
        with col3:
            pourcentage = (nb_correct / nb_total) * 100 if nb_total > 0 else 0
            st.metric("Pourcentage", f"{pourcentage:.1f}%")
        
        st.markdown("---")
        
        # Message de feedback
        if pourcentage >= 80:
            st.success("🌟 Excellent travail ! Vous maîtrisez très bien le sujet !")
        elif pourcentage >= 60:
            st.info("👍 Bon travail ! Continuez à vous entraîner pour progresser.")
        elif pourcentage >= 40:
            st.warning("📚 Pas mal. Révisez les notions qui vous ont posé problème.")
        else:
            st.error("💪 Ne vous découragez pas ! L'entraînement est la clé du succès.")
        
        if st.button("🔄 Retour à l'accueil", use_container_width=True):
            st.session_state.quiz_data = []
            st.rerun()
            
    else:
        idx = st.session_state.current_idx
        q = st.session_state.quiz_data[idx]
        
        # En-tête avec informations
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**📖 {q['matiere']}** | Difficulté : {q['difficulte']}")
        with col2:
            score_actuel = calculer_score_ares()
            st.markdown(f"**📊 Score : {score_actuel:.2f}**")
        with col3:
            if st.button("🏠 Accueil", use_container_width=True):
                st.session_state.quiz_data = []
                st.rerun()
        
        # Barre de progression
        st.progress((idx) / len(st.session_state.quiz_data))
        st.markdown(f"### Question {idx + 1} sur {len(st.session_state.quiz_data)}")
        
        # Question
        st.markdown(f"**{q['q']}**")
        
        # Formulaire de réponse
        with st.form(key=f"form_{idx}"):
            reponse_utilisateur = st.radio(
                "✨ Sélectionnez votre réponse :",
                st.session_state.current_options,
                key=f"radio_{idx}"
            )
            soumettre = st.form_submit_button("✅ Valider la réponse", use_container_width=True)
        
        if soumettre and not st.session_state.submitted:
            st.session_state.submitted = True
            est_correct = (reponse_utilisateur == q['ans'])
            
            # Enregistrer la réponse
            st.session_state.answers_history.append({
                'question': q['q'],
                'reponse_utilisateur': reponse_utilisateur,
                'reponse_correcte': q['ans'],
                'is_correct': est_correct
            })
            
            if est_correct:
                st.session_state.score += 1
                st.success(f"✅ Correct ! +1 point")
            else:
                st.error(f"❌ Incorrect. La réponse était : **{q['ans']}** (-1/3 point)")
            
            # Afficher l'explication
            if 'explication' in q:
                st.markdown("---")
                st.markdown(f"<div class='explication-box'><strong>💡 Explication :</strong><br>{q['explication']}</div>", 
                          unsafe_allow_html=True)
        
        # Navigation
        if st.session_state.submitted:
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("⬅️ Précédent", use_container_width=True) and idx > 0:
                    st.session_state.current_idx -= 1
                    st.session_state.submitted = False
                    preparer_question()
                    st.rerun()
            with col2:
                texte_bouton = "🏁 Terminer" if idx + 1 >= len(st.session_state.quiz_data) else "➡️ Question suivante"
                if st.button(texte_bouton, use_container_width=True, type="primary"):
                    if idx + 1 < len(st.session_state.quiz_data):
                        st.session_state.current_idx += 1
                        st.session_state.submitted = False
                        preparer_question()
                        st.rerun()
                    else:
                        st.session_state.finished = True
                        st.rerun()
