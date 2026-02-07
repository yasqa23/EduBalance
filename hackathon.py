import streamlit as st
from supabase import create_client

# 1. BAĞLANTI AYARLARI
URL = "SƏNİN_GOTURDUYUN_URL"
KEY = "SƏNİN_GOTURDUYUN_ANON_KEY"
supabase = create_client(URL, KEY)

# SƏHİFƏ AYARLARI (Dizayn üçün)
st.set_page_config(page_title="EduBalance", layout="wide")

# 2. DİL SEÇİMİ (Özəllik 7)
lang = st.sidebar.selectbox("Dil / Language", ["Azerbaycan", "English", "Türkçe"])

texts = {
    "Azerbaycan": {"title": "EduBalance-a Xoş Gəldiniz", "sleep": "Yuxu saatı", "send": "Yadda saxla"},
    "English": {"title": "Welcome to EduBalance", "sleep": "Sleep hours", "send": "Save Data"},
    "Türkçe": {"title": "EduBalance'a Hoş Geldiniz", "sleep": "Uyku saati", "send": "Kaydet"}
}

t = texts[lang]

# 3. İNTERFEYS (GİRİŞ HİSSƏSİ)
st.title(f"🎓 {t['title']}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Günlük Göstəricilər")
    u_name = st.text_input("Adın:")
    u_sleep = st.slider(t['sleep'], 0, 12, 8)
    u_mood = st.selectbox("Əhvalın:", ["Əla", "Yorğun", "Stressli", "Normal"])

# 4. BAZAYA GÖNDƏRMƏ (Hər şeyi birləşdirən hissə)
if st.button(t['send']):
    data = {
        "user_name": u_name,
        "sleep_hours": u_sleep,
        "mood": u_mood,
        "language": lang
    }
    
    # "profiles" cədvəlinə məlumatı yazırıq
    try:
        response = supabase.table("profiles").insert(data).execute()
        st.success("Məlumatlar uğurla qeyd olundu!")
        
        # 5. AVTOMATİK MƏSLƏHƏT (Özəllik 1 və 2)
        if u_sleep < 6:
            st.warning("⚠️ Yuxun azdır! Bu gün ağır dərsləri təxirə sal və bol su iç.")
        
        # 6. PLAYLIST TƏKLİFİ (Özəllik 5)
        if u_mood == "Stressli":
            st.info("🎵 Gərgin görünürsən. Bu Lofi pleylistini dinləyərək dərslərinə fokuslana bilərsən.")
            st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk") # Nümunə Lofi linki
            
    except Exception as e:
        st.error(f"Xəta baş verdi: {e}")

# 7. PROQRAMIN AŞAĞI HİSSƏSİ (Statistika)
st.divider()
st.write("EduBalance v1.0 - Hackathon Edition")