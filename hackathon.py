import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance Pro", layout="wide")

# Sessiya yaddaşı
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "current_video" not in st.session_state: st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"

# 2. 8 DİLLİ TAM TƏRCÜMƏ SİSTEMİ
lang = st.sidebar.selectbox("🌐 Dil / Language", ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance Pro", "profile": "Profil", "daily": "Statistika", "study": "Dərs", "schedule": "Cədvəl", "playlist": "Musiqi", "motivation": "Motivasiya",
        "user_label": "👤 İstifadəçi adı:", "save": "Yadda saxla", "success": "Uğurla tamamlandı!", "error_user": "Adınızı daxil edin!",
        "sleep": "🌙 Yuxu (Saat)", "water": "💧 Su (Litr)", "target": "🎯 Hədəf", "subject": "📚 Fənn",
        "shift": "Növbə:", "morn": "Səhər", "aft": "Günorta", "calc": "Hesabla", "music": "🎧 Fokus", "link": "YouTube Linki", "fact": "💡 Günün Faktı"
    },
    "Türkçe": {
        "welcome": "EduBalance Pro", "profile": "Profil", "daily": "Analiz", "study": "Ders", "schedule": "Program", "playlist": "Müzik", "motivation": "Motivasyon",
        "user_label": "👤 Kullanıcı adı:", "save": "Kaydet", "success": "Tamamlandı!", "error_user": "Adınızı girin!",
        "sleep": "🌙 Uyku (Saat)", "water": "💧 Su (Litre)", "target": "🎯 Hedef", "subject": "📚 Ders",
        "shift": "Vardiya:", "morn": "Sabah", "aft": "Öğle", "calc": "Hesapla", "music": "🎧 Odak", "link": "YouTube Linki", "fact": "💡 Günün Bilgisi"
    },
    "English": {
        "welcome": "EduBalance Pro", "profile": "Profile", "daily": "Analytics", "study": "Study", "schedule": "Schedule", "playlist": "Music", "motivation": "Motivation",
        "user_label": "👤 Username:", "save": "Save", "success": "Success!", "error_user": "Enter name!",
        "sleep": "🌙 Sleep (Hours)", "water": "💧 Water (Liters)", "target": "🎯 Target", "subject": "📚 Subject",
        "shift": "Shift:", "morn": "Morning", "aft": "Afternoon", "calc": "Calculate", "music": "🎧 Focus", "link": "YouTube Link", "fact": "💡 Daily Fact"
    },
    "Español": { "welcome": "EduBalance Pro", "profile": "Perfil", "daily": "Estadísticas", "study": "Estudio", "schedule": "Horario", "playlist": "Música", "motivation": "Motivación", "user_label": "👤 Usuario:", "save": "Guardar", "success": "¡Éxito!", "error_user": "¡Nombre!", "sleep": "🌙 Sueño", "water": "💧 Agua", "target": "🎯 Meta", "subject": "📚 Materia", "shift": "Turno:", "morn": "Mañana", "aft": "Tarde", "calc": "Calcular", "music": "🎧 Enfoque", "link": "YouTube Link", "fact": "💡 Dato" },
    "Italiano": { "welcome": "EduBalance Pro", "profile": "Profilo", "daily": "Statistiche", "study": "Studio", "schedule": "Programma", "playlist": "Musica", "motivation": "Motivazione", "user_label": "👤 Nome:", "save": "Salva", "success": "Fatto!", "error_user": "Nome!", "sleep": "🌙 Sonno", "water": "💧 Acqua", "target": "🎯 Obiettivo", "subject": "📚 Materia", "shift": "Turno:", "morn": "Mattina", "aft": "Pomeriggio", "calc": "Calcola", "music": "🎧 Focus", "link": "YouTube Link", "fact": "💡 Curiosità" },
    "Français": { "welcome": "EduBalance Pro", "profile": "Profil", "daily": "Stats", "study": "Étude", "schedule": "Calendrier", "playlist": "Musique", "motivation": "Motivation", "user_label": "👤 Nom:", "save": "Enregistrer", "success": "Succès!", "error_user": "Nom!", "sleep": "🌙 Sommeil", "water": "💧 Eau", "target": "🎯 Examen", "subject": "📚 Matière", "shift": "Horaire:", "morn": "Matin", "aft": "Après-midi", "calc": "Calculer", "music": "🎧 Focus", "link": "YouTube Link", "fact": "💡 Fait" },
    "Deutsch": { "welcome": "EduBalance Pro", "profile": "Profil", "daily": "Statistik", "study": "Lernen", "schedule": "Planer", "playlist": "Musik", "motivation": "Motivation", "user_label": "👤 Name:", "save": "Speichern", "success": "Erfolg!", "error_user": "Name!", "sleep": "🌙 Schlaf", "water": "💧 Wasser", "target": "🎯 Ziel", "subject": "📚 Fach", "shift": "Schicht:", "morn": "Morgen", "aft": "Nachmittag", "calc": "Berechnen", "music": "🎧 Fokus", "link": "YouTube Link", "fact": "💡 Fakt" },
    "Русский": { "welcome": "EduBalance Pro", "profile": "Профиль", "daily": "Статистика", "study": "Учеба", "schedule": "План", "playlist": "Музыка", "motivation": "Мотивация", "user_label": "👤 Имя:", "save": "Сохранить", "success": "Успешно!", "error_user": "Имя!", "sleep": "🌙 Сон", "water": "💧 Вода", "target": "🎯 Цель", "subject": "📚 Предмет", "shift": "Смена:", "morn": "Утро", "aft": "День", "calc": "Рассчитать", "music": "🎧 Фокус", "link": "YouTube Link", "fact": "💡 Фаkt" }
}

