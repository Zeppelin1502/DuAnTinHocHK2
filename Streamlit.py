import streamlit as st
import time
from Backend import tinh_TDEE, tinh_Tong_TDEE

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
calo_tieu_thu = tinh_Tong_TDEE(can_nang, chieu_cao, tuoi, gioi_tinh, van_dong)
#2. main
st.title("🥗 AI Nutritionist - Trợ lý Dinh dưỡng Cá nhân của bạn!")
st.subheader("Chỉ số của cơ thể")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Mục tiêu Calo/ngày", f" {calo_muc_tieu} kcal") # Thay "---" bằng biến logic
with col2:
    st.metric("Đạm khuyên dùng", "--- g")      # Thay "---" bằng biến logic
with col3:
    st.metric("Tổng năng lượng tiêu mỗi ngày", f"{calo_tieu_thu} kcal")   # Thay "---" bằng biến logic
st.divider()
#3. button
if st.button(" TẠO THỰC ĐƠN!", use_container_width=True, type="primary"):
    with st.status("Đang tính toán...") as status:
        st.write("Đang lục lọi nhà bếp...")
        time.sleep(1)
        st.write("Đang tính toán calo...")
        time.sleep(1)
        status.update(label="Xong rồi!", state="complete")


    st.subheader("Thực đơn gợi ý")
    for i in range(so_bua_an):
        with st.container(border=True):
            st.markdown(f"#### Bữa {i + 1}")
            st.write("Món ăn: (bla bla...)")
            st.caption("Chi tiết: -- kcal | --g Đạm | --g Carbs")
#4. button
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.button("Đổi món khác")
with c2:
    st.button("Tải thực đơn (PDF/CSV)")