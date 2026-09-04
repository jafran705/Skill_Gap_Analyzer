import streamlit as st
from pypdf import PdfReader
from urllib.parse import quote_plus
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI-Based Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# JOB ROLE DATABASE
# =========================================================

role_skills = {

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "statistics",
        "data visualization",
        "pandas",
        "numpy"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "statistics",
        "pandas",
        "numpy",
        "machine learning",
        "deep learning",
        "data visualization"
    ],

    "Python Developer": [
        "python",
        "sql",
        "git",
        "django",
        "flask",
        "api",
        "html",
        "css"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git",
        "python",
        "sql",
        "api"
    ],

    "AI Engineer": [
        "python",
        "numpy",
        "pandas",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "sql"
    ],

    "Machine Learning Engineer": [
        "python",
        "numpy",
        "pandas",
        "machine learning",
        "deep learning",
        "scikit-learn",
        "tensorflow",
        "sql"
    ]
}


# =========================================================
# SUPPORTED LANGUAGES
# =========================================================

languages = [
    "English",
    "Tamil",
    "Hindi",
    "Telugu",
    "Malayalam",
    "Kannada",
    "Bengali",
    "Marathi",
    "Gujarati",
    "Punjabi",
    "Urdu"
]


# =========================================================
# SKILL ALIASES
# =========================================================

skill_aliases = {

    "python programming": "python",
    "python language": "python",

    "structured query language": "sql",

    "ms excel": "excel",
    "microsoft excel": "excel",

    "powerbi": "power bi",
    "power-bi": "power bi",

    "data visualisation": "data visualization",
    "data visualization tools": "data visualization",

    "machinelearning": "machine learning",

    "deep-learning": "deep learning",

    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",

    "js": "javascript",

    "reactjs": "react",

    "tensorflow": "tensorflow",

    "pytorch framework": "pytorch"
}


# =========================================================
# YOUTUBE LINK FUNCTION
# =========================================================

def create_youtube_link(skill, language):

    search_text = f"{skill} tutorial {language}"

    encoded_text = quote_plus(search_text)

    return (
        "https://www.youtube.com/results?search_query="
        + encoded_text
    )


# =========================================================
# NORMALIZE SKILLS
# =========================================================

def normalize_skill(skill):

    skill = skill.strip().lower()

    if skill in skill_aliases:

        return skill_aliases[skill]

    return skill


# =========================================================
# RESUME TEXT EXTRACTION
# =========================================================

def extract_resume_text(uploaded_file):

    try:

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + " "

        return text.lower()

    except Exception:

        return ""


# =========================================================
# DETECT SKILLS FROM RESUME
# =========================================================

def detect_resume_skills(resume_text):

    detected = []

    all_skills = set()

    for skills in role_skills.values():

        for skill in skills:

            all_skills.add(skill)

    for skill in all_skills:

        if skill.lower() in resume_text:

            detected.append(skill)

    return detected


# =========================================================
# PDF REPORT GENERATOR
# =========================================================

def create_pdf_report(
    name,
    target_role,
    language,
    readiness,
    skill_gap,
    matched_skills,
    missing_skills
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    width, height = A4

    y = height - 50

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        width / 2,
        y,
        "AI-Based Skill Gap Analyzer"
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        width / 2,
        y,
        "Personalized Career Analysis Report"
    )

    y -= 50

    # -----------------------------------------------------
    # STUDENT INFORMATION
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Student Information"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        60,
        y,
        f"Name: {name}"
    )

    y -= 20

    pdf.drawString(
        60,
        y,
        f"Target Role: {target_role}"
    )

    y -= 20

    pdf.drawString(
        60,
        y,
        f"Learning Language: {language}"
    )

    y -= 35

    # -----------------------------------------------------
    # ANALYSIS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Skill Analysis"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        60,
        y,
        f"Skill Readiness: {readiness:.1f}%"
    )

    y -= 20

    pdf.drawString(
        60,
        y,
        f"Skill Gap: {skill_gap:.1f}%"
    )

    y -= 35

    # -----------------------------------------------------
    # MATCHED SKILLS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Skills You Have"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    if matched_skills:

        for skill in matched_skills:

            pdf.drawString(
                70,
                y,
                "• " + skill.title()
            )

            y -= 18

            if y < 60:

                pdf.showPage()

                y = height - 50

                pdf.setFont(
                    "Helvetica",
                    11
                )

    else:

        pdf.drawString(
            70,
            y,
            "No matching skills found."
        )

        y -= 20

    y -= 15

    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Skills To Learn"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    if missing_skills:

        for skill in missing_skills:

            pdf.drawString(
                70,
                y,
                "• " + skill.title()
            )

            y -= 18

            if y < 60:

                pdf.showPage()

                y = height - 50

                pdf.setFont(
                    "Helvetica",
                    11
                )

    else:

        pdf.drawString(
            70,
            y,
            "No missing skills."
        )

        y -= 20

    y -= 15

    # -----------------------------------------------------
    # ROADMAP
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "Personalized Roadmap"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    if missing_skills:

        for index, skill in enumerate(
            missing_skills,
            start=1
        ):

            pdf.drawString(
                70,
                y,
                f"Week {index}: Learn {skill.title()}"
            )

            y -= 18

            if y < 60:

                pdf.showPage()

                y = height - 50

                pdf.setFont(
                    "Helvetica",
                    11
                )

    else:

        pdf.drawString(
            70,
            y,
            "Ready to apply for the target role."
        )

        y -= 20

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    y = 40

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawCentredString(
        width / 2,
        y,
        "Generated by AI-Based Skill Gap Analyzer"
    )

    pdf.save()

    buffer.seek(0)

    return buffer


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🎯 AI-Based Skill Gap Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Personalized Career Roadmap Generator'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Analyze your resume and current skills to discover "
    "the skills required for your dream career."
)

