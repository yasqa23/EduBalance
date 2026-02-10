import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance Global", layout="centered")

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_video" not in st.session_state:
    st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"

# 2. 8 DİLLİ LÜĞƏT SİSTEMİ (Bütün bölmələr daxil)
lang = st.sidebar.selectbox("🌐 Choose Language / Dil seçin", 
    ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz", "profile": "Profil", "daily": "Statistika", "study": "Dərs", "schedule": "Cədvəl", "playlist": "Musiqi", "motivation": "Motivasiya",
        "user_label": "👤 İstifadəçi adı:", "user_placeholder": "Adınızı yazın...", "save": "Yadda saxla", "success": "Uğurla tamamlandı!", "error_user": "Adınızı yazın!",
        "mood_label": "Əhval:", "sleep_label": "🌙 Yuxu (Saat):", "water_label": "💧 Su (Litr):", "target_label": "🎯 Hədəf imtahan:", "subject_label": "📚 Fənn:",
        "shift_label": "Növbəni seçin:", "shift_m": "Səhər", "shift_a": "Günorta", "calc_btn": "Optimal Planı Hesabla",
        "wake": "☀️ Oyanış", "school": "🏫 Məktəb/Uni", "rest": "😴 Dincəlmə", "study_time": "✍️ Əsas Dərs Vaxtı", "sleep": "🌙 Yatış",
        "music_title": "🎧 Fokuslanma Musiqisi", "lofi": "Lofi Fokus", "nature": "Təbiət", "deep": "Dərin Diqqət", "add_link": "Öz YouTube linkini əlavə et:",
        "fact_title": "💡 Günün Faktı:", "fact": "Beyin öyrəndiklərini yuxuda sistemləşdirir. Yuxuna fikir ver!", "story_btn": "Uğur Hekayəsi Oxu"
    },
    "Türkçe": {
        "welcome": "EduBalance'a Hoş Geldiniz", "profile": "Profil", "daily": "İstatistik", "study": "Ders", "schedule": "Program", "playlist": "Müzik", "motivation": "Motivasyon",
        "user_label": "👤 Kullanıcı adı:", "user_placeholder": "Adınızı girin...", "save": "Kaydet", "success": "Başarıyla tamamlandı!", "error_user": "Adınızı girin!",
        "mood_label": "Ruh Hali:", "sleep_label": "🌙 Uyku (Saat):", "water_label": "💧 Su (Litre):", "target_label": "🎯 Hedef Sınav:", "subject_label": "📚 Ders:",
        "shift_label": "Vardiya seçin:", "shift_m": "Sabah", "shift_a": "Öğle", "calc_btn": "Optimal Planı Hesapla",
        "wake": "☀️ Uyanış", "school": "🏫 Okul/Uni", "rest": "😴 Dinlenme", "study_time": "✍️ Ana Çalışma Vakti", "sleep": "🌙 Uyku Vakti",
        "music_title": "🎧 Odaklanma Müziği", "lofi": "Lofi Odak", "nature": "Doğa", "deep": "Derin Odak", "add_link": "Kendi YouTube linkini ekle:",
        "fact_title": "💡 Günün Bilgisi:", "fact": "Beyin öğrendiklerini uykuda düzenler. Uykunuza dikkat edin!", "story_btn": "Başarı Hikayesi Oku"
    },
    "English": {
        "welcome": "Welcome to EduBalance", "profile": "Profile", "daily": "Stats", "study": "Study", "schedule": "Schedule", "playlist": "Music", "motivation": "Motivation",
        "user_label": "👤 Username:", "user_placeholder": "Enter your name...", "save": "Save", "success": "Success!", "error_user": "Enter your name!",
        "mood_label": "Mood:", "sleep_label": "🌙 Sleep (Hours):", "water_label": "💧 Water (Liters):", "target_label": "🎯 Target Exam:", "subject_label": "📚 Subject:",
        "shift_label": "Select Shift:", "shift_m": "Morning", "shift_a": "Afternoon", "calc_btn": "Calculate Optimal Plan",
        "wake": "☀️ Wake up", "school": "🏫 School/Uni", "rest": "😴 Resting", "study_time": "✍️ Main Study Time", "sleep": "🌙 Bedtime",
        "music_title": "🎧 Focus Music", "lofi": "Lofi Focus", "nature": "Nature", "deep": "Deep Focus", "add_link": "Add your YouTube link:",
        "fact_title": "💡 Daily Fact:", "fact": "The brain organizes what it learns during sleep. Watch your sleep!", "story_btn": "Read Success Story"
    },
    "Español": {
        "welcome": "Bienvenido a EduBalance", "profile": "Perfil", "daily": "Estadísticas", "study": "Estudio", "schedule": "Horario", "playlist": "Música", "motivation": "Motivación",
        "user_label": "👤 Usuario:", "user_placeholder": "Tu nombre...", "save": "Guardar", "success": "¡Éxito!", "error_user": "¡Ingrese nombre!",
        "mood_label": "Ánimo:", "sleep_label": "🌙 Sueño (Horas):", "water_label": "💧 Agua (Litros):", "target_label": "🎯 Examen:", "subject_label": "📚 Materia:",
        "shift_label": "Turno:", "shift_m": "Mañana", "shift_a": "Tarde", "calc_btn": "Calcular Plan Óptimo",
        "wake": "☀️ Despertar", "school": "🏫 Escuela", "rest": "😴 Descanso", "study_time": "✍️ Tiempo de Estudio", "sleep": "🌙 Dormir",
        "music_title": "🎧 Música para enfocar", "lofi": "Lofi", "nature": "Naturaleza", "deep": "Enfoque Profundo", "add_link": "Añadir link de YouTube:",
        "fact_title": "💡 Dato del día:", "fact": "¡El cerebro organiza lo aprendido mientras duermes!", "story_btn": "Leer historia de éxito"
    },
    "Italiano": {
        "welcome": "Benvenuti in EduBalance", "profile": "Profilo", "daily": "Statistiche", "study": "Studio", "schedule": "Programma", "playlist": "Musica", "motivation": "Motivazione",
        "user_label": "👤 Nome:", "user_placeholder": "Tuo nome...", "save": "Salva", "success": "Fatto!", "error_user": "Inserisci nome!",
        "mood_label": "Umore:", "sleep_label": "🌙 Sonno (Ore):", "water_label": "💧 Acqua (Litri):", "target_label": "🎯 Esame:", "subject_label": "📚 Materia:",
        "shift_label": "Turno:", "shift_m": "Mattina", "shift_a": "Pomeriggio", "calc_btn": "Calcola Piano",
        "wake": "☀️ Sveglia", "school": "🏫 Scuola", "rest": "😴 Riposo", "study_time": "✍️ Studio Principale", "sleep": "🌙 Dormire",
        "music_title": "🎧 Musica Focus", "lofi": "Lofi", "nature": "Natura", "deep": "Focus Profondo", "add_link": "Aggiungi link YouTube:",
        "fact_title": "💡 Curiosità:", "fact": "Il cervello rielabora le informazioni nel sonno!", "story_btn": "Leggi storia di successo"
    },
    "Français": {
        "welcome": "Bienvenue sur EduBalance", "profile": "Profil", "daily": "Stats", "study": "Étude", "schedule": "Calendrier", "playlist": "Musique", "motivation": "Motivation",
        "user_label": "👤 Nom:", "user_placeholder": "Ton nom...", "save": "Enregistrer", "success": "Succès!", "error_user": "Entrez votre nom!",
        "mood_label": "Humeur:", "sleep_label": "🌙 Sommeil (H):", "water_label": "💧 Eau (L):", "target_label": "🎯 Examen:", "subject_label": "📚 Matière:",
        "shift_label": "Horaire:", "shift_m": "Matin", "shift_a": "Après-midi", "calc_btn": "Calculer le plan",
        "wake": "☀️ Réveil", "school": "🏫 École", "rest": "😴 Repos", "study_time": "✍️ Temps d'étude", "sleep": "🌙 Sommeil",
        "music_title": "🎧 Musique Focus", "lofi": "Lofi", "nature": "Nature", "deep": "Focus Profond", "add_link": "Ajouter lien YouTube:",
        "fact_title": "💡 Fait du jour:", "fact": "Le cerveau traite les infos pendant le sommeil!", "story_btn": "Lire un succès"
    },
    "Deutsch": {
        "welcome": "Willkommen bei EduBalance", "profile": "Profil", "daily": "Statistik", "study": "Lernen", "schedule": "Planer", "playlist": "Musik", "motivation": "Motivation",
        "user_label": "👤 Name:", "user_placeholder": "Dein Name...", "save": "Speichern", "success": "Erfolg!", "error_user": "Name eingeben!",
        "mood_label": "Stimmung:", "sleep_label": "🌙 Schlaf (Std):", "water_label": "💧 Wasser (L):", "target_label": "🎯 Prüfung:", "subject_label": "📚 Fach:",
        "shift_label": "Schicht:", "shift_m": "Morgen", "shift_a": "Nachmittag", "calc_btn": "Plan berechnen",
        "wake": "☀️ Aufstehen", "school": "🏫 Schule", "rest": "😴 Pause", "study_time": "✍️ Lernzeit", "sleep": "🌙 Schlafen",
        "music_title": "🎧 Fokus-Musik", "lofi": "Lofi", "nature": "Natur", "deep": "Tiefer Fokus", "add_link": "YouTube Link hinzufügen:",
        "fact_title": "💡 Fakt des Tages:", "fact": "Das Gehirn lernt im Schlaf weiter!", "story_btn": "Erfolgsgeschichte"
    },
    "Русский": {
        "welcome": "Добро пожаловать в EduBalance", "profile": "Профиль", "daily": "Статистика", "study": "Учеба", "schedule": "План", "playlist": "Музыка", "motivation": "Мотивация",
        "user_label": "👤 Имя:", "user_placeholder": "Ваше имя...", "save": "Сохранить", "success": "Успешно!", "error_user": "Введите имя!",
        "mood_label": "Настроение:", "sleep_label": "🌙 Сон (Ч):", "water_label": "💧 Вода (Л):", "target_label": "🎯 Экзамен:", "subject_label": "📚 Предмет:",
        "shift_label": "Смена:", "shift_m": "Утро", "shift_a": "День", "calc_btn": "Рассчитать план",
        "wake": "☀️ Подъем", "school": "🏫 Учеба", "rest": "😴 Отдых", "study_time": "✍️ Время учебы", "sleep": "🌙 Сон",
        "music_title": "🎧 Музыка для учебы", "lofi": "Лофи", "nature": "Природа", "deep": "Концентрация", "add_link": "Добавить ссылку YouTube:",
        "fact_title": "💡 Факт дня:", "fact": "Мозг систематизирует знания во сне!", "story_btn": "История успеха"
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ GİRİŞİ
user_input = st.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])
if user_input: st.session_state.user_name = user_input
if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([t['profile'], t['daily'], t['study'], t['schedule'], t['playlist'], t['motivation']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox(t['target_label'], ["Buraxılış", "SAT", "YÖS", "MİQ", "Other"])
    if st.button(f"➕ {t['profile']}"):
        supabase.table("students_profiles").upsert({"username": st.session_state.user_name, "Language": lang, "target_exam": target}, on_conflict="username").execute()
        st.balloons(); st.success(t['success'])

# --- TAB 2: GÜNLÜK STATS ---
with tab2:
    sl = st.slider(t['sleep_label'], 0.0, 12.0, 8.0); wt = st.number_input(t['water_label'], 0.0, 5.0, 1.5)
    score = (60 if 7 <= sl <= 9 else 30) + (40 if wt >= 2 else 15)
    mood = "🔥" if score >= 90 else "😊" if score >= 60 else "😴"
    st.metric(t['mood_label'], mood)
    if st.button(f"💾 {t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            supabase.table("daily_stats").insert({"user_ID": res.data[0]['id'], "sleep_hours": sl, "mood": mood, "water_liters": wt}).execute()
            st.success(t['success'])

# --- TAB 3: DƏRS ---
with tab3:
    sub = st.selectbox(t['subject_label'], ["Math", "English", "History", "Physics", "Chemistry", "Biology"])
    dur = st.number_input("⏱️ (min):", 10, 300, 45)
    if st.button(f"📖 {t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            supabase.table("study_sessions").insert({"user_ID": res.data[0]['id'], "subject": sub, "duration_time": dur}).execute()
            st.success(t['success'])

# --- TAB 4: AĞILLI CƏDVƏL (7 DİLLƏ) ---
with tab4:
    st.subheader(t['schedule'])
    sh = st.radio(t['shift_label'], [t['shift_m'], t['shift_a']])
    s_start = st.time_input("Start:", datetime.time(8, 0)); s_end = st.time_input("End:", datetime.time(13, 0))
    if st.button(t['calc_btn']):
        st.divider()
        if sh == t['shift_m']:
            wk = (datetime.combine(datetime.date.today(), s_start) - datetime.timedelta(hours=1, minutes=30)).time()
            st.write(f"{t['wake']}: {wk.strftime('%H:%M')}")
            st.write(f"{t['school']}: {s_start.strftime('%H:%M')} - {s_end.strftime('%H:%M')}")
            st.write(f"{t['rest']}: {s_end.strftime('%H:%M')} - 1.5h")
            st.write(f"**{t['study_time']}: 16:30 - 19:30**")
        else:
            st.write(f"{t['wake']}: 08:00")
            st.write(f"**{t['study_time']}: 09:30 - 12:00**")
            st.write(f"{t['school']}: {s_start.strftime('%H:%M')} - {s_end.strftime('%H:%M')}")
        st.write(f"{t['sleep']}: 23:00")

# --- TAB 5: MUSİQİ (PLAYLIST) ---
with tab5:
    st.subheader(t['music_title'])
    c1, c2, c3 = st.columns(3)
    if c1.button(t['lofi']): st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
    if c2.button(t['nature']): st.session_state.current_video = "https://www.youtube.com/watch?v=mPZkdNFqeps"
    if c3.button(t['deep']): st.session_state.current_video = "https://www.youtube.com/watch?v=4mS_r0D999U"
    u_link = st.text_input(t['add_link'])
    if st.button("➕"): st.session_state.current_video = u_link
    st.video(st.session_state.current_video)

# --- TAB 6: MOTİVASİYA ---
with tab6:
    st.subheader(t['motivation'])
    st.write(f"**{t['fact_title']}** {t['fact']}")
    if st.button(t['story_btn']):
        st.info("📖 'The expert in anything was once a beginner.' - Keep going!")

st.divider()
st.caption("EduBalance v2.5 | Global Edition 🌍")
