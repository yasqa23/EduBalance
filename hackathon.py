import streamlit as st
from supabase import create_client
import datetime
import google.generativeai as genai

# 1. BAĞLANTILAR
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

# AI tənzimləməsi (Sənin açarın)
genai.configure(api_key="AIzaSyAY0vlR1_YOnD1bYUdS74tacmWq9w7EaSU")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="EduBalance Global", layout="centered")

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# 2. 7 DİLLİ LÜĞƏT SİSTEMİ (Addım 1)
lang = st.sidebar.selectbox("🌐 Dil / Language", 
    ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "user_label": "👤 İstifadəçi adı:",
        "profile": "Profil",
        "daily": "Statistika",
        "study": "Dərs",
        "ai_mentor": "🤖 AI Mentor",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivasiya",
        "save": "Yadda saxla",
        "success": "Uğurla tamamlandı!",
        "error_user": "Adınızı daxil edin!",
        "target_label": "🎯 Hədəf İmtahan:"
    },
    "Türkçe": {
        "welcome": "EduBalance'a Hoş Geldiniz",
        "user_label": "👤 Kullanıcı Adı:",
        "profile": "Profil",
        "daily": "İstatistik",
        "study": "Ders",
        "ai_mentor": "🤖 AI Mentor",
        "playlist": "📺 Oynatma Listesi",
        "motivation": "🔥 Motivasyon",
        "save": "Kaydet",
        "success": "Başarıyla tamamlandı!",
        "error_user": "Adınızı giriniz!",
        "target_label": "🎯 Hedef Sınav:"
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "user_label": "👤 Username:",
        "profile": "Profile",
        "daily": "Stats",
        "study": "Study",
        "ai_mentor": "🤖 AI Mentor",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivation",
        "save": "Save",
        "success": "Successfully completed!",
        "error_user": "Please enter your name!",
        "target_label": "🎯 Target Exam:"
    },
    "Español": {
        "welcome": "Bienvenido a EduBalance",
        "user_label": "👤 Usuario:",
        "profile": "Perfil",
        "daily": "Estadísticas",
        "study": "Estudio",
        "ai_mentor": "🤖 IA Mentor",
        "playlist": "📺 Lista de reproducción",
        "motivation": "🔥 Motivación",
        "save": "Guardar",
        "success": "¡Completado con éxito!",
        "error_user": "¡Ingrese su nombre!",
        "target_label": "🎯 Examen Objetivo:"
    },
    "Italiano": {
        "welcome": "Benvenuti in EduBalance",
        "user_label": "👤 Nome utente:",
        "profile": "Profilo",
        "daily": "Statistiche",
        "study": "Studio",
        "ai_mentor": "🤖 IA Mentor",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivazione",
        "save": "Salva",
        "success": "Completato con successo!",
        "error_user": "Inserisci il tuo nome!",
        "target_label": "🎯 Esame Obiettivo:"
    },
    "Français": {
        "welcome": "Bienvenue sur EduBalance",
        "user_label": "👤 Nom d'utilisateur:",
        "profile": "Profil",
        "daily": "Stats",
        "study": "Étude",
        "ai_mentor": "🤖 IA Mentor",
        "playlist": "📺 Playlist",
        "motivation": "🔥 Motivation",
        "save": "Enregistrer",
        "success": "Terminé avec succès !",
        "error_user": "Entrez votre nom !",
        "target_label": "🎯 Examen Cible:"
    },
    "Deutsch": {
        "welcome": "Willkommen bei EduBalance",
        "user_label": "👤 Benutzername:",
        "profile": "Profil",
        "daily": "Statistiken",
        "study": "Studium",
        "ai_mentor": "🤖 KI-Mentor",
        "playlist": "📺 Playlisten",
        "motivation": "🔥 Motivation",
        "save": "Speichern",
        "success": "Erfolgreich abgeschlossen!",
        "error_user": "Geben Sie Ihren Namen ein!",
        "target_label": "🎯 Zielprüfung:"
    },
    "Русский": {
        "welcome": "Добро пожаловать в EduBalance",
        "user_label": "👤 Имя пользователя:",
        "profile": "Профиль",
        "daily": "Статистика",
        "study": "Учеба",
        "ai_mentor": "🤖 ИИ Ментор",
        "playlist": "📺 Плейлисты",
        "motivation": "🔥 Мотивация",
        "save": "Сохранить",
        "success": "Успешно завершено!",
        "error_user": "Введите ваше имя!",
        "target_label": "🎯 Целевой Экзамен:"
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# Kullanıcı Girişi
user_input = st.text_input(t['user_label'], value=st.session_state.user_name)
if user_input:
    st.session_state.user_name = user_input

if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

# 3. YENİ TAB STRUKTURU (Addım-addım dolduracağıq)
tab1, tab2, tab3, tab4, tab5 = st.tabs([t['profile'], t['daily'], t['ai_mentor'], t['playlist'], t['motivation']])

with tab1:
    st.subheader(t['profile'])
    # Profil kodları bura gələcək...

with tab2:
    st.subheader(t['daily'])
    # Statistika kodları bura gələcək...

with tab3:
    st.subheader(t['ai_mentor'])
    st.info("Bu bölmədə AI sənin üçün cədvəl hazırlayacaq (Növbəti addım).")

with tab4:
    st.subheader(t['playlist'])
    st.info("Abituriyentlər üçün video dərslər bura əlavə olunacaq.")

with tab5:
    st.subheader(t['motivation'])
    st.info("Uğur hekayələri və fun-fact bölməsi.")

st.divider()
st.caption(f"EduBalance v2.0 | Language: {lang} 🚀")