st.divider()


# =========================================================
# STUDENT DETAILS
# =========================================================

st.header("👤 Student Details")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Enter Your Name",
        placeholder="Example: Your Name"
    )

with col2:

    target_role = st.selectbox(
        "🎯 Select Your Target Job Role",
        list(role_skills.keys())
    )


# =========================================================
# LEARNING LANGUAGE
# =========================================================

st.header("🌐 Learning Language")

selected_language = st.selectbox(
    "Select your preferred learning language",
    languages
)

st.info(
    f"🎥 Learning videos will be searched in "
    f"**{selected_language}**."
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.header("📄 Resume Upload")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

resume_text = ""

if uploaded_file is not None:

    resume_text = extract_resume_text(
        uploaded_file
    )

    if resume_text:

        st.success(
            "✅ Resume uploaded and text extracted successfully!"
        )

    else:

        st.error(
            "❌ Could not extract text from the resume."
        )


# =========================================================
# CURRENT SKILLS
# =========================================================

st.header("💻 Current Skills")

current_skills = st.text_area(
    "Enter your current skills separated by commas",
    placeholder=(
        "Example: Python, SQL, Excel, Pandas"
    )
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze_button = st.button(
    "🔍 Analyze My Skills",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name:

        st.warning(
            "⚠️ Please enter your name."
        )

    elif not current_skills and not resume_text:

        st.warning(
            "⚠️ Please enter your skills "
            "or upload your resume."
        )

    else:

        # =================================================
        # MANUAL SKILLS
        # =================================================

        manual_skills = []

        for skill in current_skills.split(","):

            skill = normalize_skill(skill)

            if skill:

                manual_skills.append(skill)

        # =================================================
        # RESUME SKILLS
        # =================================================

        resume_skills = detect_resume_skills(
            resume_text
        )

        # =================================================
        # COMBINE
        # =================================================

        detected_skills = set(
            manual_skills + resume_skills
        )

        required_skills = role_skills[
            target_role
        ]

        # =================================================
        # MATCHED SKILLS
        # =================================================

        matched_skills = []

        for skill in required_skills:

            if skill in detected_skills:

                matched_skills.append(skill)

        # =================================================
        # MISSING SKILLS
        # =================================================

        missing_skills = []

        for skill in required_skills:

            if skill not in detected_skills:

                missing_skills.append(skill)

        # =================================================
        # CALCULATE
        # =================================================

        total_skills = len(
            required_skills
        )

        matched_count = len(
            matched_skills
        )

        readiness = (
            matched_count / total_skills
        ) * 100

        skill_gap = 100 - readiness

        # =================================================
        # RESULT HEADER
        # =================================================

        st.divider()

        st.header(
            "📊 Skill Gap Analysis"
        )

        st.write(
            f"### 👋 Welcome, {name}!"
        )

        st.write(
            f"**Target Job Role:** {target_role}"
        )

        st.write(
            f"**Learning Language:** {selected_language}"
        )

        # =================================================
        # METRICS
        # =================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎯 Skill Readiness",
                f"{readiness:.1f}%"
            )

        with col2:

            st.metric(
                "📉 Skill Gap",
                f"{skill_gap:.1f}%"
            )

        with col3:

            st.metric(
                "✅ Skills Matched",
                f"{matched_count}/{total_skills}"
            )

        # =================================================
        # PROGRESS BAR
        # =================================================

        st.subheader(
            "📈 Career Readiness"
        )

        st.progress(
            int(readiness)
        )

        # =================================================
        # SKILL GAP CHART
        # =================================================

        st.subheader(
            "📊 Skill Readiness vs Skill Gap"
        )

        chart_data = {
            "Skill Analysis": [
                "Skill Readiness",
                "Skill Gap"
            ],
            "Percentage": [
                readiness,
                skill_gap
            ]
        }

        st.bar_chart(
            chart_data,
            x="Skill Analysis",
            y="Percentage"
        )

        # =================================================
        # DETECTED SKILLS
        # =================================================

        st.divider()

        st.subheader(
            "💡 Skills Detected"
        )

        if detected_skills:

            for skill in sorted(
                detected_skills
            ):

                st.write(
                    f"✅ {skill.title()}"
                )

        else:

            st.info(
                "No skills detected."
            )

        # =================================================
        # MATCHED SKILLS
        # =================================================

        st.subheader(
            "🟢 Required Skills You Already Have"
        )

        if matched_skills:

            for skill in matched_skills:

                st.write(
                    f"🟢 {skill.title()}"
                )

        else:

            st.info(
                "No matching skills found."
            )

        # =================================================
        # MISSING SKILLS
        # =================================================

        st.subheader(
            "🔴 Skills You Need To Learn"
        )

        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"🔴 {skill.title()}"
                )

        else:

            st.success(
                "🎉 You have all the required skills!"
            )

        # =================================================
        # LEARNING VIDEOS
        # =================================================

        if missing_skills:

            st.divider()

            st.header(
                "🎥 Recommended Learning Videos"
            )

            st.write(
                f"Learning resources for "
                f"**{selected_language}**"
            )

            for skill in missing_skills:

                st.markdown(
                    f"### 🔴 {skill.title()}"
                )

                youtube_link = create_youtube_link(
                    skill,
                    selected_language
                )

                st.markdown(
                    f"▶️ [Watch {skill.title()} "
                    f"Videos in {selected_language}]"
                    f"({youtube_link})"
                )

                st.caption(
                    f"YouTube Search: "
                    f"{skill.title()} tutorial "
                    f"{selected_language}"
                )

        # =================================================
        # PERSONALIZED ROADMAP
        # =================================================

        st.divider()

        st.header(
            "🗺️ Personalized Career Roadmap"
        )

        if missing_skills:

            for week, skill in enumerate(
                missing_skills,
                start=1
            ):

                st.markdown(
                    f"""
### 📅 Week {week}: {skill.title()}

🌐 **Learning Language:** {selected_language}

📖 Learn the basic concepts

🎥 Watch tutorials in {selected_language}

💻 Practice with examples

📝 Complete exercises

🛠️ Build a mini project

📄 Add the skill to your resume

"""
                )

        else:

            st.success(
                "🚀 You are ready for this career!"
            )

        # =================================================
        # CAREER RECOMMENDATION
        # =================================================

        st.divider()

        st.header(
            "🎯 Career Recommendation"
        )

        if readiness >= 80:

            st.success(
                "🌟 Excellent! Your skills are strongly "
                "aligned with this job role. "
                "You can start applying for internships "
                "and entry-level jobs."
            )

        elif readiness >= 60:

            st.info(
                "👍 Good progress! Focus on the missing "
                "skills and build practical projects."
            )

        elif readiness >= 40:

            st.warning(
                "📚 You have a basic foundation. "
                "Follow the roadmap and practice regularly."
            )

        else:

            st.error(
                "⚠️ Your current skill gap is high. "
                "Start learning the recommended skills "
                "step by step."
            )

        # =================================================
        # PDF REPORT
        # =================================================

        st.divider()

        st.header(
            "📥 Download Your Report"
        )

        pdf_file = create_pdf_report(
            name=name,
            target_role=target_role,
            language=selected_language,
            readiness=readiness,
            skill_gap=skill_gap,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )

        st.download_button(
            label="📥 Download Skill Gap Report (PDF)",
            data=pdf_file,
            file_name="Skill_Gap_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =========================================================
# RESET BUTTON
# =========================================================

st.divider()

if st.button(
    "🔄 Reset",
    use_container_width=True
):

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 AI-Based Skill Gap Analyzer | "
    "B.Tech Artificial Intelligence & Data Science Project"
)