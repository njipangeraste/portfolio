import streamlit as st
import base64
import os
import re
import urllib.parse
import requests

# ──────────────────────────────────────────────
# CONFIG PAGE
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="NJIPANG DONGMO Eraste — Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def get_image_base64(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def get_file_bytes(path: str) -> bytes | None:
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


def find_cv_file() -> str | None:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()
    candidates = [
        "CV_NJIPANG_Eraste.pdf", "CV_NJIPANG_Eraste.PDF",
        "CV_Eraste2.pdf", "CV_Eraste.pdf", "CV.pdf", "MonCV.pdf",
    ]
    for c in candidates:
        p = os.path.join(base_dir, c)
        if os.path.isfile(p):
            return p
    for f in os.listdir(base_dir):
        lf = f.lower()
        if lf.endswith(".pdf") and any(k in lf for k in ("cv", "eraste", "njipang", "curriculum")):
            return os.path.join(base_dir, f)
    return None


# ──────────────────────────────────────────────
# CSS GLOBAL
# ──────────────────────────────────────────────
def inject_css():
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
            st.html(f"<style>{css}</style>")
    except FileNotFoundError:
        st.error("style.css non trouvé.")


# ──────────────────────────────────────────────
# NAVIGATION (state)
# ──────────────────────────────────────────────
PAGES = {
    "🏠 Accueil":      "home",
    "👤 À propos":     "about",
    "⚡ Compétences":  "skills",
    "🚀 Projets":      "projects",
    "📚 Parcours":     "experience",
    "📬 Contact":      "contact",
}

if "page" not in st.session_state:
    st.session_state.page = "home"


# ──────────────────────────────────────────────
# RENDER NAV
# ──────────────────────────────────────────────
def render_nav():
    page = st.session_state.page
    links_html = ""
    for label, key in PAGES.items():
        active = "active" if key == page else ""
        short = label.split(" ", 1)[1]
        links_html += f'<a class="{active}" href="?page={key}" target="_self">{short}</a>'

    st.html(f"""<nav class="pf-nav">
<div class="pf-logo">NJIPANG <em>ERASTE</em></div>
<div class="pf-nav-links">{links_html}</div>
<div class="pf-avail"><div class="pf-dot"></div>Disponible pour projets</div>
</nav>""")


# ──────────────────────────────────────────────
# READ QUERY PARAM
# ──────────────────────────────────────────────
qp = st.query_params.get("page", None)
if qp and qp in PAGES.values():
    st.session_state.page = qp


# ──────────────────────────────────────────────
# CSS + NAV
# ──────────────────────────────────────────────
inject_css()
render_nav()

current = st.session_state.page


