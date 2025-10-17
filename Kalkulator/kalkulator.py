import streamlit as st
import matplotlib.pyplot as plt

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
}

# ---------------------------------------
# Tampilan Utama
# ---------------------------------------
st.set_page_config(page_title="Kalkulator Kalori Gen Z", page_icon="🔥", layout="centered")

# ---------------------------------------
# Custom CSS for Gen Z Style
# ---------------------------------------
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #1a1a1a;
        color: #e6e6e6;
    }
    
    /* Titles and headers */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }

    /* Input widgets */
    .st-emotion-cache-1r4qj8v, .st-emotion-cache-1y4p8pa {
        border-radius: 12px;
        border: 1px solid #4f4f4f;
        background-color: #2b2b2b;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 12px;
        border: 1px solid #4f4f4f;
        background-color: #3d3d3d;
        color: #ffffff;
    }

    /* Metrics */
    .st-emotion-cache-1vzeuhh {
        border-radius: 12px;
        padding: 1rem;
        background-color: #2b2b2b;
    }
    
    /* Progress bar */
    .st-emotion-cache-fplgep {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


st.title("🔥 Kalkulator Kalori Gen Z")
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

        if total["kalori"] < 0.9 * tdee:
            st.info("Kalorimu masih kurang nih, gas nambah nasi atau pisang! 🍌")
        elif total["kalori"] > 1.1 * tdee:
            st.warning("Waduh, kalori agak over. Coba kurangin yang goreng-goreng ya. 😉")
        else:
            st.success("Mantap! Kalorimu udah pas. Pertahankan! 🥦")

        if total["protein"] < 0.8 * (berat * 0.8):
            st.info("Biar otot makin jadi, tambahin protein dari telur atau tahu, kuy!")
else:
    st.write("💬 Pilih makanan & masukin porsinya buat liat hasilnya, bestie.")
