import streamlit as st
import time
from Backend import tinh_TDEE, tinh_protein, tinh_fat, tinh_carb, learn, create

def load():
    return learn("duantinhoc.csv")

knn, df, scaler = load()

st.set_page_config(
    page_title="Dự Án Tin Học Hk2",
    layout="wide",
)
#1.sidebar
with st.sidebar:
    st.header("Thông số của bạn")
    chieu_cao = st.number_input("Chiều cao(cm):",min_value=0, value=200)
    can_nang = st.number_input("Cân nặng(kg):",min_value= 1, value=150)
    tuoi = st.number_input("Tuổi:",min_value=0, value=14)
    gioi_tinh = st.selectbox("Giới tính:", ["Nam", "Nữ"])
    van_dong = st.selectbox("Mức độ vận động:", ["Rất hay vận động", "Hay vận động", "Ít vận động", "Không bao giờ vận động"])
    so_bua_an = st.slider("Số bữa ăn trong ngày", 1, 5, 3)
    muc_tieu =st.selectbox("Mục tiêu:", ["Tăng cân", "Giảm cân", "Giữ dáng"])
    loai_tru = st.multiselect("Món muốn loại trừ:", ["Hành", "Hải sản", "Sữa"])

calo_muc_tieu = tinh_TDEE(can_nang, chieu_cao, tuoi, gioi_tinh, van_dong, muc_tieu)
protein_can_thiet = tinh_protein(can_nang, muc_tieu, van_dong)
fat_can_thiet = tinh_fat(calo_muc_tieu)
carb_can_thiet = tinh_carb(calo_muc_tieu, protein_can_thiet, fat_can_thiet)
#2. main
st.title("🥗 AI Nutritionist - Trợ lý Dinh dưỡng Cá nhân của bạn!")
st.subheader("Chỉ số của cơ thể")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Mục tiêu Calo/ngày", f" {calo_muc_tieu} kcal") # Thay "---" bằng biến logic
with col2:
    st.metric("Đạm khuyên dùng", f" {protein_can_thiet} g")      # Thay "---" bằng biến logic
with col3:
    st.metric("Tinh bột khuyên dùng", f" {carb_can_thiet} g")
with col4:
    st.metric("Chất béo khuyên dùng", f" {fat_can_thiet} g")
st.divider()
# 3. button
if st.button(" TẠO THỰC ĐƠN!", use_container_width=True, type="primary"):
    with st.status("Đang tính toán...") as status:
        st.write("Đang lục lọi nhà bếp...")
        time.sleep(1)
        st.write("Đang tính toán calo...")
        time.sleep(1)
        status.update(label="Xong rồi!", state="complete")

    menu_here = create(knn, df, scaler, calo_muc_tieu, carb_can_thiet, protein_can_thiet, fat_can_thiet, so_bua_an)

    st.subheader("Thực đơn gợi ý (có thể sẽ lệch do dataset)")
    for i in range(3):
        mon_an = menu_here[i]
        with st.container(border=True):
            st.markdown(f"#### Bữa {i + 1}")
            st.write(f"Món ăn: {mon_an["Name"]} ")
            st.caption(f"Chi tiết: {mon_an["Calo (kcal)"]} kcal | {mon_an["Protein (g)"]} g Đạm | {mon_an["Carbs (g)"]} g Carbs | {mon_an["Fat (g)"]} g Fat")

mon_1 = menu_here[0]
mon_2 = menu_here[1]
mon_3 = menu_here[2]
#4. button
st.divider()
c1 = st.columns(1)
with c1:
    noi_dung_file = f"Thực đơn của bạn: \nBữa 1: {mon_1}\nBữa 2: {mon_2}\nBữa 3: {mon_3}"
    st.download_button(
        label="Tải thực đơn về máy (.txt)",
        data=noi_dung_file,
        file_name="thuc_don.txt",
        mime="text/plain",
    )