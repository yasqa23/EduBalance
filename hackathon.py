import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
# Qeyd: URL-dəki artıq boşluğu sildim ki, xəta verməsin
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance", layout="centered")

# 2. DİL SEÇİMİ
lang = st.sidebar.selectbox("🌐 Dil / Language", ["Azerbaycan", "English"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "profile": "Profil Məlumatları",
        "daily": "Günlük Statistika",
        "study": "Dərs Sessiyası",
        "save": "Yadda saxla",
        "success": "Məlumatlar uğurla qeyd olundu!",
        "mood_label": "Təxmin edilən Əhval:",
        "sleep_info": "Yuxu saatı:"
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "profile": "Profile Info",
        "daily": "Daily Stats",
        "study": "Study Session",
        "save": "Save Data",
        "success": "Data saved successfully!",
        "mood_label": "Estimated Mood:",
        "sleep_info": "Sleep hours:"
    }
}
t = texts[lang]

st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI
user_name_input = st.text_input("👤 Username:", "ali123")

tab1, tab2, tab3 = st.tabs([t['profile'], t['daily'], t['study']])

# --- TAB 1: PROFİL ---
with tab1:
    target = st.text_input("🎯 Hədəf İmtahan:", "Blok İmtahanı")
    if st.button(f"{t['save']} (Profile)"):
        prof_data = {"username": user_name_input, "Language": lang, "target_exam": target}
        supabase.table("students_profiles").insert(prof_data).execute()
        st.balloons()
        st.success(t['success'])

# --- TAB 2: GÜNLÜK STATS (AVTOMATİK ƏHVAL) ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider(t['sleep_info'], 0, 12, 8)
        water = st.number_input("💧 Su (Litr):", 0.0, 5.0, 1.5)
    
    with col2:
        # AVTOMATİK ƏHVAL MƏNTİQİ
        if sleep >= 8:
            auto_mood = "Əla"
            st.success("Enerjin yerindədir! ⚡")
        elif 6 <= sleep < 8:
            auto_mood = "Normal"
            st.info("Yaxşıdır, amma bir az daha dincələ bilərsən. 😊")
        else:
            auto_mood = "Yorğun"
            st.warning("Yuxun azdır, bu gün ağır dərsləri təxirə sal. ⚠️")
        
        # Əhvalı istifadəçi seçmir, proqram göstərir
        st.text_input(t['mood_label'], auto_mood, disabled=True)

    if st.button(f"{t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep, "mood": auto_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])
            
            if water < 2: st.warning("💧 Su qəbulun azdır, diqqətli ol!")
            if auto_mood == "Yorğun": 
                st.info("🎵 Rahatlamaq üçün bu pleylisti dinlə:")
                st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

# --- TAB 3: DƏRS SESSİYASI (AĞILLI MƏSLƏHƏT) ---
with tab3:
    subject = st.text_input("📚 Fənn adı:", "Riyaziyyat")
    duration = st.number_input("⏱️ Müddət (Dəqiqə):", 10, 300, 45)
    
    # Ağıllı məsləhət (Özəllik 6)
    if duration > 90:
        st.error("🚨 Diqqət: Birbaşa 90 dəqiqədən çox dərs oxumaq səmərəni azaldır. Pomodoro texnikasını yoxla!")
    elif duration >= 45:
        st.info("✅ İdeal dərs müddətidir. 5-10 dəqiqə fasilə verməyi unutma.")

    if st.button(f"{t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"Bravo! {subject} dərsi qeyd edildi!")

st.divider()
st.caption("EduBalance v1.0 | Hackathon Project 🚀")
