import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import ssl
try:
    import google.generativeai as genai
except Exception:
    genai = None

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
# Custom CSS for Gen Z Style
# ---------------------------------------
st.markdown("""
<style>
    /* ... (style sama persis dengan yang kamu kirim) ... */
</style>
""", unsafe_allow_html=True)


st.title("🔥 Kalkulator Kalori ")
st.caption("Hitung kalori & gizi harianmu, no ribet! ✨")

# ---------------------------------------
# Input Data Pengguna
# ---------------------------------------
with st.container():
    st.header("👤 Data Diri")
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
with st.container():
    st.header("🍽️ Makanan Hari Ini")
    makanan = st.multiselect("Pilih makanan yang kamu makan:", list(foods.keys()))
    porsi = {}

    for m in makanan:
        porsi[m] = st.number_input(f"{m} (gram)", min_value=0.0, max_value=1000.0, step=10.0, key=f"porsi_{m}")

# ---------------------------------------
# Hitung Total Nutrisi
# ---------------------------------------
if makanan:
    total = {"kalori": 0, "protein": 0, "karbo": 0, "lemak": 0}
    for m, g in porsi.items():
        for n in total:
            total[n] += foods[m][n] * (g / 100)

    st.divider()
    
    with st.container():
        st.subheader("📊 Hasil Asupanmu")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Kalori", f"{total['kalori']:.1f} kkal")
            st.metric("Protein", f"{total['protein']:.1f} g")
        with col2:
            st.metric("Karbohidrat", f"{total['karbo']:.1f} g")
            st.metric("Lemak", f"{total['lemak']:.1f} g")

        # Progress bar kalori
        st.write("**Progress Kalori Harian:**")
        st.progress(min(total["kalori"] / tdee, 1.0))

        # Pie chart makronutrien
        st.write("**Komposisi Makro:**")
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.patch.set_alpha(0) # Transparan background
        fig.patch.set_alpha(0)
        
        pie_colors = ['#ff9999','#66b3ff','#99ff99']
        ax.pie(
            [total["karbo"], total["protein"], total["lemak"]],
            labels=["Karbo", "Protein", "Lemak"],
            autopct="%1.1f%%",
            colors=pie_colors,
            textprops={"fontsize": 8, "color": "white"},
        )
        st.pyplot(fig)

    # ---------------------------------------
    # Rekomendasi Otomatis
    # ---------------------------------------
    st.divider()
    with st.container():
        st.subheader("💡 Rekomendasi Cepet")

        # Basic calorie status
        if total["kalori"] < 0.9 * tdee:
            st.info("Kalorimu masih kurang nih — tambah porsi karbo atau camilan sehat (pisang, roti, jagung). 🍌")
        elif total["kalori"] > 1.1 * tdee:
            st.warning("Kalori hari ini agak over. Kurangi gorengan atau porsi nasi/karbo, dan tambah sayur. 😉")
        else:
            st.success("Kalori sudah pas untuk hari ini — teruskan!")

        # Macro breakdown and suggestions
        prot = total.get("protein", 0)
        kar = total.get("karbo", 0)
        fat = total.get("lemak", 0)
        cal = total.get("kalori", 0)

        # calories from macros
        calories_from_prot = prot * 4
        calories_from_kar = kar * 4
        calories_from_fat = fat * 9
        total_macro_cals = max(calories_from_prot + calories_from_kar + calories_from_fat, 1)

        prot_pct = calories_from_prot / total_macro_cals
        kar_pct = calories_from_kar / total_macro_cals
        fat_pct = calories_from_fat / total_macro_cals

        st.write(f"Protein: {prot:.1f} g — Karbo: {kar:.1f} g — Lemak: {fat:.1f} g")
        st.write(f"Komposisi energi (perkiraan): Protein {prot_pct:.0%}, Karbo {kar_pct:.0%}, Lemak {fat_pct:.0%}")

        # Practical tips based on macros
        tips = []
        # Protein target suggestion: simple heuristic 1.2-1.6 g/kg for active, else 0.8-1.0
        protein_target = 1.0 * berat
        if aktivitas == "Sangat Aktif (nge-gym)":
            protein_target = 1.4 * berat

        if prot < 0.8 * protein_target:
            tips.append("Proteinmu masih kurang — tambahin telur, tahu, tempe, atau ayam sebagai lauk.")
        elif prot > 2.5 * berat:
            tips.append("Protein sudah sangat tinggi untuk 1 hari — variasikan sumber dan kurangi porsi besar.")

        # Carb guidance
        if kar < 0.4 * (cal / 4):
            tips.append("Karbo rendah — kalau butuh energi tambah nasi, roti, atau pisang sebelum aktivitas.")
        if fat > 0.35 * (cal / 9):
            tips.append("Lemak terlihat tinggi — kurangi makanan goreng/berminyak.")

        # Quick swaps
        swaps = []
        if any(x in str(makanan).lower() for x in ["goreng", "fried", "bakar"]) and cal > 1.1 * tdee:
            swaps.append("Ganti beberapa gorengan dengan tahu/tempe kukus atau sayur rebus untuk memangkas lemak.")

        if cal < 0.9 * tdee:
            swaps.append("Tambahkan snack sehat: yogurt + buah, segenggam kacang, atau telur rebus.")

        # Display tips
        if tips:
            for t in tips:
                st.info(t)
        else:
            st.write("Tidak ada isu makro besar yang terdeteksi — good job!")

        if swaps:
            st.write("Saran penggantian cepat:")
            for s in swaps:
                st.write(f"- {s}")

        # Extra recommendation: sample mini-meal plan to reach TDEE if under
        if cal < 0.9 * tdee:
            st.write("\nContoh penambahan 1 porsi untuk menambah ~300 kkal:")
            st.write("- 1 porsi nasi + 1 telur goreng (atau 2 sdm kacang) — sekitar 250-350 kkal")

        # Additional protein reminder
        if prot < 0.8 * (berat * 0.8):
            st.info("Biar otot makin jadi, tambahin protein dari telur atau tahu, kuy!")

        # End recommendations

        # -------------------------
        # Optional AI Assistant (Gemini) - FIXED (unique keys)
        # -------------------------
        st.divider()
        st.subheader("🤖 AI Assistant (opsional - Gemini)")
        st.write("Tanya asisten tentang meal planning, substitusi bahan, atau minta ide resep singkat. (Menggunakan Google Generative API / Gemini)")

        # gunakan key unik untuk text_area & button agar tidak terjadi duplicate element id
        if "ai_prompt" not in st.session_state:
            st.session_state.ai_prompt = ""

        ai_prompt = st.text_area(
            "Tanya AI (contoh: 'Beri aku ide makan siang 400 kkal kaya protein')",
            value=st.session_state.get("ai_prompt", ""),
            height=80,
            key="ai_prompt_textarea",
        )

        # tombol dengan key unik
        ask_ai = st.button("Kirim ke AI", key="ask_ai_button")

        # -------------------------
        # Ambil API key dengan benar
        # -------------------------
        def _get_gemini_key():
            try:
                return st.secrets["GEMINI_API_KEY"]
            except Exception:
                return os.environ.get("GEMINI_API_KEY")

        # --- NEW/ROBUST: model detection + safe call for Gemini ---
        def _ensure_genai_configured():
            api_key = _get_gemini_key()
            if not api_key:
                return False, "API key Gemini tidak ditemukan. Tambahkan GEMINI_API_KEY ke st.secrets."
            if genai is None:
                return False, "Library 'google-generativeai' belum terpasang di environment. Tambahkan ke requirements.txt."
            try:
                genai.configure(api_key=api_key)
            except Exception as e:
                return False, f"Gagal konfigurasi Gemini SDK: {e}"
            return True, None

        def _detect_compatible_model():
            """
            List available models and pick the first model that supports generateContent.
            Cache the result in st.session_state['gemini_model_name'].
            """
            if "gemini_model_name" in st.session_state:
                return st.session_state["gemini_model_name"], None

            ok, err = _ensure_genai_configured()
            if not ok:
                return None, err

            try:
                models = genai.list_models()
                candidate = None
                for m in models:
                    # support multiple field names depending on genai version
                    mname = getattr(m, "name", None) or getattr(m, "model", None) or str(m)
                    methods = getattr(m, "supported_generation_methods", None) or getattr(m, "supported_methods", None) or []
                    # Accept generateContent or generate_text variants
                    if methods:
                        methods_lower = [str(x).lower() for x in methods]
                        if any("generatecontent" in s or "generate" in s for s in methods_lower):
                            candidate = mname
                            break
                if not candidate:
                    # fallback: try common known names if list_models doesn't reveal methods
                    # prefer flash model names (these may or may not exist depending on account)
                    fallback_names = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-1.5-pro-latest"]
                    for fn in fallback_names:
                        try:
                            # quick probe: try constructing a model object (no call yet)
                            _ = genai.GenerativeModel(fn)
                            candidate = fn
                            break
                        except Exception:
                            continue
                if not candidate:
                    return None, "Tidak ditemukan model Gemini yang mendukung generateContent pada akun ini."
                st.session_state["gemini_model_name"] = candidate
                return candidate, None
            except Exception as e:
                return None, f"Gagal mendapat daftar model Gemini: {e}"

        def call_gemini_chat(prompt_text: str):
            ok, err = _ensure_genai_configured()
            if not ok:
                return None, err

            model_name, err = _detect_compatible_model()
            if err:
                return None, err

            try:
                # buat model dengan generation_config (atur temperature dll di sini)
                model = genai.GenerativeModel(
                    model_name,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "max_output_tokens": 300,
                    },
                )

                context = f"Asupan sekarang: {total['kalori']:.1f} kkal, protein {total['protein']:.1f} g, karbo {total['karbo']:.1f} g, lemak {total['lemak']:.1f} g, TDEE {tdee:.0f} kkal."
                full_prompt = context + "\n\nUser question: " + prompt_text

                resp = model.generate_content(full_prompt)
                # respons bisa berbeda format tergantung versi SDK — coba beberapa opsi
                text = None
                if resp is None:
                    text = ""
                else:
                    text = getattr(resp, "text", None) or getattr(resp, "content", None)
                    if not text:
                        # some versions return candidates list
                        try:
                            cand = getattr(resp, "candidates", None)
                            if cand and len(cand) > 0:
                                # candidate may have .output_text or .content
                                text = getattr(cand[0], "output", None) or getattr(cand[0], "output_text", None) or getattr(cand[0], "content", None) or str(cand[0])
                        except Exception:
                            text = str(resp)
                return text or "", None
            except Exception as e:
                return None, f"Gagal memanggil Gemini: {e}"

        # wrapper yang sesuai dengan API pengguna: call_gemini(prompt) -> raises on error
        def call_gemini(prompt: str):
            resp, err = call_gemini_chat(prompt)
            if err:
                raise RuntimeError(err)
            return resp

        # jalankan panggilan AI hanya bila tombol ditekan
        if ask_ai and ai_prompt.strip():
            # simpan prompt ke session_state agar tidak hilang pada rerun
            st.session_state.ai_prompt = ai_prompt
            with st.spinner("🤖 Gemini lagi mikir..."):
                try:
                    resp = call_gemini(ai_prompt.strip())
                    st.success("**AI (Gemini) Menjawab:**")
                    st.info(resp)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini: {e}")
