import streamlit as st
from supabase import create_client
import datetime
import pandas as pd # Qrafiklər üçün mütləqdir

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance Pro", layout="wide") # Daha geniş görünüş

# Sessiya yaddaşı
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_video" not in st.session_state:
    st.session_state.current_video = "https://www.youtube.com/watch?v=jfKfPfyJRdk"

# 2. 8 DİLLİ LÜĞƏT SİSTEMİ (Qrafik etiketləri daxil)
lang = st.sidebar.selectbox("🌐 Language / Dil", 
    ["Azerbaycan", "Türkçe", "English", "Español", "Italiano", "Français", "Deutsch", "Русский"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance Pro-ya Xoş Gəldiniz", "profile": "Profil", "daily": "Analitika", "study": "Dərs", "schedule": "Cədvəl", "playlist": "Musiqi", "motivation": "Motivasiya",
        "user_label": "👤 İstifadəçi adı:", "save": "Yadda saxla", "success": "Uğurla tamamlandı!", "error_user": "Ad daxil edin!",
        "graph_title": "📊 Həftəlik Tərəqqi", "sleep_label": "Yuxu", "water_label": "Su", "study_label": "Dərs (dəq)",
        "shift_m": "Səhər", "shift_a": "Günorta", "calc_btn": "Hesabla", "music_title": "🎧 Fokus Musiqisi"
    },
    "English": {
        "welcome": "Welcome to EduBalance Pro", "profile": "Profile", "daily": "Analytics", "study": "Study", "schedule": "Schedule", "playlist": "Music", "motivation": "Motivation",
        "user_label": "👤 Username:", "save": "Save", "success": "Saved successfully!", "error_user": "Enter username!",
        "graph_title": "📊 Weekly Progress", "sleep_label": "Sleep", "water_label": "Water", "study_label": "Study (min)",
        "shift_m": "Morning", "shift_a": "Afternoon", "calc_btn": "Calculate", "music_title": "🎧 Focus Music"
    },
    # Digər dillər üçün bura qısaldılmışdır, tam versiyada hər biri mövcuddur...
}
# Qeyd: Digər dilləri yuxarıdakı məntiqlə bura əlavə edə bilərsən (v2.5-dəki kimi)
t = texts.get(lang, texts["English"])

st.title(f"🚀 {t['welcome']}")

# 3. İSTİFADƏÇİ GİRİŞİ
user_input = st.sidebar.text_input(t['user_label'], value=st.session_state.user_name)
if user_input: st.session_state.user_name = user_input
if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([t['profile'], t['daily'], t['study'], t['schedule'], t['playlist'], t['motivation']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.selectbox("🎯 Target:", ["Buraxılış", "SAT", "YÖS", "MİQ"])
    if st.button(f"➕ {t['profile']}"):
        supabase.table("students_profiles").upsert({"username": st.session_state.user_name, "Language": lang, "target_exam": target}, on_conflict="username").execute()
        st.success(t['success'])

# --- TAB 2: ANALİTİKA (YENİ QRAFİK SİSTEMİ) ---
with tab2:
    st.subheader(t['graph_title'])
    
    # Supabase-dən məlumatları çəkmək
    res_prof = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
    if res_prof.data:
        u_id = res_prof.data[0]['id']
        
        # Günlük Stats Qrafiki
        stats_res = supabase.table("daily_stats").select("created_at, sleep_hours, water_liters").eq("user_ID", u_id).limit(7).execute()
        if stats_res.data:
            df = pd.DataFrame(stats_res.data)
            df['created_at'] = pd.to_datetime(df['created_at']).dt.date
            st.line_chart(df.set_index('created_at')[['sleep_hours', 'water_liters']])
        else:
            st.info("Qrafik üçün kifayət qədər məlumat yoxdur. Məlumat daxil edin!")

    # Yeni məlumat girişi
    st.divider()
    c1, c2 = st.columns(2)
    sl = c1.slider("🌙 Sleep", 0.0, 12.0, 8.0)
    wt = c2.number_input("💧 Water", 0.0, 5.0, 2.0)
    if st.button(f"💾 {t['save']}"):
        supabase.table("daily_stats").insert({"user_ID": u_id, "sleep_hours": sl, "water_liters": wt}).execute()
        st.rerun()

# --- TAB 3: DƏRS (BAR CHART İLƏ) ---
with tab3:
    col_a, col_b = st.columns([1, 2])
    with col_a:
        sub = st.selectbox("📚 Subject:", ["Math", "English", "Physics", "History"])
        dur = st.number_input("⏱️ Min:", 10, 300, 45)
        if st.button("📖 Save Study"):
            supabase.table("study_sessions").insert({"user_ID": u_id, "subject": sub, "duration_time": dur}).execute()
            st.rerun()
    
    with col_b:
        study_res = supabase.table("study_sessions").select("subject, duration_time").eq("user_ID", u_id).execute()
        if study_res.data:
            sdf = pd.DataFrame(study_res.data)
            st.bar_chart(sdf.groupby('subject').sum())

# --- TAB 4, 5, 6 (PRO VERSİYA) ---
with tab4: # Cədvəl
    st.subheader(t['schedule'])
    sh = st.radio("Shift:", [t['shift_m'], t['shift_a']])
    if st.button(t['calc_btn']):
        st.success("Təqviminiz hesablandı! Gündəlik 3 saatlıq fokus bloku təyin edildi.")

with tab5: # Musiqi
    st.subheader(t['music_title'])
    st.session_state.current_video = st.text_input("🔗 YouTube URL:", st.session_state.current_video)
    st.video(st.session_state.current_video)

with tab6: # Motivasiya
    st.markdown("### 🔥 High Performance Tips")
    st.write("1. **Deep Work:** İlk 90 dəqiqə telefona baxma.")
    st.write("2. **Hydration:** Beyin 80% sudan ibarətdir, su içməyi unutma!")

st.divider()
st.caption("EduBalance v3.0 | Analytics & High Performance 🚀")
