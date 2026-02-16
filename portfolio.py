import streamlit as st
from datetime import datetime
import base64
import os

# Fonction pour encoder une image en base64
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None


# Fonction pour lire un fichier binaire (ex: CV.pdf)
def get_file_bytes(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


# Recherche automatique d'un fichier CV dans le dossier du script
def find_cv_file():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()

    # Noms candidats fréquents et heuristique
    candidates = [
        "CV_NJIPANG_Eraste.pdf",
        "CV_NJIPANG_Eraste.PDF",
        "CV_Eraste2.pdf",
        "CV_Eraste.pdf",
        "CV.pdf",
        "MonCV.pdf",
    ]

    for c in candidates:
        p = os.path.join(base_dir, c)
        if os.path.isfile(p):
            return p

    # Heuristique: tout PDF contenant 'cv' ou 'eraste' ou 'njipang'
    for f in os.listdir(base_dir):
        lf = f.lower()
        if lf.endswith('.pdf') and ("cv" in lf or "eraste" in lf or "njipang" in lf or "curriculum" in lf):
            return os.path.join(base_dir, f)

    return None

# Configuration de la page
st.set_page_config(
        page_title="NJIPANG DONGMO Eraste — Portfolio Développeur IA | Python, Machine Learning",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"  # mobile friendly
)

# SEO / Meta tags (aide basique pour le partage et l'indexation)
st.markdown("""
<head>
    <meta name="description" content="Portfolio de NJIPANG DONGMO Eraste — Développeur d'applications IA, Machine Learning et Python. Découvrez mes projets, compétences et coordonnées.">
    <meta name="keywords" content="NJIPANG DONGMO Eraste, développeur IA, machine learning, python, portfolio, data science">
    <meta name="author" content="NJIPANG DONGMO Eraste">
    <meta property="og:title" content="NJIPANG DONGMO Eraste — Portfolio Développeur IA">
    <meta property="og:description" content="Développeur IA et Machine Learning — projets en Python, TensorFlow, Keras. Découvrez mon travail et contactez-moi.">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://raw.githubusercontent.com/your-username/your-repo/main/preview.png">
    <meta name="robots" content="index, follow">
</head>
""", unsafe_allow_html=True)
# Initialiser le state pour le thème
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Fonction pour basculer le thème
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Définition des couleurs selon le mode
if st.session_state.dark_mode:
    # Mode sombre
    bg_main = "#0f1419"
    bg_card = "#1a1f2e"
    text_primary = "#e4e6eb"
    text_secondary = "#b0b3b8"
    primary_color = "#3b82f6"
    secondary_color = "#10b981"
    sidebar_bg = "linear-gradient(180deg, #1a2332 0%, #0d1117 100%)"
    border_color = "#2d3748"
    hover_bg = "#252d3d"
else:
    # Mode clair
    bg_main = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    bg_card = "#ffffff"
    text_primary = "#000205"
    text_secondary = "#0F1933"
    primary_color = "#030409"
    secondary_color = "#10AC84"
    sidebar_bg = "linear-gradient(180deg, #97d7c1ff 0%, #02271aff 100%)"
    border_color = "#e2e8f0"
    hover_bg = "#f7fafc"

# CSS personnalisé avec gestion du thème
def load_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    body, .stApp {{
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }}

    /* Reset et variables */
    * {{
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }}
    
    /* Conteneur principal */
    .main {{
        background: {bg_main};
        background-attachment: fixed;
    }}
    
    /* Override Streamlit defaults */
    .stApp {{
        background: {bg_main};
    }}
    
    /* Cartes de compétences */
    .skill-card {{
        background: {bg_card};
        color: {text_primary};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        border-left: 4px solid {primary_color};
        border: 1px solid {border_color};
    }}
    
    .skill-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        background: {hover_bg};
    }}
    
    .skill-card h4 {{
        color: {primary_color};
        margin: 0 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.35rem; /* réduit l'espacement entre logo et texte */
    }}
    .skill-logo {{
        width: 18px;  /* réduit la taille du logo */
        height: 18px; /* réduit la taille du logo */
        object-fit: contain;
        border-radius: 4px;
    }}
    
    .skill-card p {{
        color: {text_secondary};
    }}
    
    /* Carte de projet */
    .project-card {{
        background: {bg_card};
        color: {text_primary};
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        border: 1px solid {border_color};
    }}
    
    .project-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }}
    
    .project-card h3 {{
        color: {primary_color};
        margin-top: 0;
    }}
    
    .project-card p {{
        color: {text_secondary};
    }}
    
    /* Titre stylisé */
    .custom-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, {primary_color}, {secondary_color});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}
    
    /* Sous-titre */
    .subtitle {{
        font-size: 1.5rem;
        color: {text_primary};
        margin-bottom: 2rem;
        opacity: 0.9;
    }}
    
    /* Badge de technologie */
    .tech-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 600;
    }}
    
    /* Timeline */
    .timeline-item {{
        border-left: 3px solid {primary_color};
        padding-left: 1.5rem;
        margin-bottom: 2rem;
        position: relative;
        background: {bg_card};
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border: 1px solid {border_color};
    }}
    
    .timeline-item::before {{
        content: '';
        position: absolute;
        left: -8px;
        top: 1rem;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: {primary_color};
    }}
    
    .timeline-item h4 {{
        color: {primary_color};
        margin: 0 0 0.5rem 0;
    }}
    
    .timeline-item p {{
        color: {text_secondary};
        margin: 0.25rem 0;
    }}
    
    /* Section container */
    .section-container {{
        background: {bg_card};
        color: {text_primary};
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid {border_color};
    }}
    
    .section-container h2, .section-container h3, .section-container h4 {{
        color: {primary_color};
    }}
    
    .section-container p, .section-container li {{
        color: {text_secondary};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {sidebar_bg};
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Bouton de thème */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: {bg_card};
        border: 2px solid {primary_color};
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        font-weight: 600;
        color: {text_primary};
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* Streamlit elements styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        border-radius: 10px;
        border: 2px solid {border_color};
        background-color: {bg_card};
        color: {text_primary};
        transition: border 0.3s ease;
    }}
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {primary_color};
    }}
    
    /* Boutons de thème dans la sidebar */
    [data-testid="stSidebar"] .stButton>button {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    [data-testid="stSidebar"] .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: {primary_color};
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {text_secondary};
    }}
    
    /* Markdown dans les cartes */
    .element-container {{
        color: {text_primary};
    }}
    
    /* Boutons Streamlit */
    .stButton>button {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color});
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }}

    /* Cible spécifiquement le bouton de téléchargement pour garantir contraste */
    .stDownloadButton>button, [data-testid="stDownloadButton"] button, .stButton[data-baseweb="button"]>button {{
        background: linear-gradient(135deg, {primary_color}, {secondary_color}) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
        text-shadow: none !important;
    }}
    
    /* Links */
    a {{
        color: {primary_color};
    }}
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label {{
        color: white !important;
    }}
    
    /* Profile image */
    .profile-img {{
        width: 290px;
        height: 300px;
        border-radius: 50%;
        overflow: hidden;
        margin: auto;
    }}
    
    .profile-img img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    
        /* Responsive design */
    @media (max-width: 768px) {{
        .custom-title {{
            font-size: 2rem;
            text-align: center;
        }}
        .subtitle {{
            font-size: 1rem;
            text-align: center;
        }}
        .section-container {{
            padding: 1.2rem;
        }}
        .profile-img {{
            width: 170px !important;
            height: 170px !important;
        }}
        p, li {{
            font-size: .95rem;
            line-height: 1.6;
        }}
        .skill-card {{
            padding: 1rem;
        }}
        .project-card {{
            padding: 1.5rem;
        }}
        .timeline-item {{
            padding-left: 1rem;
        }}
        .skill-logo {{
            width: 16px;  /* encore plus petit sur mobile */
            height: 16px;
        }}
        }}
    </style>
    """, unsafe_allow_html=True)

# Chargement du CSS
load_css()

# Sidebar Navigation avec bouton de thème
def sidebar_navigation():
    st.sidebar.markdown("---")
    
    # Bouton de thème dans la sidebar
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    theme_text = "Mode Sombre" if not st.session_state.dark_mode else "Mode Clair"
    
    if st.sidebar.button(f"{theme_icon} {theme_text}", use_container_width=True, key="theme_button"):
        toggle_theme()
        st.rerun()
    
    st.sidebar.markdown("---")
    
    pages = {
        "🏠 Accueil": "home",
        "👤 À propos": "about",
        "⚡ Compétences": "skills",
        "🚀 Projets": "projects",
        "📚 Parcours": "experience",
        "📬 Contact": "contact"
    }
    
    selected = st.sidebar.radio("Navigation", list(pages.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Liens rapides")
    st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com)")
    st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eraste-njipang-162162266/)")
    
    return pages[selected]

# Page Accueil
def home_page():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        image_base64 = get_image_base64("My_Photo.jpeg")
        if image_base64:
            st.markdown(f"""
                <div class="profile-img">
                    <img src="data:image/jpeg;base64,{image_base64}">
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Image non trouvée")
    
    with col2:
        st.markdown('<h1 class="custom-title">NJIPANG DONGMO Eraste</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Développeur Python & Intelligence Artificielle</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="color: {text_secondary};">
        
        ### 🎯 Transformer les données en solutions intelligentes
        
        Jeune professionnel passionné par l'Intelligence Artificielle et les technologies émergentes, je combine une solide formation en génie logiciel et une expertise pratique en Machine Learning avec TensorFlow/Keras.
        
        </div>
        """, unsafe_allow_html=True)
        
        # Social links under title
        soc_col1, soc_col2, soc_col3 = st.columns([1,1,2])
        with soc_col1:
            st.markdown('<a href="https://github.com/njipangeraste"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" width="150" height="auto" alt="GitHub"></a>', unsafe_allow_html=True)
        with soc_col2:
            st.markdown('<a href="https://www.linkedin.com/in/eraste-njipang-162162266/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="150" height="auto" alt="LinkedIn"></a>', unsafe_allow_html=True)
        with soc_col3:
            st.markdown("<div style='height:9px'></div>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn2:
            # Cherche automatiquement un fichier CV local
            cv_path = find_cv_file()
            if cv_path:
                cv_bytes = get_file_bytes(cv_path)
                if cv_bytes:
                    st.download_button(
                        label="📄 Télécharger CV",
                        data=cv_bytes,
                        file_name=os.path.basename(cv_path),
                        mime="application/pdf",
                        use_container_width=True,
                    )
                else:
                    st.error("Le fichier CV a été trouvé mais impossible de le lire.")
            else:
                # Fallback : montrer un lien externe si le fichier local est absent
                st.info("CV local non trouvé. Vous pouvez télécharger le CV depuis un lien externe.")
                st.markdown("[Voir/ Télécharger mon CV en ligne](https://example.com/cv.pdf)")
    
    st.markdown("---")
    
    # Statistiques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="skill-card">', unsafe_allow_html=True)
        st.metric("Projets réalisés", "2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="skill-card">', unsafe_allow_html=True)
        st.metric("Technologies", "20+")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="skill-card">', unsafe_allow_html=True)
        st.metric("Années d'expérience", "2+")
        st.markdown('</div>', unsafe_allow_html=True)
    

# Page À propos
def about_page():
    st.markdown('<div class="section-container fade-in">', unsafe_allow_html=True)
    st.markdown("## 👤 À propos de moi")
    
    st.markdown("""
    ### Qui suis-je ?
    
    Jeune professionnel passionné par l'Intelligence Artificielle et les technologies émergentes, je combine une solide formation en génie logiciel et une expertise pratique en Machine Learning avec TensorFlow/Keras. Mon parcours m'a permis de développer une application hybride (Web/Mobile) intégrant IA appliquée à la reconnaissance d'images, la classification et la prédiction pour la soutenance de mon rapport de stage. Innovant et déterminé, je vise à contribuer à la recherche et au développement de systèmes intelligents exploitant les données pour résoudre des problématiques concrètes.
    
    ### 🎯 Ma vision
    
    Je crois fermement que l'intelligence artificielle et le développement logiciel moderne peuvent 
    révolutionner notre façon de travailler et d'interagir avec la technologie. Mon objectif est de 
    rendre ces technologies accessibles et impactantes pour tous.
    
    ### 💡 Ce qui me motive
    
    - **Innovation continue** : Rester à la pointe des technologies émergentes
    - **Impact réel** : Créer des solutions qui résolvent de vrais problèmes
    - **Excellence technique** : Produire du code propre, maintenable et performant
    - **Apprentissage** : Chaque projet est une opportunité d'apprendre et de grandir
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page Compétences
def skills_page():
    st.markdown('<div class="section-container fade-in">', unsafe_allow_html=True)
    st.markdown("## ⚡ Mes Compétences")
    
    skills_data = {
        "💻 Langages de Programmation": [
            ("Java", "Intermédiaire", "☕"),
            ("PHP", "Intermédiaire", "🐘"),
            ("JavaScript", "Intermédiaire", "⚡"),
            ("Python", "Avancé", "🐍")
        ],
        "🗄️ Bases de Données": [
            ("MySQL", "Avancé", "🗄️"),
            ("Oracle", "Avancé", "🗄️")
        ],
        "🚀 Frameworks & Bibliothèques": [
            ("React Native", "Intermédiaire", "📱"),
            ("Node.js", "Intermédiaire", "⚡"),
            ("Express.js", "Intermédiaire", "⚡"),
            ("Laravel", "Intermédiaire", "🐘")
        ],
        "🤖 Intelligence Artificielle": [
            ("TensorFlow", "Avancé", "🧠"),
            ("Keras", "Avancé", "🧠"),
            ("Scikit-learn", "Avancé", "📈"),
            ("Pandas", "Avancé", "🐼"),
            ("Numpy", "Avancé", "🔢")
        ],
        "🛠️ Outils & Environnements": [
            ("Git/Github", "Avancé", "🔧"),
            ("Pycharm", "Avancé", "🛠️"),
            ("VS Code", "Avancé", "🛠️"),
            ("IntelliJ", "Avancé", "🛠️"),
            ("Oracle Sql Developer", "Avancé", "🛠️"),
            ("Oracle XE", "Avancé", "🛠️"),
            ("Oracle Sql Developer Data Modeler", "Avancé", "🛠️")
        ],
        "🌟 Compétences Transversales": [
            ("Résolution de problèmes", "Expert", "🧩"),
            ("Esprit d'analyse et de synthèse", "Expert", "🔍"),
            ("Travail en équipe", "Expert", "👥"),
            ("Adaptabilité et curiosité des nouvelles technologies", "Expert", "🚀")
        ]
    }

    skill_logos = {
        "Java": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
        "PHP": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg",
        "JavaScript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
        "Python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "MySQL": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
        "Oracle": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/oracle/oracle-original.svg",
        "React Native": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
        "Node.js": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg",
        "Express.js": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/express/express-original.svg",
        "Laravel": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-original.svg",
        "TensorFlow": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg",
        "Keras": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/keras/keras-original.svg",
        "Scikit-learn": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/scikitlearn/scikitlearn-original.svg",
        "Pandas": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg",
        "Numpy": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg",
        "Git/Github": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
        "Pycharm": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pycharm/pycharm-original.svg",
        "VS Code": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg",
        "IntelliJ": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/intellij/intellij-original.svg",
        "Oracle Sql Developer": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/oracle/oracle-original.svg",
        "Oracle XE": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/oracle/oracle-original.svg",
        "Oracle Sql Developer Data Modeler": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/oracle/oracle-original.svg",
    }
    
    for category, skills in skills_data.items():
        st.markdown(f"### {category}")
        cols = st.columns(2)
        
        for idx, (skill, description, icon) in enumerate(skills):
            with cols[idx % 2]:
                logo_url = skill_logos.get(skill)
                label_html = (
                    f'<img class="skill-logo" src="{logo_url}" alt="{skill} logo"> {skill}'
                    if logo_url else f'{icon} {skill}'
                )
                st.markdown(f"""
                <div class="skill-card">
                    <h4>{label_html}</h4>
                    <p style="margin: 0;">{description}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page Projets
def projects_page():
    st.markdown('<div class="section-container fade-in">', unsafe_allow_html=True)
    st.markdown("## 🚀 Mes Projets")
    
    projects = [
        {
            "title": "🤖 Application Hybride IA pour Reconnaissance d'Images",
            "description": "Développement d'une application hybride (Web/Mobile) intégrant IA appliquée à la reconnaissance d'images, la classification et la prédiction pour la soutenance de mon rapport de stage.",
            "tech": ["Python", "TensorFlow", "Keras", "React Native"],
            "github": "https://github.com",
            "demo": "https://demo-ia-reconnaissance.streamlit.app"
        },
        {
            "title": "📱 Application Desktop",
            "description": "Divertissez-vous avec un jeu de balle captivant developpe en JAVA ",
            "tech": ["Java", "Java swing", "Java awt"],
            "github": "https://github.com/njipangeraste/Jeu-de-balle-en-JAVA",
            "demo": "https://demo-mobile-fagiciel.example.com"
        },
        {
            "title": "🌐 Application Web avec React.js et Next.js",
            "description": "Développement d'une application web chez ISDEV Experts avec React.js et Next.js, mise en place du SSR pour performances et SEO. Intégration d'API REST, interfaces responsives avec Tailwind CSS, déploiement sur Vercel, gestion Agile avec Jira et Slack.",
            "tech": ["React.js", "Next.js", "Tailwind CSS", "Node.js"],
            "github": "https://github.com",
            "demo": "https://demo-web-isdev.vercel.app"
        }
    ]
    
    for project in projects:
        st.markdown(f"""
        <div class="project-card">
            <h3>{project['title']}</h3>
            <p style="font-size: 1.1rem; margin: 1rem 0;">{project['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tech_badges = " ".join([f'<span class="tech-badge">{tech}</span>' for tech in project['tech']])
            st.markdown(tech_badges, unsafe_allow_html=True)
        
        with col2:
            col_gh, col_demo = st.columns(2)
            with col_gh:
                st.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]({project['github']})", unsafe_allow_html=True)
            with col_demo:
                st.link_button("🚀 Démo", project['demo'], use_container_width=True)
                
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page Expérience
def experience_page():
    st.markdown('<div class="section-container fade-in">', unsafe_allow_html=True)
    st.markdown("## 📚 Parcours Professionnel & Formation")
    
    st.markdown("### 💼 Expériences")
    
    experiences = [
        {
            "title": "Développeur Stagiaire - FAGICIEL",
            "period": "Juillet 2023 - Octobre 2023, Yaoundé",
            "description": "Participation complète au cycle de vie d'une application mobile innovante. Contribution à la conception fonctionnelle et à l'optimisation de l'interface utilisateur (UI). Développement de fonctionnalités backend avec PHP/Laravel. Intégration front-end et tests utilisateurs en environnement collaboratif Agile."
        },
        {
            "title": "Développeur Stagiaire - ISDEV Experts",
            "period": "Février 2025 - Mai 2025, Douala",
            "description": "Développement d'une application web avec React.js et Next.js, mise en place du rendu côté serveur (SSR). Intégration d'API REST et optimisation des échanges client-serveur. Conception d'interfaces responsives avec Tailwind CSS. Déploiement automatisé sur Vercel. Gestion du projet en mode Agile avec Jira."
        }
    ]
    
    for exp in experiences:
        st.markdown(f"""
        <div class="timeline-item">
            <h4>{exp['title']}</h4>
            <p style="font-weight: 600;">{exp['period']}</p>
            <p>{exp['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎓 Formation")
    
    formations = [
        {
            "title": "LICENCE PROFESSIONNELLE",
            "school": "Institut Universitaire du Golfe de Guinée",
            "period": "2024 – 2025, Douala",
            "description": ""
        },
        {
            "title": "BTS Génie Logiciel",
            "school": "Institut Universitaire du Golfe de Guinée",
            "period": "2023 – 2024, Douala",
            "description": ""
        },
        {
            "title": "Baccalaureat des Technologies Informatique (TI)",
            "school": "Lycee Classique de Bangangte",
            "period": "2020 – 2021, Bangangte",
            "description": ""
        }
    ]
    
    for formation in formations:
        st.markdown(f"""
        <div class="timeline-item">
            <h4>{formation['title']}</h4>
            <p style="font-weight: 600;">{formation['school']} | {formation['period']}</p>
            <p>{formation['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page Contact
def contact_page():
    st.markdown('<div class="section-container fade-in">', unsafe_allow_html=True)
    st.markdown("## 📬 Contactez-moi")
    
    st.markdown("""
    ### Discutons de votre projet !
    
    Que vous ayez un projet en tête, une opportunité professionnelle ou simplement envie d'échanger 
    sur la tech et l'IA, n'hésitez pas à me contacter. Je réponds généralement sous 24h.
    """)

    # ────────────────────────────────────────────────
    # Formulaire de contact
    # ────────────────────────────────────────────────
    with st.form(key="contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nom complet *", key="name")
            email = st.text_input("Email *", key="email")
        
        with col2:
            subject = st.text_input("Sujet *", key="subject")
            phone = st.text_input("Téléphone (optionnel)", key="phone")
        
        message = st.text_area("Votre message *", height=150, key="message")
        
        submit_button = st.form_submit_button("📧 Envoyer", use_container_width=True, type="primary")

    if submit_button:
        if not (name.strip() and email.strip() and subject.strip() and message.strip()):
            st.error("❌ Veuillez remplir tous les champs obligatoires")
        else:
            # ────────────────────────────────────────────────
            # Tentative d'envoi de l'email
            # ────────────────────────────────────────────────
            try:
                # Récupération des identifiants (priorité : secrets → variables d'environnement)
                sender_email = st.secrets.get("email", os.getenv("EMAIL_ADDRESS"))
                sender_password = st.secrets.get("password", os.getenv("EMAIL_PASSWORD"))
                receiver_email = "enjipang@gmail.com"  # ton adresse de réception

                if not sender_email or not sender_password:
                    raise ValueError("Identifiants email non configurés (secrets ou variables d'environnement manquantes)")

                # Construction du message
                msg = MIMEMultipart()
                msg["From"] = f"{name} <{email}>"
                msg["To"] = receiver_email
                msg["Subject"] = subject

                body = f"""
Nouveau message depuis ton portfolio !

Nom          : {name}
Email        : {email}
Téléphone    : {phone if phone else "non renseigné"}
Sujet        : {subject}

Message :
─────────────────────────────────
{message}
─────────────────────────────────
Envoyé le : {st.session_state.get('current_time', 'date inconnue')}
                """

                msg.attach(MIMEText(body, "plain", "utf-8"))

                # Connexion et envoi via Gmail SMTP
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)

                st.success("✅ Message envoyé avec succès ! Je te répondrai dès que possible.")
                st.balloons()

            except smtplib.SMTPAuthenticationError:
                st.error("❌ Erreur d'authentification Gmail. Vérifie ton mot de passe d'application (App Password).")
            except Exception as e:
                st.error(f"❌ Une erreur est survenue lors de l'envoi :\n{str(e)}")

    # ────────────────────────────────────────────────
    # Coordonnées alternatives
    # ────────────────────────────────────────────────
    st.markdown("---")
    
    st.markdown("### 🔗 Autres moyens de me contacter")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <h3>📧</h3>
            <h4>Email</h4>
            <p>enjipang@gmail.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <h3>💼</h3>
            <h4>LinkedIn</h4>
            <a href="https://www.linkedin.com/in/eraste-njipang-162162266/" target="_blank" style="color: #0a66c2; text-decoration: none;">
                Mon profil LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="skill-card" style="text-align: center;">
            <h3>📞</h3>
            <h4>Téléphone</h4>
            <p>237 673 13 30 12</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Navigation principale
def main():
    page = sidebar_navigation()
    
    if page == "home":
        home_page()
    elif page == "about":
        about_page()
    elif page == "skills":
        skills_page()
    elif page == "projects":
        projects_page()
    elif page == "experience":
        experience_page()
    elif page == "contact":
        contact_page()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {text_secondary}; padding: 2rem;">
        <p>© 2024 NJIPANG DONGMO Eraste | Développeur Python & IA</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()