# ══════════════════════════════════════════════
# PAGE : HOME
# ══════════════════════════════════════════════
if current == "home":
    img_b64 = get_image_base64("My_Photo.jpeg")
    photo_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else ""
    
    photo_html = (
        f"""<input type="checkbox" id="lightbox-toggle">
<label for="lightbox-toggle" class="photo-trigger">
<div class="profile-circle"><img src="{photo_src}"></div>
</label>
<label for="lightbox-toggle" class="photo-lightbox">
<img src="{photo_src}" class="lightbox-content">
</label>"""
        if img_b64
        else '<div class="profile-placeholder">NE</div>'
    )

    st.html(f"""<div class="pf-section active">
<div class="hero">
<div class="hero-left">
<div class="hero-tag">Basé à Douala, Cameroun</div>
<h1 class="hero-name">NJIPANG<br>DONGMO<br><em>Eraste</em></h1>
<p class="hero-desc">
Développeur spécialisé en <strong>Intelligence Artificielle</strong> & <strong>Python</strong>. 
Je conçois des solutions innovantes en transformant les données en outils décisionnels performants.
</p>
<div class="hero-ctas">
<a class="btn-primary" href="?page=projects" target="_self">Découvrir mes projets</a>
<a class="btn-outline" href="?page=contact" target="_self">Me contacter</a>
</div>
</div>
<div class="hero-right">
<div class="hero-card">
{photo_html}
<div class="hero-stats">
<div class="hero-stat">
<div class="hero-stat-num">3+</div>
<div class="hero-stat-lbl">Projets clés</div>
</div>
<div class="hero-stat">
<div class="hero-stat-num">2</div>
<div class="hero-stat-lbl">Stages Pro</div>
</div>
<div class="hero-stat">
<div class="hero-stat-num">2025</div>
<div class="hero-stat-lbl">Diplômé LP GL</div>
</div>
<div class="hero-stat">
<div class="hero-stat-num">AI</div>
<div class="hero-stat-lbl">Spécialisation</div>
</div>
</div>
<div class="hero-links">
<a href="https://github.com/njipangeraste" target="_blank" class="hero-link-btn">GitHub</a>
<a href="https://www.linkedin.com/in/eraste-njipang-162162266/" target="_blank" class="hero-link-btn">LinkedIn</a>
</div>
</div>
</div>
</div>
</div>""")

    # ── CV download ───────────────────────────────────────────────────────────
    cv_path  = find_cv_file()
    cv_bytes = get_file_bytes(cv_path) if cv_path else None
    cv_name  = os.path.basename(cv_path) if cv_path else "CV_NJIPANG_Eraste.pdf"

    col_dl, col_up, _ = st.columns([1, 1.4, 2])

    with col_dl:
        if cv_bytes:
            st.download_button(
                label="📄 Télécharger mon CV",
                data=cv_bytes,
                file_name=cv_name,
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.markdown(
                '<p style="font-size:13px;color:#6B7280;margin-top:8px;">'
                '📄 CV non trouvé dans le dossier</p>',
                unsafe_allow_html=True,
            )

    with col_up:
        if not cv_bytes:
            # Permet à l'auteur d'uploader son CV directement depuis l'interface
            uploaded = st.file_uploader(
                "Déposez votre CV ici",
                type=["pdf"],
                label_visibility="collapsed",
                help="Glissez-déposez votre CV PDF pour activer le bouton de téléchargement",
            )
            if uploaded:
                st.download_button(
                    label="📄 Télécharger le CV déposé",
                    data=uploaded.getvalue(),
                    file_name=uploaded.name,
                    mime="application/pdf",
                    use_container_width=True,
                )

    st.empty()


# ══════════════════════════════════════════════
# PAGE : ABOUT
# ══════════════════════════════════════════════
elif current == "about":
    st.html("""<div class="pf-section active">
<div class="section-inner">
<span class="eyebrow">Mon Profil</span>
<h2 class="section-title">Passionné par l'innovation technologique</h2>
<div class="about-grid">
<div class="about-block about-full">
<div class="about-block-label">Mon Parcours</div>
<p>
Je suis un développeur passionné par l'<strong>Intelligence Artificielle</strong> et les systèmes complexes. 
Ma formation en <strong>Génie Logiciel</strong> m'a permis d'acquérir une base solide en conception d'architectures robustes, 
que j'applique aujourd'hui au domaine du <strong>Machine Learning</strong>.
</p>
<br>
<p>
Mon expertise pratique se concentre sur l'intégration de modèles de Deep Learning (TensorFlow/Keras) au sein d'applications hybrides 
concrètes, alliant performance backend et expérience utilisateur fluide.
</p>
</div>
<div class="about-block">
<div class="about-block-label">Mes Objectifs</div>
<ul>
<li>Conception de systèmes IA scalables</li>
<li>Optimisation de processus via l'analyse de données</li>
<li>Veille constante sur les modèles LLM et Computer Vision</li>
<li>Développement de code propre (Clean Code) et maintenable</li>
</ul>
</div>
<div class="about-block">
<div class="about-block-label">Compétences Linguistiques</div>
<div class="lang-row">
<span class="lang-name">Français</span>
<span class="lang-level">Natif / Bilingue</span>
</div>
<div class="lang-row">
<span class="lang-name">Anglais</span>
<span class="lang-level">Débutant (A1/A2)</span>
</div>
</div>
</div>
</div>
</div>""")


# ══════════════════════════════════════════════
# PAGE : SKILLS
# ══════════════════════════════════════════════
elif current == "skills":
    def skill_card(logo_url, name, progress):
        return f"""<div class="skill-row">
<div class="skill-header">
<div class="skill-icon"><img src="{logo_url}" alt="{name}"></div>
<div class="skill-name">{name}</div>
</div>
<div class="skill-progress-bg">
<div class="skill-progress-bar" style="width: {progress}%"></div>
</div>
</div>"""

    ia_cards = "".join([
        skill_card("https://cdn.simpleicons.org/tensorflow/FF6F00", "TensorFlow", 85),
        skill_card("https://cdn.simpleicons.org/keras/D00000", "Keras", 80),
        skill_card("https://cdn.simpleicons.org/scikitlearn/F7931E", "Scikit-Learn", 85),
        skill_card("https://cdn.simpleicons.org/pandas/150458", "Pandas / NumPy", 90),
    ])
    lang_cards = "".join([
        skill_card("https://cdn.simpleicons.org/python/3776AB", "Python (Advanced)", 95),
        skill_card("https://cdn.simpleicons.org/openjdk/007396", "Java / OOP", 75),
        skill_card("https://cdn.simpleicons.org/php/777BB4", "PHP", 70),
        skill_card("https://cdn.simpleicons.org/javascript/F7DF1E", "JavaScript / ES6", 70),
    ])
    fw_cards = "".join([
        skill_card("https://cdn.simpleicons.org/nextdotjs/000000", "Next.js / React", 80),
        skill_card("https://cdn.simpleicons.org/tailwindcss/06B6D4", "Tailwind CSS", 90),
        skill_card("https://cdn.simpleicons.org/fastapi/05998B", "FastAPI / Node", 75),
        skill_card("https://cdn.simpleicons.org/laravel/FF2D20", "Laravel", 70),
    ])
    db_cards = "".join([
        skill_card("https://cdn.simpleicons.org/mysql/4479A1", "MySQL / PostgreSQL", 85),
        skill_card("https://cdn.simpleicons.org/git/F05032", "Git / CI-CD", 80),
        skill_card("https://cdn.simpleicons.org/docker/2496ED", "Docker / Linux", 60),
        skill_card("https://cdn.simpleicons.org/jira/0052CC", "Agile (Jira/Slack)", 85),
    ])

    st.html(f"""<div class="pf-section active">
<div class="section-inner">
<span class="eyebrow">Expertise</span>
<h2 class="section-title">Compétences Techniques</h2>
<div class="skills-cat-title">Intelligence Artificielle & Data</div>
<div class="skills-grid">{ia_cards}</div>
<div class="skills-cat-title">Langages de Programmation</div>
<div class="skills-grid">{lang_cards}</div>
<div class="skills-cat-title">Frameworks & Modern Web</div>
<div class="skills-grid">{fw_cards}</div>
<div class="skills-cat-title">Bases de Données & Outils</div>
<div class="skills-grid">{db_cards}</div>
</div>
</div>""")


# ══════════════════════════════════════════════
# PAGE : PROJECTS
# ══════════════════════════════════════════════
elif current == "projects":
    def project_card(num, category, title, desc, tags, github_url, demo_url=None):
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
        demo_btn  = f'<a class="btn-outline" href="{demo_url}" target="_blank">Démo Live</a>' if demo_url else ""
        return f"""<div class="project-item">
<div class="project-content">
<div class="project-num">{num} — {category}</div>
<h3 class="project-title">{title}</h3>
<p class="project-desc">{desc}</p>
<div class="project-tags">{tags_html}</div>
<div style="display: flex; gap: 10px;">
<a class="btn-primary" href="{github_url}" target="_blank">Voir Code</a>
{demo_btn}
</div>
</div>
<div class="project-image-placeholder">
{title}
</div>
</div>"""

    p1 = project_card(
        "01", "Intelligence Artificielle",
        "DeepVision — Reconnaissance d'images",
        "Solution hybride (Web & Mobile) exploitant le Deep Learning pour la classification d'images en temps réel. Intègre TensorFlow et Keras pour des prédictions haute précision.",
        ["Python", "TensorFlow", "React Native", "FastAPI"],
        "https://github.com/njipangeraste",
    )
    p2 = project_card(
        "02", "Desktop App",
        "Swing Ball Game",
        "Jeu d'arcade performant développé en Java. Gestion avancée des collisions, moteur physique personnalisé et interface fluide avec Swing/AWT.",
        ["Java", "Swing", "AWT", "OOP"],
        "https://github.com/njipangeraste/Jeu-de-balle-en-JAVA",
    )
    p3 = project_card(
        "03", "Fullstack Web",
        "ISDEV Experts Portal",
        "Plateforme web d'entreprise avec Server Side Rendering (SSR). Optimisation SEO, interfaces ultra-réactives avec Tailwind CSS et déploiement continu sur Vercel.",
        ["Next.js", "TypeScript", "Tailwind CSS", "Node.js"],
        "https://github.com/njipangeraste",
    )

    st.html(f"""<div class="pf-section active">
<div class="section-inner">
<span class="eyebrow">Portfolio</span>
<h2 class="section-title">Projets Sélectionnés</h2>
{p1}{p2}{p3}
</div>
</div>""")


# ══════════════════════════════════════════════
# PAGE : EXPERIENCE
# ══════════════════════════════════════════════
elif current == "experience":
    def exp_item(period, title, company, desc):
        return f"""<div class="exp-item">
<div class="exp-period">{period}</div>
<div class="exp-title">{title}</div>
<div class="exp-company">{company}</div>
<p class="exp-desc">{desc}</p>
</div>"""

    def edu_item(period, title, school):
        return f"""<div class="exp-item">
<div class="exp-period">{period}</div>
<div class="exp-title">{title}</div>
<div class="exp-company">{school}</div>
</div>"""

    xp2 = exp_item(
        "Fév. – Mai 2025",
        "Développeur Stagiaire (Next.js)",
        "ISDEV Experts · Douala",
        "Conception d'une application web performante avec Next.js et Tailwind CSS. "
        "Mise en place du rendu SSR et déploiement automatisé via Vercel."
    )
    xp1 = exp_item(
        "Juil. – Oct. 2023",
        "Stagiaire Développeur Laravel",
        "FAGICIEL · Yaoundé",
        "Développement de modules backend en PHP/Laravel et intégration d'interfaces mobiles réactives."
    )
    
    ed1 = edu_item("2024 – 2025", "Licence Professionnelle Génie Logiciel", "Institut Universitaire du Golfe de Guinée")
    ed2 = edu_item("2023 – 2024", "BTS Génie Logiciel", "Institut Universitaire du Golfe de Guinée")
    ed3 = edu_item("2020 – 2021", "Baccalauréat TI", "Lycée Classique de Bangangté")

    st.html(f"""<div class="pf-section active">
<div class="section-inner">
<span class="eyebrow">Parcours</span>
<h2 class="section-title">Expériences & Éducation</h2>
<div class="skills-cat-title">Expériences Professionnelles</div>
<div class="exp-timeline">
{xp2}{xp1}
</div>
<div class="skills-cat-title" style="margin-top:4rem">Formation Académique</div>
<div class="exp-timeline">
{ed1}{ed2}{ed3}
</div>
</div>
</div>""")


# ══════════════════════════════════════════════
# PAGE : CONTACT
# ══════════════════════════════════════════════
elif current == "contact":
    # ── FORMSPREE : vrai envoi d'email sans SMTP ──────────────────────────────
    # 1. Créez un compte gratuit sur https://formspree.io
    # 2. Créez un formulaire → copiez votre Form ID (ex: "xpwzgkdo")
    # 3. Collez-le ici ↓  (laissez "" pour utiliser le fallback mailto)
    FORMSPREE_ID = ""   # ← ex: "xpwzgkdo"
    # ──────────────────────────────────────────────────────────────────────────

    import requests as _req
    import re as _re

    def is_valid_email(e: str) -> bool:
        return bool(_re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e.strip()))

    def send_via_formspree(form_id, name, email, subject, phone, message) -> tuple[bool, str]:
        """Envoie le formulaire à Formspree et retourne (succès, message)."""
        url = f"https://formspree.io/f/{form_id}"
        payload = {
            "name":    name,
            "email":   email,
            "phone":   phone or "non renseigné",
            "_subject": subject,
            "message": message,
        }
        try:
            r = _req.post(url, data=payload, headers={"Accept": "application/json"}, timeout=10)
            if r.status_code == 200:
                return True, "ok"
            data = r.json()
            return False, data.get("error", f"Erreur HTTP {r.status_code}")
        except _req.exceptions.Timeout:
            return False, "timeout"
        except Exception as exc:
            return False, str(exc)

    # ── UI ────────────────────────────────────────────────────────────────────
    st.html("""<div class="pf-section active">
<div class="section-inner">
<span class="eyebrow">Contact</span>
<h2 class="section-title">Discutons de votre projet</h2>
<p class="contact-note">
Que vous ayez un projet en tête, une opportunité professionnelle ou simplement
envie d'échanger sur l'IA et la tech — je réponds généralement sous 24h.
</p>
<div class="contact-grid">
<div class="contact-card">
<div class="contact-icon">📧</div>
<div class="contact-label">Email</div>
<div class="contact-value"><a href="mailto:enjipang@gmail.com">enjipang@gmail.com</a></div>
</div>
<div class="contact-card">
<div class="contact-icon">📞</div>
<div class="contact-label">Téléphone</div>
<div class="contact-value">+237 673 13 30 12</div>
</div>
<div class="contact-card">
<div class="contact-icon">💼</div>
<div class="contact-label">LinkedIn</div>
<div class="contact-value">
<a href="https://www.linkedin.com/in/eraste-njipang-162162266/" target="_blank">
eraste-njipang ↗
</a>
</div>
</div>
<div class="contact-card">
<div class="contact-icon">🐙</div>
<div class="contact-label">GitHub</div>
<div class="contact-value">
<a href="https://github.com/njipangeraste" target="_blank">njipangeraste ↗</a>
</div>
</div>
</div>
</div>
</div>
<div style="max-width:1080px; margin: 0 auto; padding: 0 3rem 2rem;">
<div class="skills-cat-title">Envoyer un message</div>
</div>""")

    if "form_sent" not in st.session_state:
        st.session_state.form_sent = False

    if st.session_state.form_sent:
        st.success("✅ Message envoyé avec succès ! Je vous répondrai sous 24h.")
        st.balloons()
        if st.button("Envoyer un autre message"):
            st.session_state.form_sent = False
            st.rerun()
    else:
        with st.form(key="contact_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                name    = st.text_input("Nom complet *", placeholder="Jean Dupont")
                email   = st.text_input("Email *", placeholder="jean@example.com")
            with col2:
                subject = st.text_input("Sujet *", placeholder="Opportunité / Projet / Question")
                phone   = st.text_input("Téléphone (optionnel)", placeholder="+237 6XX XX XX XX")
            message = st.text_area("Message *", height=150,
                                   placeholder="Décrivez votre projet ou votre demande...")
            submitted = st.form_submit_button("📨 Envoyer le message", type="primary",
                                              use_container_width=False)

        if submitted:
            # ── Validation ──
            errors = []
            if not name.strip():
                errors.append("Le nom est requis.")
            if not email.strip() or not is_valid_email(email):
                errors.append("Adresse email invalide.")
            if not subject.strip():
                errors.append("Le sujet est requis.")
            if not message.strip() or len(message.strip()) < 10:
                errors.append("Le message doit contenir au moins 10 caractères.")

            if errors:
                for e in errors:
                    st.error(f"❌ {e}")
            else:
                # ── Envoi ──
                if FORMSPREE_ID:
                    # Envoi HTTP réel via Formspree → reçu dans votre Gmail
                    with st.spinner("Envoi en cours..."):
                        ok, err = send_via_formspree(
                            FORMSPREE_ID, name.strip(), email.strip(),
                            subject.strip(), phone.strip(), message.strip()
                        )
                    if ok:
                        st.session_state.form_sent = True
                        st.rerun()
                    elif err == "timeout":
                        st.warning("⏱️ Le serveur met trop de temps à répondre. Vérifiez votre connexion et réessayez.")
                    else:
                        st.error(f"❌ Erreur Formspree : {err}")
                        st.info("💡 En attendant, écrivez directement à : enjipang@gmail.com")
                else:
                    # Fallback : mailto (ouvre le client email local)
                    import urllib.parse
                    body = urllib.parse.quote(
                        f"Nom : {name}\nEmail : {email}\n"
                        f"Téléphone : {phone or 'non renseigné'}\n\n{message}"
                    )
                    mailto = (
                        f"mailto:enjipang@gmail.com"
                        f"?subject={urllib.parse.quote(subject)}"
                        f"&body={body}"
                    )
                    st.html(f'<meta http-equiv="refresh" content="0;url={mailto}">')
                    st.info(
                        "⚠️ Formspree non configuré — votre client email s'ouvre.\n\n"
                        "Pour activer l'envoi automatique, renseignez `FORMSPREE_ID` dans le code."
                    )

# ──────────────────────────────────────────────
# GLOBAL FOOTER
# ──────────────────────────────────────────────
st.html("""<footer class="pf-footer">
<div class="pf-footer-logo">NJIPANG <em>ERASTE</em></div>
<p style="margin-bottom: 2rem; opacity: 0.7;">Développeur IA & Python passionné par l'innovation.</p>
<div class="pf-footer-copy">© 2026 NJIPANG DONGMO Eraste — Tous droits réservés</div>
</footer>""")