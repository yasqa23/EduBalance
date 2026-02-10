import streamlit as st
from supabase import create_client
import datetime
import pandas as pd

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance Pro", layout="wide")

# Sessiya yaddaşı (Xətaların qarşısını almaq üçün)
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_video" not in st.session_state:
    st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"

# 2. 8 DİLLİ LÜĞƏT SİSTEMİ
lang = st.sidebar.selectbox("🌐 Choose Language / Dil seçin", 
    ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance Pro-ya Xoş Gəldiniz", "profile": "Profil", "daily": "Statistika", "study": "Dərs", "schedule": "Cədvəl", "playlist": "Musiqi", "motivation": "Motivasiya",
        "user_label": "👤 İstifadəçi adı:", "user_placeholder": "Adınızı daxil edin...", "save": "Yadda saxla", "success": "Uğurla tamamlandı!", "error_user": "Davam etmək üçün adınızı yazıb Enter basın!",
        "mood_label": "Təxmin edilən Əhval:", "sleep_label": "🌙 Yuxu (Saat):", "water_label": "💧 Su (Litr):", "target_label": "🎯 Hədəf İmtahan:", "subject_label": "📚 Fənn:",
        "shift_label": "Növbəni seçin:", "shift_m": "Səhər", "shift_a": "Günorta", "calc_btn": "Planı Hesabla", "wake": "☀️ Oyanış", "school": "🏫 Dərs saatı", "rest": "😴 Dincəlmə", "study_time": "✍️ Əsas Dərs", "sleep": "🌙 Yatış",
        "music_title": "🎧 Fokus Musiqisi", "lofi": "Lofi Fokus", "nature": "Təbiət", "deep": "Dərin Diqqət", "add_link": "YouTube linki:", "fact_title": "💡 Günün Faktı:", "story_btn": "Motivasiya Sözü"
    },
    "Türkçe": {
        "welcome": "EduBalance Pro'ya Hoş Geldiniz", "profile": "Profil", "daily": "İstatistik", "study": "Ders", "schedule": "Program", "playlist": "Müzik", "motivation": "Motivasyon",
        "user_label": "👤 Kullanıcı adı:", "user_placeholder": "Adınızı girin...", "save": "Kaydet", "success": "Başarıyla tamamlandı!", "error_user": "Devam etmek için adınızı girin!",
        "mood_label": "Ruh Hali:", "sleep_label": "🌙 Uyku (Saat):", "water_label": "💧 Su (Litre):", "target_label": "🎯 Hedef Sınav:", "subject_label": "📚 Ders:",
        "shift_label": "Vardiya:", "shift_m": "Sabah", "shift_a": "Öğle", "calc_btn": "Programı Hesapla", "wake": "☀️ Uyanış", "school": "🏫 Okul", "rest": "😴 Dinlenme", "study_time": "✍️ Ana Ders", "sleep": "🌙 Yatış",
        "music_title": "🎧 Odaklanma Müziği", "lofi": "Lofi Odak", "nature": "Doğa", "deep": "Derin Odak", "add_link": "YouTube linki:", "fact_title": "💡 Günün Bilgisi:", "story_btn": "Motivasyon Sözü"
    },
    "English": {
        "welcome": "Welcome to EduBalance Pro", "profile": "Profile", "daily": "Analytics", "study": "Study", "schedule": "Schedule", "playlist": "Music", "motivation": "Motivation",
        "user_label": "👤 Username:", "user_placeholder": "Enter your name...", "save": "Save", "success": "Success!", "error_user": "Please enter username!",
        "mood_label": "Mood:", "sleep_label": "🌙 Sleep (Hours):", "water_label": "💧 Water (Liters):", "target_label": "🎯 Target Exam:", "subject_label": "📚 Subject:",
        "shift_label": "Select Shift:", "shift_m": "Morning", "shift_a": "Afternoon", "calc_btn": "Calculate Plan", "wake": "☀️ Wake up", "school": "🏫 School", "rest": "😴 Resting", "study_time": "✍️ Main Study", "sleep": "🌙 Bedtime",
        "music_title": "🎧 Focus Music", "lofi": "Lofi Focus", "nature": "Nature", "deep": "Deep Focus", "add_link": "YouTube link:", "fact_title": "💡 Daily Fact:", "story_btn": "Motivation Quote"
    },
    # Digər dillər üçün (ES, IT, FR, DE, RU) v2.5-dəki tərcümələri bura daxil edə bilərsən. 
    # Kodun qısa olması üçün bura 3 əsas dili qoydum, amma struktur hazırdır.
}

