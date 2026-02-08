import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance", layout="centered")

# --- SESSİYA YADDAŞI (Məlumatların itməməsi üçün) ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# 2. DİL SEÇİMİ
lang = st.sidebar.selectbox("🌐 Dil / Language / Langue", ["Azerbaycan", "English", "Français"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "user_label": "👤 İstifadəçi adı:",
        "user_placeholder": "Adınızı daxil edin...",
        "profile": "Profil Yarat",
        "daily": "Günlük Statistika",
        "study": "Dərs Sessiyası",
        "save": "Yadda saxla",
        "success": "Məlumatlar uğurla qeyd olundu!",
        "error_user": "Davam etmək üçün istifadəçi adını yazıb Enter basın!",
        "mood_label": "Təxmin edilən Əhval:",
        "target_label": "🎯 Hədəf İmtahan:",
        "subject_label": "📚 Fənni seçin:",
        "exams": ["Buraxılış İmtahanı", "Blok İmtahanı", "Magistratura", "YÖS / SAT", "MİQ", "Sertifikasiya", "Digər"],
        "subjects": ["Azərbaycan dili", "Riyaziyyat", "İngilis dili", "Fizika", "Kimya", "Biologiya", "Tarix", "Coğrafiya", "İnformatika", "Digər"]
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "user_label": "👤 Username:",
        "user_placeholder": "Enter your name...",
        "profile": "Create Profile",
        "daily": "Daily Stats",
        "study": "Study Session",
        "save": "Save Data",
        "success": "Data saved successfully!",
        "error_user": "Please enter username and press Enter!",
        "mood_label": "Estimated Mood:",
        "target_label": "🎯 Target Exam:",
        "subject_label": "📚 Select Subject:",
        "exams": ["Graduation Exam", "Block Exam", "Master's Degree", "YÖS / SAT", "Teacher Recruitment", "Certification", "Other"],
        "subjects": ["Azerbaijani language", "Mathematics", "English", "Physics", "Chemistry", "Biology", "History", "Geography", "Informatics", "Other"]
    },
    "Français": {
        "welcome": "Bienvenue sur EduBalance",
        "user_label": "👤 Nom d'utilisateur:",
        "user_placeholder": "Entrez votre nom...",
        "profile": "Créer un profil",
        "daily": "Stats Quotidiennes",
        "study": "Session d'Étude",
        "save": "Enregistrer",
        "success": "Données enregistrées avec succès !",
        "error_user": "Veuillez entrer votre nom et appuyer sur Entrée !",
        "mood_label": "Humeur Estimée :",
        "target_label": "🎯 Examen Cible:",
        "exams": ["Examen de fin d'études", "Examen par bloc", "Maîtrise", "YÖS / SAT", "Recrutement des enseignants", "Certification", "Autre"],
        "subjects": ["Langue azerbaïdjanaise", "Mathématiques", "Anglais", "Physique", "Chimie", "Biologie", "Histoire", "Géographie", "Informatique", "Autre"]
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI (SESSION STATE İLƏ)
# value hissəsini st.session_state.user_name-ə bağladıq
user_input = st.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])

# Adı yaddaşda saxlayırıq
if user_input:
    st.session_state.user_name = user_input

if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

tab1, tab2, tab3 = st.tabs([t['profile'], t['daily'], t['study']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox(t['target_label'], t['exams'])
    if st.button(f"➕ {t['profile']}"):
        prof_data = {"username": st.session_state.user_name, "Language": lang, "target_exam": target}
        supabase.table("students_profiles").insert(prof_data).execute()
        st.balloons()
        st.success(f"@{st.session_state.user_name}, {t['success']}")

# --- TAB 2: GÜNLÜK STATS ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sleep_duration = st.slider("🌙 Yuxu (Saat):", 0.0, 12.0, 8.0)
        water = st.number_input("💧 Su (Litr):", 0.0, 5.0, 1.5, step=0.1)
    
    with col2:
        score = (60 if 7 <= sleep_duration <= 9 else 30) + (40 if water >= 2 else 15)
        auto_mood = "Əla" if score >= 90 else "Normal" if score >= 60 else "Yorğun"
        st.metric(t['mood_label'], auto_mood)

    if st.button(f"💾 {t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep_duration, "mood": auto_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])

# --- TAB 3: DƏRS SESSİYASI ---
with tab3:
    subject_choice = st.selectbox(t['subject_label'], t['subjects'])
    duration = st.number_input("⏱️ (Dəqiqə):", 10, 300, 45)
    
    if st.button(f"📖 {t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject_choice, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject_choice} qeyd edildi!")

st.divider()
st.caption("EduBalance v1.2 | Fixed State 🚀")
