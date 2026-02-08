import streamlit as st
from supabase import create_client
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cXFwYnZuZnBneWVmenhoY2pyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0NjkyNjMsImV4cCI6MjA4NjA0NTI2M30.o9m2wuK-FrFRLZ0FLfivz5X8Ryen9OluGvc5F3f6oZY"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="EduBalance", layout="centered")

# 2. DİL SEÇİMİ
lang = st.sidebar.selectbox("🌐 Dil / Language / Langue", ["Azerbaycan", "English", "Français"])

texts = {
    "Azerbaycan": {
        "welcome": "EduBalance-a Xoş Gəldiniz",
        "profile": "Profil Məlumatları",
        "daily": "Günlük Statistika",
        "study": "Dərs Sessiyası",
        "save": "Yadda saxla",
        "success": "Məlumatlar uğurla qeyd olundu!",
        "mood_label": "Təxmin edilən Əhval:",
        "sleep_info": "Yuxu hesabı:",
        "sleep_start": "Nə vaxt yatdınız?",
        "sleep_end": "Nə vaxt oyandınız?"
    },
    "English": {
        "welcome": "Welcome to EduBalance",
        "profile": "Profile Info",
        "daily": "Daily Stats",
        "study": "Study Session",
        "save": "Save Data",
        "success": "Data saved successfully!",
        "mood_label": "Estimated Mood:",
        "sleep_info": "Sleep Calculation:",
        "sleep_start": "When did you sleep?",
        "sleep_end": "When did you wake up?"
    },
    "Français": {
        "welcome": "Bienvenue sur EduBalance",
        "profile": "Infos Profil",
        "daily": "Stats Quotidiennes",
        "study": "Session d'Étude",
        "save": "Enregistrer",
        "success": "Données enregistrées avec succès !",
        "mood_label": "Humeur Estimée :",
        "sleep_info": "Calcul du sommeil :",
        "sleep_start": "Quand avez-vous dormi ?",
        "sleep_end": "Quand vous êtes-vous réveillé ?"
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

# --- TAB 2: GÜNLÜK STATS (AĞILLI YUXU HESABLAYICI) ---
with tab2:
    st.subheader(f"🌙 {t['sleep_info']}")
    col1, col2 = st.columns(2)
    
    with col1:
        # Saat daxil etmə hissəsi
        sleep_time = st.time_input(t['sleep_start'], datetime.time(23, 0))
        wake_time = st.time_input(t['sleep_end'], datetime.time(7, 0))
        
        # Yuxu müddətini hesablamaq
        sleep_dt = datetime.datetime.combine(datetime.date.today(), sleep_time)
        wake_dt = datetime.datetime.combine(datetime.date.today(), wake_time)
        if wake_dt <= sleep_dt:
            wake_dt += datetime.timedelta(days=1)
        
        sleep_duration = (wake_dt - sleep_dt).seconds / 3600
        st.info(f"⏱️ Toplam: {sleep_duration:.1f} saat")
        
        water = st.number_input("💧 Su (Litr):", 0.0, 5.0, 1.5)
    
    with col2:
        # YUXU VƏ ƏHVAL MƏNTİQİ (Qızıl Orta)
        if 7 <= sleep_duration <= 9:
            auto_mood = "Əla"
            st.success("İdeal yuxu! Enerjin pik nöqtədədir. ⚡")
        elif sleep_duration > 9:
            auto_mood = "Halsız"
            st.warning("Həddindən çox yatmısan, bu süstlük yarada bilər. 😴")
        elif 5 <= sleep_duration < 7:
            auto_mood = "Normal"
            st.info("Fokuslanmaq üçün kifayətdir. 😊")
        else:
            auto_mood = "Yorğun"
            st.error("Yuxun çox azdır! Özünü yorma. ⚠️")
        
        st.text_input(t['mood_label'], auto_mood, disabled=True)

    if st.button(f"{t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep_duration, "mood": auto_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])
            
            if water < 2: st.warning("💧 Su içməyi unutma!")
            if auto_mood in ["Yorğun", "Halsız"]: 
                st.info("🎵 Rahatlamaq üçün pleylist:")
                st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

# --- TAB 3: DƏRS SESSİYASI ---
with tab3:
    subject = st.text_input("📚 Fənn adı:", "Riyaziyyat")
    duration = st.number_input("⏱️ Müddət (Dəqiqə):", 10, 300, 45)
    
    if duration > 90:
        st.error("🚨 Pomodoro texnikasını yoxla (90 dəqiqə + fasilə)!")
    elif duration >= 45:
        st.info("✅ İdeal dərs müddətidir.")

    if st.button(f"{t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject} qeyd edildi!")

st.divider()
st.caption("EduBalance v1.0 | Hackathon Project 🚀")
