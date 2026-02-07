import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co "
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY "
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance", layout="centered")

# 2. DİL SEÇİMİ (Özəllik 1)
lang = st.sidebar.selectbox("🌐 Dil / Language", ["Azerbaycan", "English"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "profile": "Profil Məlumatları",
        "daily": "Günlük Statistika (Yuxu və Su)",
        "study": "Dərs Sessiyası",
        "save": "Yadda saxla",
        "success": "Məlumatlar bazaya yazıldı!"
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "profile": "Profile Info",
        "daily": "Daily Stats (Sleep & Water)",
        "study": "Study Session",
        "save": "Save Data",
        "success": "Data saved successfully!"
    }
}
t = texts[lang]

st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI (Cədvəlləri bağlamaq üçün açar)
user_name_input = st.text_input("👤 Username (Qeydiyyatdakı adınız):", "ali123")

tab1, tab2, tab3 = st.tabs([t['profile'], t['daily'], t['study']])

# --- TAB 1: PROFİL (students_profiles) ---
with tab1:
    target = st.text_input("🎯 Hədəf İmtahan (Target Exam):", "Blok İmtahanı")
    if st.button(f"{t['save']} (Profile)"):
        prof_data = {"username": user_name_input, "Language": lang, "target_exam": target}
        supabase.table("students_profiles").insert(prof_data).execute()
        st.balloons()

# --- TAB 2: GÜNLÜK STATS (daily_stats) ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("😴 Yuxu saatı:", 0, 12, 8)
        water = st.number_input("💧 Su (Litr):", 0.0, 5.0, 1.5)
    with col2:
        mood = st.selectbox("😊 Əhval:", ["Əla", "Normal", "Yorğun", "Stressli"])
    
    if st.button(f"{t['save']} (Daily)"):
        # Öncə user_ID tapılır
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep, "mood": mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])
            
            # MƏSLƏHƏT (Özəllik: Su və Yuxu Analizi)
            if water < 2: st.warning("⚠️ Daha çox su içməlisən!")
            if mood == "Stressli": 
                st.info("🎵 Rahatlamaq üçün bu pleylisti dinlə:")
                st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

# --- TAB 3: DƏRS SESSİYASI (study_sessions) ---
with tab3:
    subject = st.text_input("📚 Fənn adı:", "Riyaziyyat")
    duration = st.number_input("⏱️ Müddət (Dəqiqə):", 10, 300, 45)
    
    if st.button(f"{t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject} dərsi qeyd edildi!")

st.divider()
st.caption("EduBalance v1.0 | Hackathon Project")
