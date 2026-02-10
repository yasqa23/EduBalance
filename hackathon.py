import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance", layout="centered")

# Sessiya yaddaşı
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# 2. 7 DİLLİ LÜĞƏT SİSTEMİ
lang = st.sidebar.selectbox("🌐 Dil / Language", 
    ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "user_label": "👤 İstifadəçi adı:",
        "user_placeholder": "Adınızı daxil edin...",
        "profile": "Profil Yarat",
        "daily": "Günlük Statistika",
        "study": "Dərs Sessiyası",
        "schedule": "📅 Ağıllı Cədvəl",
        "playlist": "📺 Playlistlər",
        "motivation": "🔥 Motivasiya",
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
    "Türkçe": {
        "welcome": "EduBalance'a Hoş Geldiniz", "user_label": "👤 Kullanıcı adı:", "user_placeholder": "Adınızı girin...",
        "profile": "Profil Oluştur", "daily": "Günlük İstatistik", "study": "Ders Oturumu", "schedule": "📅 Akıllı Program",
        "playlist": "📺 Oynatma Listeleri", "motivation": "🔥 Motivasyon", "save": "Kaydet", "success": "Başarıyla kaydedildi!",
        "error_user": "Devam etmek için kullanıcı adınızı girin!", "mood_label": "Tahmini Ruh Hali:",
        "sleep_label": "🌙 Uyku (Saat):", "water_label": "💧 Su (Litre):", "target_label": "🎯 Hedef Sınav:",
        "subject_label": "📚 Ders seçin:", "mood_status": {"great": "Harika 🔥", "normal": "Normal 😊", "tired": "Yorgun 😴"},
        "exams": ["Mezuniyet", "Yüksek Lisans", "YÖS / SAT", "Diğer"], "subjects": ["Türkçe", "Matematik", "Fen", "Diğer"]
    },
    "English": {
        "welcome": "Welcome to EduBalance", "user_label": "👤 Username:", "user_placeholder": "Enter your name...",
        "profile": "Create Profile", "daily": "Daily Stats", "study": "Study Session", "schedule": "📅 Smart Schedule",
        "playlist": "📺 Playlists", "motivation": "🔥 Motivation", "save": "Save Data", "success": "Data saved successfully!",
        "error_user": "Please enter username and press Enter!", "mood_label": "Estimated Mood:",
        "sleep_label": "🌙 Sleep (Hours):", "water_label": "💧 Water (Liters):", "target_label": "🎯 Target Exam:",
        "subject_label": "📚 Select Subject:", "mood_status": {"great": "Great 🔥", "normal": "Normal 😊", "tired": "Tired 😴"},
        "exams": ["Graduation", "Master's", "SAT", "Other"], "subjects": ["Math", "English", "Science", "Other"]
    },
    # Qeyd: Digər dillər (Fransız, İspan, İtalyan, Alman, Rus) üçün də bura eyni qaydada t'ləri əlavə edə bilərsən
    "Français": {
        "welcome": "Bienvenue sur EduBalance", "user_label": "👤 Nom d'utilisateur:", "user_placeholder": "Entrez votre nom...",
        "profile": "Créer un profil", "daily": "Stats Quotidiennes", "study": "Session d'Étude", "schedule": "📅 Calendrier",
        "playlist": "📺 Playlists", "motivation": "🔥 Motivation", "save": "Enregistrer", "success": "Succès!",
        "error_user": "Entrez votre nom!", "mood_label": "Humeur:", "sleep_label": "🌙 Sommeil:", "water_label": "💧 Eau:",
        "target_label": "🎯 Examen:", "subject_label": "📚 Matière:", "mood_status": {"great": "Super 🔥", "normal": "Normal 😊", "tired": "Fatigué 😴"},
        "exams": ["Diplôme", "Master", "SAT", "Autre"], "subjects": ["Français", "Maths", "Science", "Autre"]
    },
    "Español": { "welcome": "Bienvenido a EduBalance", "user_label": "👤 Usuario:", "profile": "Perfil", "daily": "Estadísticas", "study": "Estudio", "schedule": "📅 Horario Inteligente", "playlist": "📺 Listas", "motivation": "🔥 Motivación", "save": "Guardar", "success": "¡Guardado!", "error_user": "¡Ingrese nombre!", "mood_label": "Ánimo:", "sleep_label": "🌙 Sueño:", "water_label": "💧 Agua:", "target_label": "🎯 Examen:", "subject_label": "📚 Materia:", "mood_status": {"great": "Genial 🔥", "normal": "Normal 😊", "tired": "Cansado 😴"}, "exams": ["Graduación", "SAT", "Otros"], "subjects": ["Español", "Mates", "Otros"] },
    "Italiano": { "welcome": "Benvenuti su EduBalance", "user_label": "👤 Nome:", "profile": "Profilo", "daily": "Statistiche", "study": "Studio", "schedule": "📅 Programma", "playlist": "📺 Playlist", "motivation": "🔥 Motivazione", "save": "Salva", "success": "Salvato!", "error_user": "Inserisci nome!", "mood_label": "Umore:", "sleep_label": "🌙 Sonno:", "water_label": "💧 Acqua:", "target_label": "🎯 Esame:", "subject_label": "📚 Materia:", "mood_status": {"great": "Ottimo 🔥", "normal": "Normale 😊", "tired": "Stanco 😴"}, "exams": ["Laurea", "SAT", "Altro"], "subjects": ["Italiano", "Matematica", "Altro"] },
    "Deutsch": { "welcome": "Willkommen bei EduBalance", "user_label": "👤 Name:", "profile": "Profil", "daily": "Statistiken", "study": "Lernen", "schedule": "📅 Planer", "playlist": "📺 Playlisten", "motivation": "🔥 Motivation", "save": "Speichern", "success": "Gespeichert!", "error_user": "Name eingeben!", "mood_label": "Stimmung:", "sleep_label": "🌙 Schlaf:", "water_label": "💧 Wasser:", "target_label": "🎯 Prüfung:", "subject_label": "📚 Fach:", "mood_status": {"great": "Super 🔥", "normal": "Normal 😊", "tired": "Müde 😴"}, "exams": ["Abschluss", "SAT", "Andere"], "subjects": ["Deutsch", "Mathe", "Andere"] },
    "Русский": { "welcome": "Добро пожаловать в EduBalance", "user_label": "👤 Имя:", "profile": "Профиль", "daily": "Статистика", "study": "Учеба", "schedule": "📅 План", "playlist": "📺 Плейлисты", "motivation": "🔥 Мотивация", "save": "Сохранить", "success": "Сохранено!", "error_user": "Введите имя!", "mood_label": "Настроение:", "sleep_label": "🌙 Сон:", "water_label": "💧 Вода:", "target_label": "🎯 Экзамен:", "subject_label": "📚 Предмет:", "mood_status": {"great": "Отлично 🔥", "normal": "Нормально 😊", "tired": "Усталость 😴"}, "exams": ["Выпускной", "SAT", "Другое"], "subjects": ["Язык", "Математика", "Другое"] }
}

