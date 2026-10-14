
import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="Tính chỉ số DTI",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 HỆ THỐNG TÍNH CHỈ SỐ DTI")
st.write("Công cụ hỗ trợ đánh giá khả năng vay vốn của khách hàng cá nhân.")

st.divider()

# Nhập thông tin khách hàng
st.subheader("📋 Thông tin khoản vay")

STV = st.number_input(
    "Số tiền vay (VNĐ)",
    min_value=0,
    value=800_000_000,
    step=10_000_000
)

THV = st.number_input(
    "Thời hạn vay (năm)",
    min_value=1,
    value=5,
    step=1
)

LS = st.number_input(
    "Lãi suất vay (%/năm)",
    min_value=0.0,
    value=12.0,
    step=0.5
)

st.subheader("💰 Thông tin tài chính hàng tháng")

TN = st.number_input(
    "Thu nhập hàng tháng (VNĐ)",
    min_value=0,
    value=45_000_000,
    step=1_000_000
)

NC = st.number_input(
    "Khoản nợ cũ hàng tháng (VNĐ)",
    min_value=0,
    value=10_000_000,
    step=1_000_000
)

CPSH = st.number_input(
    "Chi phí sinh hoạt mỗi người/tháng (VNĐ)",
    min_value=0,
    value=4_000_000,
    step=500_000
)

SN = st.number_input(
    "Số người trong gia đình",
    min_value=1,
    value=3,
    step=1
)

st.divider()

# Tính toán DTI
if st.button("🔍 TÍNH CHỈ SỐ DTI", use_container_width=True):

    # Quy đổi lãi suất từ % sang số thập phân
    lai_suat_thang = (LS / 100) / 12

    # Tiền gốc trả hàng tháng
    tien_goc_thang = STV / (THV * 12)

    # Tiền lãi hàng tháng theo công thức ban đầu
    tien_lai_thang = STV * lai_suat_thang

    # Tổng nghĩa vụ tài chính hàng tháng
    tong_nghia_vu = tien_goc_thang + tien_lai_thang + NC

    # Thu nhập còn lại sau chi phí sinh hoạt
    thu_nhap_kha_dung = TN - CPSH * SN

    if thu_nhap_kha_dung <= 0:
        st.error(
            "Không thể tính DTI hợp lệ vì thu nhập "
            "sau chi phí sinh hoạt không lớn hơn 0."
        )

    else:
        DTI = tong_nghia_vu / thu_nhap_kha_dung

        # Hiển thị kết quả
        st.subheader("📊 KẾT QUẢ ĐÁNH GIÁ")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Chỉ số DTI",
                f"{DTI * 100:.2f}%"
            )

        with col2:
            st.metric(
                "Ngưỡng đánh giá",
                "70%"
            )

        st.progress(min(DTI, 1.0))

        # Kết luận theo yêu cầu
        if DTI > 0.70:
            st.success("✅ KẾT LUẬN: KHÔNG ĐƯỢC VAY")
            st.write("DTI nhỏ hơn 70%.")

        else:
            st.error("❌ KẾT LUẬN: ĐƯỢC VAY")
            st.write("DTI lớn hơn hoặc bằng 70%.")

        # Chi tiết tính toán
        with st.expander("Xem chi tiết tính toán"):
            st.write(
                f"Tiền gốc/tháng: {tien_goc_thang:,.0f} VNĐ"
            )
            st.write(
                f"Tiền lãi/tháng: {tien_lai_thang:,.0f} VNĐ"
            )
            st.write(
                f"Nợ cũ/tháng: {NC:,.0f} VNĐ"
            )
            st.write(
                f"Tổng nghĩa vụ hàng tháng: "
                f"{tong_nghia_vu:,.0f} VNĐ"
            )
            st.write(
                f"Thu nhập khả dụng: "
                f"{thu_nhap_kha_dung:,.0f} VNĐ"
            )
