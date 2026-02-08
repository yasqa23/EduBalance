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
        "sleep_end": "Nə vaxt oyandınız?",
        "subject_label": "📚 Fənni seçin:",
        "target_label": "🎯 Hədəf İmtahan:"
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
        "sleep_end": "When did you wake up?",
        "subject_label": "📚 Select Subject:",
        "target_label": "🎯 Target Exam:"
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
        "sleep_end": "Quand vous êtes-vous réveillé ?",
        "subject_label": "📚 Sélectionner la matière:",
        "target_label": "🎯 Examen Cible:"
    }
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# 3. İSTİFADƏÇİ ADI
user_name_input = st.text_input("👤 Username:", "ali123")

tab1, tab2, tab3 = st.tabs([t['profile'], t['daily'], t['study']])

# --- TAB 1: PROFİL (COXSEÇİMLİ İMTAHAN SEÇİMİ) ---
with tab1:
    exam_options = [
        "Buraxılış İmtahanı", 
        "Blok İmtahanı", 
        "Magistratura", 
        "YÖS / SAT", 
        "MİQ", 
        "Sertifikasiya", 
        "Digər"
    ]
    target = st.selectbox(t['target_label'], exam_options)
    
    if st.button(f"{t['save']} (Profile)"):
        prof_data = {"username": user_name_input, "Language": lang, "target_exam": target}
        supabase.table("students_profiles").insert(prof_data).execute()
        st.balloons()
        st.success(t['success'])

# --- TAB 2: GÜNLÜK STATS (AĞILLI ANALİZ) ---
with tab2:
    st.subheader(f"🌙 {t['sleep_info']}")
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_time = st.time_input(t['sleep_start'], datetime.time(23, 0))
        wake_time = st.time_input(t['sleep_end'], datetime.time(7, 0))
        
        sleep_dt = datetime.datetime.combine(datetime.date.today(), sleep_time)
        wake_dt = datetime.datetime.combine(datetime.date.today(), wake_time)
        if wake_dt <= sleep_dt:
            wake_dt += datetime.timedelta(days=1)
        
        sleep_duration = (wake_dt - sleep_dt).seconds / 3600
        st.info(f"⏱️ Toplam yuxu: {sleep_duration:.1f} saat")
        
        water = st.number_input("💧 Günlük içdiyin su (Litr):", 0.0, 5.0, 1.5, step=0.1)
    
    with col2:
        score = 0
        if 7 <= sleep_duration <= 9: score += 60
        elif sleep_duration > 9 or 5 <= sleep_duration < 7: score += 40
        else: score += 20
        
        if water >= 2.0: score += 40
        elif 1.0 <= water < 2.0: score += 20
        else: score += 0
        
        if score >= 90:
            auto_mood = "Əla"
            st.success("Möhtəşəm! Tam balanslısan. 🔥")
        elif score >= 60:
            auto_mood = "Normal"
            st.info("Vəziyyətin yaxşıdır. 😊")
        elif 40 <= score < 60:
            auto_mood = "Yorğun / Halsız"
            st.warning("Yuxu və ya su çatışmır! ⚠️")
        else:
            auto_mood = "Stressli / Baş ağrısı"
            st.error("Bədənin SOS verir! Su iç və dincəl. 🚨")
        
        st.text_input(t['mood_label'], auto_mood, disabled=True)

    if st.button(f"{t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep_duration, "mood": auto_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])
            
            if water < 2: st.error("💧 Su azlığı diqqəti 25% azaldır! Su iç!")
            if auto_mood in ["Yorğun", "Stressli", "Halsız"]: 
                st.info("🎵 Fokuslanmaq üçün pleylist:")
                st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

# --- TAB 3: DƏRS SESSİYASI (FƏNN SEÇİMİ) ---
with tab3:
    subjects_list = [
        "Azərbaycan dili", "Riyaziyyat", "İngilis dili", 
        "Fizika", "Kimya", "Biologiya", "Tarix", 
        "Coğrafiya", "İnformatika", "Digər"
    ]
    
    subject_choice = st.selectbox(t['subject_label'], subjects_list)
    duration = st.number_input("⏱️ Müddət (Dəqiqə):", 10, 300, 45)
    
    if duration > 90:
        st.error("🚨 Beyin yorulur! Fasilə ver.")
    elif duration >= 45:
        st.info("✅ İdeal fokus müddəti.")

    if st.button(f"{t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", user_name_input).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject_choice, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject_choice} qeyd edildi!")

st.divider()
st.caption("EduBalance v1.0 | Hackathon Project 🚀")