t = texts.get(lang, texts["Azerbaycan"])
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI
user_input = st.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])
if user_input:
    st.session_state.user_name = user_input

if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

# TAB SİSTEMİ (6 TAB)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([t['profile'], t['daily'], t['study'], t['schedule'], t['playlist'], t['motivation']])

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

# --- TAB 4: AĞILLI CƏDVƏL (ALQORİTM) ---
with tab4:
    st.subheader(t['schedule'])
    shift = st.radio("Növbəni seçin:", ["Səhər", "Günorta"])
    s_start = st.time_input("Dərs başlanğıcı:", datetime.time(8, 0))
    s_end = st.time_input("Dərs bitişi:", datetime.time(13, 0))

    if st.button("Optimal Planı Gör"):
        st.info("Sənin üçün ən sağlam gündəlik rejim:")
        if shift == "Səhər":
            wake = (datetime.combine(datetime.date.today(), s_start) - datetime.timedelta(hours=1, minutes=30)).time()
            st.write(f"☀️ **Oyanış:** {wake.strftime('%H:%M')}")
            st.write(f"🏫 **Məktəb:** {s_start.strftime('%H:%M')} - {s_end.strftime('%H:%M')}")
            st.write(f"😴 **Dincəlmə:** {s_end.strftime('%H:%M')} - 1.5 saat")
            st.write(f"✍️ **Əsas Dərs Vaxtı:** 16:30 - 19:30")
            st.write(f"🌙 **Yatış:** 22:30 (Məsləhətdir)")
        else:
            st.write(f"☀️ **Oyanış:** 08:00")
            st.write(f"✍️ **Əsas Dərs Vaxtı:** 09:30 - 12:00 (Ən məhsuldar)")
            st.write(f"🏫 **Məktəb:** {s_start.strftime('%H:%M')} - {s_end.strftime('%H:%M')}")
            st.write(f"🌙 **Yatış:** 23:30")

# --- TAB 5: PLAYLISTLƏR ---
with tab5:
    st.subheader(t['playlist'])
    st.info("Fənlər üzrə seçilmiş dərslər tezliklə bura əlavə olunacaq.")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Nümunə

# --- TAB 6: MOTİVASİYA ---
with tab6:
    st.subheader(t['motivation'])
    st.write("💡 **Günün Faktı:** Beyin gün ərzində öyrəndiklərini yuxuda sistemləşdirir. Yuxuna fikir ver!")
    if st.button("Uğur Hekayəsi Oxu"):
        st.write("📖 *Steve Jobs öz qarajında başladığı işi dünya nəhənginə çevirdi. Sənin qarajın isə sənin iş masandır!*")

st.divider()
st.caption("EduBalance v2.0 | Multi-Language & Smart Logic 🚀")
