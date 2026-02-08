import streamlit as st
from supabase import create_client
import openai  # pip install openai
import datetime

# 1. SUPABASE BAĞLANTISI
URL = "https://tvqqpbvnfpgyefzxhcjr.supabase.co"
KEY = "YOUR_SUPABASE_KEY"
supabase = create_client(URL, KEY)

# 2. OPENAI API AÇARI
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="EduBalance AI", layout="centered")

# Sessiya yaddaşı
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# 3. DİL SEÇİMİ
lang = st.sidebar.selectbox("🌐 Dil / Language / Langue", ["Azerbaycan", "English", "Français"])

texts = {
    "Azerbaycan": {"welcome":"EduBalance-a Xoş Gəldiniz","user_label":"👤 İstifadəçi adı:","user_placeholder":"Adınızı daxil edin...","save":"Yadda saxla","success":"Məlumatlar uğurla qeyd olundu!","error_user":"Davam etmək üçün istifadəçi adını yazıb Enter basın!","mood_label":"Təxmin edilən Əhval:"},
    "English": {"welcome":"Welcome to EduBalance","user_label":"👤 Username:","user_placeholder":"Enter your name...","save":"Save Data","success":"Data saved successfully!","error_user":"Please enter username and press Enter!","mood_label":"Estimated Mood:"},
    "Français": {"welcome":"Bienvenue sur EduBalance","user_label":"👤 Nom d'utilisateur:","user_placeholder":"Entrez votre nom...","save":"Enregistrer","success":"Données enregistrées avec succès !","error_user":"Veuillez entrer votre nom et appuyer sur Entrée !","mood_label":"Humeur Estimée :"}
}

t = texts[lang]
st.title(f"🎓 {t['welcome']}")

# İstifadəçi adı
user_input = st.text_input(t['user_label'], value=st.session_state.user_name, placeholder=t['user_placeholder'])
if user_input:
    st.session_state.user_name = user_input
if not st.session_state.user_name:
    st.warning(t['error_user'])
    st.stop()

tab1, tab2, tab3 = st.tabs(["Profile","Daily","Study"])

# --- TAB 2: Günlük Stats + AI Feedback ---
with tab2:
    sleep_duration = st.slider("🌙 Sleep (Hours)", 0.0, 12.0, 8.0)
    water = st.number_input("💧 Water (Liters)", 0.0, 5.0, 1.5, step=0.1)
    
    # AI tərəfindən tövsiyə funksiyası
    def get_ai_advice(sleep, water):
        prompt = f"""
        You are a friendly AI wellness assistant. A student slept {sleep} hours and drank {water} liters of water today.
        Give a short motivational and health advice in {lang} language.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role":"system","content":"You give short, friendly wellness advice to students."},
                          {"role":"user","content":prompt}],
                temperature=0.7,
                max_tokens=60
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error: {e}"
    
    if st.button(f"💡 Get AI Advice"):
        advice = get_ai_advice(sleep_duration, water)
        st.info(advice)

    # Əhval statusu
    score = (60 if 7 <= sleep_duration <= 9 else 30) + (40 if water >= 2 else 15)
    if score >= 90:
        current_mood = "Great 🔥"
    elif score >= 60:
        current_mood = "Normal 😊"
    else:
        current_mood = "Tired 😴"
    st.metric(t['mood_label'], current_mood)

    # Data yadda saxla
    if st.button(f"💾 {t['save']} (Daily)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            u_id = res.data[0]['id']
            stats = {"user_ID": u_id, "sleep_hours": sleep_duration, "mood": current_mood, "water_liters": water}
            supabase.table("daily_stats").insert(stats).execute()
            st.success(t['success'])

# --- TAB 3: Study Session + AI Study Tips ---
with tab3:
    subject_choice = st.selectbox("📚 Subject:", ["Math","Physics","English","Biology"])
    duration = st.number_input("⏱️ Duration (min):", 10, 300, 45)
    
    def get_ai_study_tip(subject, duration):
        prompt = f"""
        You are a friendly AI study coach. A student is going to study {subject} for {duration} minutes.
        Give a short motivational and focus tip in {lang} language.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role":"system","content":"You give short study tips to students."},
                          {"role":"user","content":prompt}],
                temperature=0.7,
                max_tokens=60
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error: {e}"
    
    if st.button(f"💡 Get AI Study Tip"):
        tip = get_ai_study_tip(subject_choice, duration)
        st.info(tip)
    
    if st.button(f"📖 {t['save']} (Study)"):
        res = supabase.table("students_profiles").select("id").eq("username", st.session_state.user_name).execute()
        if res.data:
            u_id = res.data[0]['id']
            study = {"user_ID": u_id, "subject": subject_choice, "duration_time": duration}
            supabase.table("study_sessions").insert(study).execute()
            st.success(f"{subject_choice} - {t['success']}")