t = texts.get(lang, texts["Azerbaycan"])
st.title(f"🚀 {t['welcome']}")

# 3. İSTİFADƏÇİ GİRİŞİ
user_input = st.sidebar.text_input(t['user_label'], value=st.session_state.user_name)
if user_input: st.session_state.user_name = user_input
if not st.session_state.user_name:
    st.warning(t['error_user']); st.stop()

# Profil ID-sini çəkmək
res_prof = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
u_id = res_prof.data[0]['id'] if (res_prof.data and len(res_prof.data) > 0) else None

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([t['profile'], t['daily'], t['study'], t['schedule'], t['playlist'], t['motivation']])

# --- TAB 1: PROFİL ---
with tab1:
    target_ex = st.selectbox(t['target'], ["Buraxılış", "SAT", "YÖS", "MİQ", "Other"])
    if st.button(f"➕ {t['profile']}"):
        supabase.table("students_profiles").upsert({"username": st.session_state.user_name, "Language": lang, "target_exam": target_ex}, on_conflict="username").execute()
        st.balloons(); st.success(t['success'])

# --- TAB 2: ANALİTİKA (PANDAS-SIZ) ---
with tab2:
    c1, c2 = st.columns([1, 2])
    with c1:
        sl = st.slider(t['sleep'], 0.0, 12.0, 8.0)
        wt = st.number_input(t['water'], 0.0, 5.0, 2.0)
        if st.button(t['save']):
            if u_id:
                supabase.table("daily_stats").insert({"user_ID": u_id, "sleep_hours": sl, "water_liters": wt}).execute()
                st.rerun()
    with c2:
        if u_id:
            stats_data = supabase.table("daily_stats").select("sleep_hours").eq("user_ID", u_id).limit(10).execute()
            if stats_data.data:
                # Pandas olmadan qrafik: Siyahıdan istifadə edirik
                chart_data = [d['sleep_hours'] for d in stats_data.data]
                st.line_chart(chart_data)
                st.caption("Son 10 günlük yuxu qrafiki")
            else: st.info("Hələ məlumat daxil edilməyib.")

# --- TAB 3: DƏRS (PANDAS-SIZ) ---
with tab3:
    col_a, col_b = st.columns([1, 2])
    with col_a:
        subjects_list = ["Math", "English", "Science", "History", "Physics"]
        sb = st.selectbox(t['subject'], subjects_list)
        dr = st.number_input("Min:", 10, 300, 45)
        if st.button("📖 OK"):
            if u_id:
                supabase.table("study_sessions").insert({"user_ID": u_id, "subject": sb, "duration_time": dr}).execute()
                st.rerun()
    with col_b:
        if u_id:
            study_res = supabase.table("study_sessions").select("subject, duration_time").eq("user_ID", u_id).execute()
            if study_res.data:
                # Pandas-sız toplama (Aggregation)
                summary = {}
                for item in study_res.data:
                    s = item['subject']
                    d = item['duration_time']
                    summary[s] = summary.get(s, 0) + d
                st.bar_chart(summary)
            else: st.info("Dərs qeydi tapılmadı.")

# --- TAB 4: AĞILLI CƏDVƏL ---
with tab4:
    sh = st.radio(t['shift'], [t['morn'], t['aft']])
    if st.button(t['calc']):
        if sh == t['morn']: st.success("07:00 Wakeup | 08:00 School | 17:00 Deep Study")
        else: st.success("08:00 Wakeup | 10:00 Deep Study | 14:00 School")

# --- TAB 5: MUSİQİ ---
with tab5:
    st.subheader(t['music'])
    c_m1, c_m2 = st.columns(2)
    if c_m1.button("Lofi"): st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
    if c_m2.button("Nature"): st.session_state.current_video = "https://www.youtube.com/watch?v=mPZkdNFqeps"
    link_inp = st.text_input(t['link'], st.session_state.current_video)
    if st.button("Play"): st.session_state.current_video = link_inp
    st.video(st.session_state.current_video)

# --- TAB 6: MOTİVASİYA ---
with tab6:
    st.info(f"{t['fact']}: Beyin fokuslandığı zaman daha çox enerji sərf edir. Su içməyi unutma!")
    if st.button("Quote"): st.write("🚀 'Success is the sum of small efforts, repeated day in and day out.'")

st.divider()
st.caption("EduBalance v3.3 | No-Pandas Version 🚀")
