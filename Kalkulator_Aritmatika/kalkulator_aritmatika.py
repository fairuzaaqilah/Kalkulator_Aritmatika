import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Laboratorium Deret Aritmatika",
    page_icon="📐",
    layout="wide"
)

# --- 2. CSS Kustom (Perbaikan Error di sini) ---
# Pastikan indentasi di dalam string (""") rata kiri atau konsisten
st.markdown("""
<style>
    .big-font {
        font-size:20px !important;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Judul dan Tujuan ---
st.title("📐 Laboratorium Penemuan: Deret Aritmatika")
st.markdown("""
Aplikasi ini dirancang untuk membantu kamu **menemukan sendiri** rumus suku ke-n ($U_n$) dari barisan aritmatika melalui visualisasi dan simulasi.
""")

st.divider()

# --- 4. Input Parameter (Sidebar) ---
with st.sidebar:
    st.header("🎛️ Panel Kontrol")
    st.info("Ubah nilai di bawah ini untuk melihat perubahannya.")
    
    a = st.number_input("Suku Pertama (a)", value=2, step=1, help="Nilai awal dari barisan")
    b = st.number_input("Beda / Selisih (b)", value=3, step=1, help="Penambahan nilai setiap langkah")
    n_terms = st.slider("Jumlah Suku (n)", min_value=3, max_value=20, value=10)

    st.markdown("---")
    st.caption("Dibuat dengan Python & Streamlit")

# --- 5. Logika Perhitungan ---
data = []

for n in range(1, n_terms + 1):
    nilai_suku = a + (n - 1) * b
    
    # Membangun logika penemuan rumus
    # Contoh: U3 = a + b + b = a + 2b
    koefisien_b = n - 1
    
    if koefisien_b == 0:
        penjelasan = f"$U_{n} = {a}$"
        pola = "a"
    elif koefisien_b == 1:
        penjelasan = f"$U_{n} = {a} + {b} = {nilai_suku}$"
        pola = "a + b"
    else:
        penjelasan = f"$U_{n} = {a} + ({koefisien_b} \\times {b}) = {nilai_suku}$"
        pola = f"a + {koefisien_b}b"

    data.append({
        "Suku Ke- (n)": n,
        "Nilai (Un)": nilai_suku,
        "Pola": pola,
        "Penjelasan": penjelasan
    })

df = pd.DataFrame(data)

# --- 6. Visualisasi & Animasi ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 Analisis Pola")
    st.write("Perhatikan bagaimana nilai bertambah:")
    
    # Menampilkan tabel interaktif
    st.dataframe(
        df[["Suku Ke- (n)", "Penjelasan"]],
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("""
    <div class='highlight'>
    <b>Pertanyaan Refleksi:</b><br>
    Lihatlah <b>koefisien</b> (angka pengali) di depan nilai beda ($b$).
    Jika suku ke-<b>n</b>, berapa kali kita menambahkan $b$?
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("📈 Visualisasi Pergerakan")
    
    tab_chart, tab_animasi = st.tabs(["Grafik Statis", "🎬 Animasi Pertumbuhan"])
    
    # Grafik Dasar
    fig = px.bar(
        df, x="Suku Ke- (n)", y="Nilai (Un)", 
        text="Nilai (Un)", 
        color="Nilai (Un)",
        color_continuous_scale="Viridis",
        title=f"Pertumbuhan Barisan Aritmatika (a={a}, b={b})"
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis=dict(tickmode='linear'))
    
    with tab_chart:
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Grafik batang menunjukkan besarnya nilai setiap suku.")

    # Animasi
    with tab_animasi:
        st.write("Tekan tombol di bawah untuk melihat animasi penambahan suku:")
        start_btn = st.button("▶️ Mulai Animasi")
        
        chart_placeholder = st.empty()
        
        if start_btn:
            # Loop untuk animasi
            for i in range(1, len(df) + 1):
                subset_df = df.iloc[:i]
                
                # Membuat grafik dinamis
                anim_fig = go.Figure()
                
                # Menambahkan Bar
                anim_fig.add_trace(go.Bar(
                    x=subset_df["Suku Ke- (n)"],
                    y=subset_df["Nilai (Un)"],
                    marker=dict(color=subset_df["Nilai (Un)"], colorscale='Viridis'),
                    text=subset_df["Nilai (Un)"],
                    textposition='outside',
                    name='Nilai'
                ))
                
                # Menambahkan Garis (Trend)
                anim_fig.add_trace(go.Scatter(
                    x=subset_df["Suku Ke- (n)"],
                    y=subset_df["Nilai (Un)"],
                    mode='lines+markers',
                    line=dict(color='red', width=2, dash='dash'),
                    name='Trend Linear'
                ))

                # Update Layout
                max_y = df["Nilai (Un)"].max() * 1.1
                anim_fig.update_layout(
                    title=f"Menambahkan Suku ke-{i}...",
                    xaxis=dict(range=[0, n_terms + 1], title="Suku Ke- (n)"),
                    yaxis=dict(range=[0, max_y], title="Nilai (Un)"),
                    showlegend=False,
                    height=400
                )
                
                chart_placeholder.plotly_chart(anim_fig, use_container_width=True)
                time.sleep(0.5) # Kecepatan animasi
            
            st.success("Animasi Selesai! Perhatikan garis lurus yang terbentuk.")

# --- 7. Kesimpulan Rumus ---
st.divider()
st.header("💡 Kesimpulan: Menemukan Rumus")

col_rumus_1, col_rumus_2 = st.columns(2)

with col_rumus_1:
    st.markdown("Mari kita bedah polanya:")
    st.latex(r"U_1 = a")
    st.latex(r"U_2 = a + 1 \cdot b")
    st.latex(r"U_3 = a + 2 \cdot b")
    st.latex(r"U_4 = a + 3 \cdot b")
    st.markdown("...")
    st.markdown("**Maka untuk suku ke-n:**")
    st.latex(r"U_n = a + (\dots) \cdot b")

with col_rumus_2:
    st.info("Jika kamu perhatikan, pengali b selalu berkurang 1 dari nilai n.")
    st.markdown("### Rumus Umum Barisan Aritmatika:")
    
    # Menampilkan rumus akhir
    st.latex(r"\huge \boxed{U_n = a + (n-1)b}")
    
    st.write(f"""
    Dalam contoh simulasi di atas:
    * **a (Suku Awal)** = {a}
    * **b (Beda)** = {b}
    * **n (Suku dicari)** = {n_terms}
    
    Coba hitung manual: ${a} + ({n_terms}-1){b} = {a + (n_terms-1)*b}$
    """)