t = texts.get(lang, texts["Azerbaycan"])
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ GİRİŞİ
user_input = st.sidebar.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])
if user_input:
    st.session_state.user_name = user_input

if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

# TAB STRUKTURU
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([t['profile'], t['daily'], t['study'], t['schedule'], t['playlist'], t['motivation']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox(t['target_label'], ["Buraxılış", "SAT", "YÖS", "MİQ", "Magistratura"])
    if st.button(f"➕ {t['profile']}"):
        supabase.table("students_profiles").upsert({"username": st.session_state.user_name, "Language": lang, "target_exam": target}, on_conflict="username").execute()
        st.balloons(); st.success(t['success'])

# --- TAB 2: ANALİTİKA (XƏTASIZ QRAFİK) ---
with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        sl_dur = st.slider(t['sleep_label'], 0.0, 12.0, 8.0)
        wt_lit = st.number_input(t['water_label'], 0.0, 5.0, 1.5)
        if st.button(f"💾 {t['save']} (Health)"):
            res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
            if res.data:
                supabase.table("daily_stats").insert({"user_ID": res.data[0]['id'], "sleep_hours": sl_dur, "water_liters": wt_lit}).execute()
                st.success(t['success'])
    
    with col2:
        res_p = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res_p.data:
            stats = supabase.table("daily_stats").select("created_at, sleep_hours").eq("user_ID", res_p.data[0]['id']).execute()
            if stats.data:
                df = pd.DataFrame(stats.data)
                df['created_at'] = pd.to_datetime(df['created_at']).dt.date
                st.line_chart(df.set_index('created_at'))
            else: st.info("Hələ ki qrafik məlumatı yoxdur.")

# --- TAB 3: DƏRS (BAR CHART) ---
with tab3:
    sub_choice = st.selectbox(t['subject_label'], ["Riyaziyyat", "İngilis", "Fizika", "Tarix"])
    dur_min = st.number_input("⏱️ (min):", 10, 300, 45)
    if st.button(f"📖 {t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            supabase.table("study_sessions").insert({"user_ID": res.data[0]['id'], "subject": sub_choice, "duration_time": dur_min}).execute()
            st.rerun()

    study_data = supabase.table("study_sessions").select("subject, duration_time").execute()
    if study_data.data:
        sdf = pd.DataFrame(study_data.data)
        st.bar_chart(sdf.groupby('subject').sum())

# --- TAB 4: AĞILLI CƏDVƏL ---
with tab4:
    sh = st.radio(t['shift_label'], [t['shift_m'], t['shift_a']])
    s_time = st.time_input("Start:", datetime.time(8, 0))
    e_time = st.time_input("End:", datetime.time(13, 0))
    if st.button(t['calc_btn']):
        st.info("🎯 Sənin Optimal Rejimin:")
        if sh == t['shift_m']:
            st.write(f"{t['wake']}: 06:30 | {t['school']}: {s_time} - {e_time} | {t['study_time']}: 17:00 - 20:00")
        else:
            st.write(f"{t['wake']}: 08:00 | {t['study_time']}: 09:30 - 12:00 | {t['school']}: {s_time} - {e_time}")

# --- TAB 5: PLAYLIST (ÖZÜN ƏLAVƏ ET) ---
with tab5:
    st.subheader(t['music_title'])
    c1, c2, c3 = st.columns(3)
    if c1.button(t['lofi']): st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
    if c2.button(t['nature']): st.session_state.current_video = "https://www.youtube.com/watch?v=mPZkdNFqeps"
    if c3.button(t['deep']): st.session_state.current_video = "https://www.youtube.com/watch?v=4mS_r0D999U"
    
    custom_url = st.text_input(t['add_link'], placeholder="YouTube linkini yapışdır...")
    if st.button("OK"):
        if custom_url: st.session_state.current_video = custom_url
    
    st.video(st.session_state.current_video)

# --- TAB 6: MOTİVASİYA ---
with tab6:
    st.write(f"**{t['fact_title']}** {t['fact']}")
    if st.button(t['story_btn']):
        st.success("💪 'Məqsədi olmayan gəmiyə heç bir külək kömək etməz.' - Sənin məqsədin artıq bəllidir!")

st.divider()
st.caption("EduBalance v3.1 | Yüksək Performans Rejimi 🚀")
