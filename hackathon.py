import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance Global", layout="centered")

# Sessiya yaddaşı
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# 2. 7 DİLLİ LÜĞƏT SİSTEMİ
lang = st.sidebar.selectbox("🌐 Choose Language / Dil seçin", 
    ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "user_label": "👤 İstifadəçi adı:",
        "user_placeholder": "Adınızı daxil edin...",
        "profile": "Profil",
        "daily": "Statistika",
        "study": "Dərs",
        "ai_mentor": "📅 Cədvəl Planı",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivasiya",
        "save": "Yadda saxla",
        "success": "Uğurla tamamlandı!",
        "error_user": "Davam etmək üçün adınızı yazıb Enter basın!",
        "target_label": "🎯 Hədəf İmtahan:",
        "subject_label": "📚 Fənni seçin:",
        "sleep_label": "🌙 Yuxu (Saat):",
        "water_label": "💧 Su (Litr):",
        "mood_label": "Təxmin edilən Əhval:",
        "mood_status": {"great": "Əla 🔥", "normal": "Normal 😊", "tired": "Yorğun 😴"},
        "exams": ["Buraxılış İmtahanı", "Blok İmtahanı", "Magistratura", "YÖS / SAT", "MİQ", "Sertifikasiya", "Digər"],
        "subjects": ["Azərbaycan dili", "Riyaziyyat", "İngilis dili", "Fizika", "Kimya", "Biologiya", "Tarix", "Coğrafiya", "İnformatika", "Digər"]
    },
    "Türkçe": {
        "welcome": "EduBalance'a Hoş Geldiniz",
        "user_label": "👤 Kullanıcı adı:",
        "user_placeholder": "Adınızı girin...",
        "profile": "Profil",
        "daily": "İstatistik",
        "study": "Ders",
        "ai_mentor": "📅 Ders Planı",
        "playlist": "📺 Oynatma Listesi",
        "motivation": "🔥 Motivasyon",
        "save": "Kaydet",
        "success": "Başarıyla tamamlandı!",
        "error_user": "Devam etmek için adınızı girin!",
        "target_label": "🎯 Hedef Sınav:",
        "subject_label": "📚 Ders seçin:",
        "sleep_label": "🌙 Uyku (Saat):",
        "water_label": "💧 Su (Litre):",
        "mood_label": "Tahmini Ruh Hali:",
        "mood_status": {"great": "Harika 🔥", "normal": "Normal 😊", "tired": "Yorgun 😴"},
        "exams": ["Mezuniyet Sınavı", "Blok Sınavı", "Yüksek Lisans", "YÖS / SAT", "Öğretmen Atama", "Sertifika", "Diğer"],
        "subjects": ["Türkçe", "Matematik", "İngilizce", "Fizik", "Kimya", "Biyoloji", "Tarih", "Coğrafya", "Bilişim", "Diğer"]
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "user_label": "👤 Username:",
        "user_placeholder": "Enter your name...",
        "profile": "Profile",
        "daily": "Stats",
        "study": "Study",
        "ai_mentor": "📅 Study Plan",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivation",
        "save": "Save",
        "success": "Successfully completed!",
        "error_user": "Please enter username and press Enter!",
        "target_label": "🎯 Target Exam:",
        "subject_label": "📚 Select Subject:",
        "sleep_label": "🌙 Sleep (Hours):",
        "water_label": "💧 Water (Liters):",
        "mood_label": "Estimated Mood:",
        "mood_status": {"great": "Great 🔥", "normal": "Normal 😊", "tired": "Tired 😴"},
        "exams": ["Graduation Exam", "Block Exam", "Master's Degree", "YÖS / SAT", "Teacher Recruitment", "Certification", "Other"],
        "subjects": ["Language", "Mathematics", "English", "Physics", "Chemistry", "Biology", "History", "Geography", "Informatics", "Other"]
    },
    "Español": {
        "welcome": "Bienvenido a EduBalance",
        "user_label": "👤 Usuario:",
        "user_placeholder": "Ingresa tu nombre...",
        "profile": "Perfil",
        "daily": "Estadísticas",
        "study": "Estudio",
        "ai_mentor": "📅 Horario",
        "playlist": "📺 Lista",
        "motivation": "🔥 Motivación",
        "save": "Guardar",
        "success": "¡Éxito!",
        "error_user": "¡Ingrese su nombre!",
        "target_label": "🎯 Examen Objetivo:",
        "subject_label": "📚 Materia:",
        "sleep_label": "🌙 Sueño (Horas):",
        "water_label": "💧 Agua (Litros):",
        "mood_label": "Estado de ánimo:",
        "mood_status": {"great": "Genial 🔥", "normal": "Normal 😊", "tired": "Cansado 😴"},
        "exams": ["Graduación", "Bloque", "Maestría", "SAT", "Otros"],
        "subjects": ["Lengua", "Matemáticas", "Inglés", "Física", "Química", "Biología", "Otros"]
    },
    "Italiano": {
        "welcome": "Benvenuti in EduBalance",
        "user_label": "👤 Nome utente:",
        "user_placeholder": "Inserisci il tuo nome...",
        "profile": "Profilo",
        "daily": "Statistiche",
        "study": "Studio",
        "ai_mentor": "📅 Piano",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivazione",
        "save": "Salva",
        "success": "Completato!",
        "error_user": "Inserisci il tuo nome!",
        "target_label": "🎯 Esame Obiettivo:",
        "subject_label": "📚 Materia:",
        "sleep_label": "🌙 Sonno (Ore):",
        "water_label": "💧 Acqua (Litri):",
        "mood_label": "Umore Stimato:",
        "mood_status": {"great": "Ottimo 🔥", "normal": "Normale 😊", "tired": "Stanco 😴"},
        "exams": ["Laurea", "Master", "SAT", "Altro"],
        "subjects": ["Lingua", "Matematica", "Inglese", "Fisica", "Chimica", "Biologia", "Altro"]
    },
    "Français": {
        "welcome": "Bienvenue sur EduBalance",
        "user_label": "👤 Nom d'utilisateur:",
        "user_placeholder": "Entrez votre nom...",
        "profile": "Profil",
        "daily": "Stats",
        "study": "Étude",
        "ai_mentor": "📅 Calendrier",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivation",
        "save": "Enregistrer",
        "success": "Succès !",
        "error_user": "Entrez votre nom !",
        "target_label": "🎯 Examen Cible:",
        "subject_label": "📚 Matière:",
        "sleep_label": "🌙 Sommeil (Heures):",
        "water_label": "💧 Eau (Litres):",
        "mood_label": "Humeur Estimée:",
        "mood_status": {"great": "Excellent 🔥", "normal": "Normal 😊", "tired": "Fatigué 😴"},
        "exams": ["Fin d'études", "Master", "SAT", "Autre"],
        "subjects": ["Langue", "Mathématiques", "Anglais", "Physique", "Chimie", "Biologie", "Autre"]
    },
    "Deutsch": {
        "welcome": "Willkommen bei EduBalance",
        "user_label": "👤 Benutzername:",
        "user_placeholder": "Namen eingeben...",
        "profile": "Profil",
        "daily": "Statistiken",
        "study": "Lernen",
        "ai_mentor": "📅 Lernplan",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivation",
        "save": "Speichern",
        "success": "Erfolg!",
        "error_user": "Name eingeben!",
        "target_label": "🎯 Zielprüfung:",
        "subject_label": "📚 Fach auswählen:",
        "sleep_label": "🌙 Schlaf (Stunden):",
        "water_label": "💧 Wasser (Liter):",
        "mood_label": "Stimmung:",
        "mood_status": {"great": "Super 🔥", "normal": "Normal 😊", "tired": "Müde 😴"},
        "exams": ["Abschluss", "Master", "SAT", "Andere"],
        "subjects": ["Sprache", "Mathematik", "Englisch", "Physik", "Chemie", "Biologie", "Andere"]
    },
    "Русский": {
        "welcome": "Добро пожаловать в EduBalance",
        "user_label": "👤 Имя пользователя:",
        "user_placeholder": "Введите имя...",
        "profile": "Профиль",
        "daily": "Статистика",
        "study": "Учеба",
        "ai_mentor": "📅 План",
        "playlist": "📺 Плейлист",
        "motivation": "🔥 Мотивация",
        "save": "Сохранить",
        "success": "Успешно!",
        "error_user": "Введите имя!",
        "target_label": "🎯 Целевой Экзамен:",
        "subject_label": "📚 Предмет:",
        "sleep_label": "🌙 Сон (Часы):",
        "water_label": "💧 Вода (Литры):",
        "mood_label": "Настроение:",
        "mood_status": {"great": "Отлично 🔥", "normal": "Нормально 😊", "tired": "Усталость 😴"},
        "exams": ["Выпускной", "Магистратура", "SAT", "Другое"],
        "subjects": ["Язык", "Математика", "Английский", "Физика", "Химия", "Биология", "Другое"]
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# İSTİFADƏÇİ GİRİŞİ
user_input = st.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])

if user_input:
    st.session_state.user_name = user_input

if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

# TAB STRUKTURU
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([t['profile'], t['daily'], t['study'], t['ai_mentor'], t['playlist'], t['motivation']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox(t['target_label'], t['exams'])
    if st.button(f"➕ {t['profile']}"):
        prof_data = {"username": st.session_state.user_name, "Language": lang, "target_exam": target}
        # Upsert istifadə edirik ki, eyni adam yenidən qeyd olsa xəta verməsin, sadəcə yeniləsin
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

# --- TAB 4, 5, 6 (STATİK BÖLMƏLƏR) ---
with tab4:
    st.info("📅 Tezliklə: Burada dərsləriniz üçün xüsusi cədvəl olacaq.")

with tab5:
    st.info("📺 Tezliklə: Abituriyentlər üçün seçilmiş dərs playlistləri.")

with tab6:
    st.info("🔥 Tezliklə: Uğur hekayələri və maraqlı faktlar.")

st.divider()
st.caption("EduBalance v2.0 | Multi-Language Stable Edition 🚀")
