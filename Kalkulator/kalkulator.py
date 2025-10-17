import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import urllib.request
import urllib.error
import ssl

# ---------------------------------------
# Data makanan sederhana (100 gram)
# ---------------------------------------
foods = {
    "Nasi Putih": {"kalori": 175, "protein": 3.2, "karbo": 40, "lemak": 0.3},
    "Ayam Goreng": {"kalori": 250, "protein": 20, "karbo": 0, "lemak": 18},
    "Tempe": {"kalori": 150, "protein": 14, "karbo": 8, "lemak": 8},
    "Sayur Bayam": {"kalori": 40, "protein": 3, "karbo": 7, "lemak": 0.5},
    "Pisang": {"kalori": 90, "protein": 1, "karbo": 23, "lemak": 0.3},
    "Telur Rebus": {"kalori": 155, "protein": 13, "karbo": 1, "lemak": 11},
    "Tahu": {"kalori": 80, "protein": 8, "karbo": 2, "lemak": 4},
    "Nasi Goreng": {"kalori": 250, "protein": 6, "karbo": 32, "lemak": 9},
    "Mie Goreng": {"kalori": 270, "protein": 7, "karbo": 40, "lemak": 8},
    "Sate Ayam": {"kalori": 230, "protein": 18, "karbo": 6, "lemak": 14},
    "Rendang": {"kalori": 350, "protein": 15, "karbo": 4, "lemak": 28},
    "Bakso": {"kalori": 200, "protein": 12, "karbo": 10, "lemak": 12},
    "Soto Ayam": {"kalori": 90, "protein": 7, "karbo": 6, "lemak": 4},
    "Ayam Bakar": {"kalori": 190, "protein": 24, "karbo": 0, "lemak": 9},
    "Ikan Goreng": {"kalori": 220, "protein": 20, "karbo": 0, "lemak": 14},
    "Ikan Bakar": {"kalori": 180, "protein": 22, "karbo": 0, "lemak": 8},
    "Udang Goreng": {"kalori": 190, "protein": 24, "karbo": 0, "lemak": 9},
    "Tempe Goreng": {"kalori": 210, "protein": 19, "karbo": 8, "lemak": 12},
    "Tahu Goreng": {"kalori": 140, "protein": 12, "karbo": 3, "lemak": 8},
    "Roti Tawar": {"kalori": 265, "protein": 9, "karbo": 49, "lemak": 3.2},
    "Kentang Goreng": {"kalori": 312, "protein": 3.4, "karbo": 41, "lemak": 15},
    "Jagung Rebus": {"kalori": 96, "protein": 3.4, "karbo": 21, "lemak": 1.5},
    "Apel": {"kalori": 52, "protein": 0.3, "karbo": 14, "lemak": 0.2},
    "Keju Cheddar": {"kalori": 403, "protein": 25, "karbo": 1.3, "lemak": 33},
    "Susu UHT (sapi)": {"kalori": 60, "protein": 3.4, "karbo": 5, "lemak": 3.3},
    "Yogurt Plain": {"kalori": 59, "protein": 10, "karbo": 3.6, "lemak": 0.4},
    "Kacang Tanah (goreng)": {"kalori": 567, "protein": 25.8, "karbo": 16.1, "lemak": 49.2},
}

# ---------------------------------------
# Tampilan Utama
# ---------------------------------------
st.set_page_config(page_title="Kalkulator Kalori ", page_icon="🔥", layout="centered")

# ---------------------------------------
# (CSS dan tampilan tetap sama)
# ---------------------------------------

st.title("🔥 Kalkulator Kalori ")
st.caption("Hitung kalori & gizi harianmu, no ribet! ✨")

# ---------------------------------------
# Input Data Pengguna
# ---------------------------------------
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    usia = st.slider("Usia (tahun)", 1, 100, 25)
    aktivitas = st.selectbox("Level Aktivitas", ["Santai (rebahan)", "Normal (kuliah/kerja)", "Sangat Aktif (nge-gym)"])
with col2:
    berat = st.slider("Berat Badan (kg)", 1, 200, 60)
    tinggi = st.slider("Tinggi Badan (cm)", 100, 220, 165)

# ---------------------------------------
# Hitung BMR & TDEE
# ---------------------------------------
if gender == "Laki-laki":
    bmr = 10 * berat + 6.25 * tinggi - 5 * usia + 5
else:
    bmr = 10 * berat + 6.25 * tinggi - 5 * usia - 161

faktor = {"Santai (rebahan)": 1.2, "Normal (kuliah/kerja)": 1.55, "Sangat Aktif (nge-gym)": 1.725}
tdee = bmr * faktor[aktivitas]

st.success(f"**Kebutuhan Kalori Harianmu (TDEE):** {tdee:.0f} kkal")

# ---------------------------------------
# Input Makanan
# ---------------------------------------
makanan = st.multiselect("🍽️ Pilih makanan yang kamu makan:", list(foods.keys()))
porsi = {m: st.number_input(f"{m} (gram)", min_value=0.0, max_value=1000.0, step=10.0, key=f"porsi_{m}") for m in makanan}

# ---------------------------------------
# Hitung Total Nutrisi
# ---------------------------------------
if makanan:
    total = {"kalori": 0, "protein": 0, "karbo": 0, "lemak": 0}
    for m, g in porsi.items():
        for n in total:
            total[n] += foods[m][n] * (g / 100)

    st.metric("Total Kalori", f"{total['kalori']:.1f} kkal")

    # -------------------------
    # 🤖 AI Assistant (fix versi)
    # -------------------------
    st.divider()
    st.subheader("🤖 AI Assistant (opsional)")
    ai_prompt = st.text_area("Tanya AI (contoh: 'Beri aku ide makan siang 400 kkal kaya protein')", height=80)
    ask_ai = st.button("Kirim ke AI")

    def _get_openai_key():
        """Ambil API key dari Streamlit Secrets atau environment variable"""
        key = None
        try:
            key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            key = os.environ.get("OPENAI_API_KEY")
        return key

    def call_openai_chat(prompt_text: str):
        api_key = _get_openai_key()
        if not api_key:
            return None, "🔑 API key tidak ditemukan. Tambahkan ke st.secrets sebagai OPENAI_API_KEY."

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

        context = f"Current totals: kalori={total['kalori']:.1f} kcal, protein={total['protein']:.1f} g, karbo={total['karbo']:.1f} g, lemak={total['lemak']:.1f} g, TDEE={tdee:.0f} kcal."
        full_prompt = context + "\n\nUser question: " + prompt_text

        body = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful nutrition assistant that gives concise, practical food advice."},
                {"role": "user", "content": full_prompt},
            ],
            "max_tokens": 300,
            "temperature": 0.7,
        }

        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=15) as resp:
                j = json.loads(resp.read().decode("utf-8"))
                return j["choices"][0]["message"]["content"], None
        except Exception as e:
            return None, str(e)

    if ask_ai and ai_prompt.strip():
        with st.spinner("Menghubungi AI..."):
            resp, err = call_openai_chat(ai_prompt.strip())
        if err:
            st.error(f"Gagal: {err}")
        else:
            st.info(resp)
else:
    st.write("💬 Pilih makanan & masukin porsinya buat liat hasilnya, bestie.")
