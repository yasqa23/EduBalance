import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance", layout="centered")

# 2. DİL SEÇİMİ
lang = st.sidebar.selectbox("🌐 Dil / Language / Langue", ["Azerbaycan", "English", "Français"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "user_placeholder": "İstifadəçi adınızı daxil edin (məs: elnur_01)",
        "profile": "Profil Yarat",
        "daily": "Günlük Statistika",
        "study": "Dərs Sessiyası",
        "save": "Yadda saxla",
        "success": "Məlumatlar uğurla qeyd olundu!",
        "error_user": "Zəhmət olmasa əvvəlcə istifadəçi adı yaradın!",
        "mood_label": "Təxmin edilən Əhval:",
        "target_label": "🎯 Hədəf İmtahan:",
        "subject_label": "📚 Fənni seçin:",
        "exams": ["Buraxılış İmtahanı", "Blok İmtahanı", "Magistratura", "YÖS / SAT", "MİQ", "Sertifikasiya", "Digər"],
        "subjects": ["Azərbaycan dili", "Riyaziyyat", "İngilis dili", "Fizika", "Kimya", "Biologiya", "Tarix", "Coğrafiya", "İnformatika", "Digər"]
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "user_placeholder": "Enter your username (e.g., elnur_01)",
        "profile": "Create Profile",
        "daily": "Daily Stats",
        "study": "Study Session",
        "save": "Save Data",
        "success": "Data saved successfully!",
        "error_user": "Please create a username first!",
        "mood_label": "Estimated Mood:",
        "target_label": "🎯 Target Exam:",
        "subject_label": "📚 Select Subject:",
        "exams": ["Graduation Exam", "Block Exam", "Master's Degree", "YÖS / SAT", "Teacher Recruitment", "Certification", "Other"],
        "subjects": ["Azerbaijani language", "Mathematics", "English", "Physics", "Chemistry", "Biology", "History", "Geography", "Informatics", "Other"]
    },
    "Français": {
        "welcome": "Bienvenue sur EduBalance",
        "user_placeholder": "Entrez votre nom d'utilisateur",
        "profile": "Créer un profil",
        "daily": "Stats Quotidiennes",
        "study": "Session d'Étude",
        "save": "Enregistrer",
        "success": "Données enregistrées avec succès !",
        "error_user": "Veuillez d'abord créer un nom d'utilisateur !",
        "mood_label": "Humeur Estimée :",
        "target_label": "🎯 Examen Cible:",
        "exams": ["Examen de fin d'études", "Examen par bloc", "Maîtrise", "YÖS / SAT", "Recrutement des enseignants", "Certification", "Autre"],
        "subjects": ["Langue azerbaïdjanaise", "Mathématiques", "Anglais", "Physique", "Chimie", "Biologie", "Histoire", "Géographie", "Informatique", "Autre"]
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI YARADILMASI (BOŞ BURAXILDI)
user_name_input = st.text_input("👤 Username:", placeholder=t['user_placeholder']).strip()

if not user_name_input:
    st.warning(t['error_user'])
    st.stop() # İstifadəçi adı yazılana qədər proqramın qalanını göstərmir

tab1, tab2, tab3 = st.tabs([t['profile'], t['daily'], t['study']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox(t['target_label'], t['exams'])
    if st.button(f"➕ {t['profile']}"):
        prof_data = {"username": user_name_input, "Language": lang, "target_exam": target}
        supabase.table("students_profiles").insert(prof_data).execute()
        st.balloons()
        st.success(f"@{user_name_input}, {t['success']}")

# --- TAB 2: GÜNLÜK STATS ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sleep_duration = st.slider("🌙 Yuxu (Saat):", 0.0, 12.0, 8.0)
        water = st.number_input("💧 Su (Litr):", 0.0, 5.0, 1.5, step=0.1)
    
    with col2:
        # Əhval hesablama məntiqi
        score = (60 if 7 <= sleep_duration <= 9 else 30) + (40 if water >= 2 else 15)
        auto_mood = "Əla" if score >= 90 else "Normal" if score >= 60 else "Yorğun"
        st.metric(t['mood_label'], auto_mood)

    if st.button(f"💾 {t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep_duration, "mood": auto_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])
        else:
            st.error("Bu istifadəçi adı ilə profil tapılmadı. Öncə 'Profil Yarat' bölməsinə keçin.")

# --- TAB 3: DƏRS SESSİYASI ---
with tab3:
    subject_choice = st.selectbox(t['subject_label'], t['subjects'])
    duration = st.number_input("⏱️ (Dəqiqə):", 10, 300, 45)
    
    if st.button(f"📖 {t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject_choice, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject_choice} qeyd edildi!")

st.divider()
st.caption("EduBalance v1.1 | Hackathon Project 🚀")
