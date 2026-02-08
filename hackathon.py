import streamlit as st
from supabase import create_client
import datetime
import google.generativeai as genai

# 1. BAĞLANTILAR (SUPABASE + GEMINI AI)
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

# Google Gemini AI tənzimləməsi - Sənin verdiyin açar əlavə olundu
genai.configure(api_key="AIzaSyAY0vlR1_YOnD1bYUdS74tacmWq9w7EaSU")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="EduBalance AI", layout="centered")

# Sessiya yaddaşı (İstifadəçi adı itməməsi üçün)
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# 2. DİL SEÇİMİ VƏ TƏRCÜMƏLƏR
lang = st.sidebar.selectbox("🌐 Dil / Language / Langue", ["Azerbaycan", "English", "Français"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "user_label": "👤 İstifadəçi adı:",
        "user_placeholder": "Adınızı daxil edin...",
        "profile": "Profil Yarat",
        "daily": "Günlük Statistika",
        "study": "Dərs Sessiyası",
        "ai_tab": "🤖 AI Mentor",
        "ai_button": "AI-dan Məsləhət Al",
        "save": "Yadda saxla",
        "success": "Məlumatlar uğurla qeyd olundu!",
        "error_user": "Davam etmək üçün istifadəçi adını yazıb Enter basın!",
        "mood_label": "Təxmin edilən Əhval:",
        "sleep_label": "🌙 Yuxu (Saat):",
        "water_label": "💧 Su (Litr):",
        "target_label": "🎯 Hədəf İmtahan:",
        "subject_label": "📚 Fənni seçin:",
        "mood_status": {"great": "Əla 🔥", "normal": "Normal 😊", "tired": "Yorğun 😴"},
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
        "ai_tab": "🤖 AI Mentor",
        "ai_button": "Get AI Advice",
        "save": "Save Data",
        "success": "Data saved successfully!",
        "error_user": "Please enter username and press Enter!",
        "mood_label": "Estimated Mood:",
        "sleep_label": "🌙 Sleep (Hours):",
        "water_label": "💧 Water (Liters):",
        "target_label": "🎯 Target Exam:",
        "subject_label": "📚 Select Subject:",
        "mood_status": {"great": "Great 🔥", "normal": "Normal 😊", "tired": "Tired 😴"},
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
        "ai_tab": "🤖 IA Mentor",
        "ai_button": "Obtenir des conseils",
        "save": "Enregistrer",
        "success": "Données enregistrées avec succès !",
        "error_user": "Veuillez entrer votre nom et appuyer sur Entrée !",
        "mood_label": "Humeur Estimée :",
        "sleep_label": "🌙 Sommeil (Heures):",
        "water_label": "💧 Eau (Litres):",
        "target_label": "🎯 Examen Cible:",
        "subject_label": "📚 Sélectionner la matière:",
        "mood_status": {"great": "Excellent 🔥", "normal": "Normal 😊", "tired": "Fatigué 😴"},
        "exams": ["Examen de fin d'études", "Examen par bloc", "Maîtrise", "YÖS / SAT", "Recrutement des enseignants", "Certification", "Autre"],
        "subjects": ["Langue azerbaïdjanaise", "Mathématiques", "Anglais", "Physique", "Chimie", "Biologie", "Histoire", "Géographie", "Informatique", "Autre"]
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI GİRİŞİ
user_input = st.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])

if user_input:
    st.session_state.user_name = user_input

if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

# Tablar
tab1, tab2, tab3, tab4 = st.tabs([t['profile'], t['daily'], t['study'], t['ai_tab']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox(t['target_label'], t['exams'])
    if st.button(f"➕ {t['profile']}"):
        prof_data = {"username": st.session_state.user_name, "Language": lang, "target_exam": target}
        supabase.table("students_profiles").upsert(prof_data, on_conflict="username").execute()
        st.balloons()
        st.success(f"@{st.session_state.user_name}, {t['success']}")

# --- TAB 2: GÜNLÜK STATS ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sleep_duration = st.slider(t['sleep_label'], 0.0, 12.0, 8.0)
        water = st.number_input(t['water_label'], 0.0, 5.0, 1.5, step=0.1)
    
    with col2:
        score = (60 if 7 <= sleep_duration <= 9 else 30) + (40 if water >= 2 else 15)
        if score >= 90: current_mood = t['mood_status']['great']
        elif score >= 60: current_mood = t['mood_status']['normal']
        else: current_mood = t['mood_status']['tired']
            
        st.metric(t['mood_label'], current_mood)

    if st.button(f"💾 {t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep_duration, "mood": current_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])

# --- TAB 3: DƏRS SESSİYASI ---
with tab3:
    subject_choice = st.selectbox(t['subject_label'], t['subjects'])
    duration = st.number_input("⏱️ (min):", 10, 300, 45)
    
    if st.button(f"📖 {t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject_choice, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject_choice} - {t['success']}")

# --- TAB 4: AI MENTOR (GEMINI İNTEQRASİYASI) ---
with tab4:
    st.subheader(f"🤖 {st.session_state.user_name} üçün AI Mentor")
    if st.button(t['ai_button']):
        with st.spinner("AI analiz edir..."):
            prompt = f"""
            Sən EduBalance tətbiqində bir mentorsan.
            Tələbə məlumatları:
            - Yuxu: {sleep_duration} saat
            - Su içmə: {water} litr
            - Əhvalı: {current_mood}
            - Hədəf İmtahanı: {target}
            
            Bu məlumatlara əsasən tələbəyə qısa, motivasiyaedici və praktiki məsləhət ver.
            Məsləhəti yalnız {lang} dilində yaz və cəmi 2-3 cümlə olsun.
            """
            try:
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error("AI qoşulmasında xəta! Lütfən 'google-generativeai' kitabxanasının yükləndiyindən əmin olun.")

st.divider()
st.caption("EduBalance v1.4 | AI Powered 🚀")
