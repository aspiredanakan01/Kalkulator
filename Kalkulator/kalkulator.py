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
st.set_page_config(page_title="Kalkulator Makanan Sehat", page_icon="🥗", layout="centered")

st.title("🥗 Kalkulator Makanan Sehat")
st.caption("Versi minimalis – hitung kalori & gizi harianmu dengan cepat")

# ---------------------------------------
# Input Data Pengguna
# ---------------------------------------
st.header("👤 Data Pribadi")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    usia = st.number_input("Usia (tahun)", 1, 100, 25)
    aktivitas = st.selectbox("Aktivitas", ["Rendah", "Sedang", "Tinggi"])
with col2:
    berat = st.number_input("Berat Badan (kg)", 1, 200, 60)
    tinggi = st.number_input("Tinggi Badan (cm)", 100, 220, 165)

# ---------------------------------------
# Hitung BMR & TDEE
# ---------------------------------------
if gender == "Laki-laki":
    bmr = 10 * berat + 6.25 * tinggi - 5 * usia + 5
else:
    bmr = 10 * berat + 6.25 * tinggi - 5 * usia - 161

faktor = {"Rendah": 1.2, "Sedang": 1.55, "Tinggi": 1.725}
tdee = bmr * faktor[aktivitas]

st.markdown(f"**Kebutuhan Kalori Harian (TDEE):** {tdee:.0f} kkal")

# ---------------------------------------
# Input Makanan
# ---------------------------------------
st.header("🍽️ Input Makanan")
makanan = st.multiselect("Pilih makanan yang dikonsumsi:", list(foods.keys()))
porsi = {}

for m in makanan:
    porsi[m] = st.number_input(f"{m} (gram)", min_value=0.0, max_value=1000.0, step=10.0)

# ---------------------------------------
# Hitung Total Nutrisi
# ---------------------------------------
if makanan:
    total = {"kalori": 0, "protein": 0, "karbo": 0, "lemak": 0}
    for m, g in porsi.items():
        for n in total:
            total[n] += foods[m][n] * (g / 100)

    st.divider()
    st.subheader("📊 Hasil Asupan Harian")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Kalori", f"{total['kalori']:.1f} kkal")
        st.metric("Protein", f"{total['protein']:.1f} g")
    with col2:
        st.metric("Karbohidrat", f"{total['karbo']:.1f} g")
        st.metric("Lemak", f"{total['lemak']:.1f} g")

    # Progress bar kalori
    st.write("**Capaian kalori harian:**")
    st.progress(min(total["kalori"] / tdee, 1.0))

    # Pie chart makronutrien
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(
        [total["karbo"], total["protein"], total["lemak"]],
        labels=["Karbo", "Protein", "Lemak"],
        autopct="%1.1f%%",
        textprops={"fontsize": 8},
    )
    st.pyplot(fig)

    # ---------------------------------------
    # Rekomendasi Otomatis
    # ---------------------------------------
    st.divider()
    st.subheader("💡 Rekomendasi")

    if total["kalori"] < 0.9 * tdee:
        st.info("Asupan kalori masih **kurang**, tambahkan makanan seperti nasi, tempe, atau pisang.")
    elif total["kalori"] > 1.1 * tdee:
        st.warning("Kalori **berlebih**, kurangi makanan tinggi lemak seperti ayam goreng.")
    else:
        st.success("Asupan kalori sudah **seimbang**, pertahankan pola makanmu! 🥦")

    if total["protein"] < 0.8 * (berat * 0.8):
        st.info("Protein agak rendah, bisa tambah sumber protein seperti telur atau tahu.")
else:
    st.write("💬 Pilih makanan dan masukkan porsinya untuk menghitung total gizi.")
