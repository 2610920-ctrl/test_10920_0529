import streamlit as st

# 1. 페이지 기본 설정 및 타이틀
st.set_page_config(page_title="스마트 자판기", page_icon="🥤", layout="centered")
st.title("🥤 스마트 데이터 자판기")
st.write("돈을 넣고 원하는 음료를 골라보세요!")

# 2. 자판기 상품 데이터 정의 (상품명: [가격, 아이콘])
ITEMS = {
    "콜라": [1500, "🥤"],
    "사이다": [1400, "🧪"],
    "이온음료": [1600, "⚡"],
    "캔커피": [1000, "☕"],
    "생수": [800, "💧"],
    "초코우유": [1200, "🍫"]
}

# 3. 세션 상태(Session State) 초기화 (돈, 장바구니 상태 유지용)
if "balance" not in st.session_state:
    st.session_state.balance = 0
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 레이아웃 분할 (왼쪽: 자판기 상품 / 오른쪽: 투입구 및 결제) ---
col1, col2 = st.columns([3, 2])

# [왼쪽 열: 상품 투입구]
with col1:
    st.subheader("🛒 상품 목록")
    
    # 2열 격자 형태로 상품 배치
    grid_cols = st.columns(2)
    for idx, (item_name, info) in enumerate(ITEMS.items()):
        price, icon = info
        with grid_cols[idx % 2]:
            st.info(f"**{icon} {item_name}**\n\n 가격: {price:,}원")
            # 선택 버튼
            if st.button(f"{item_name} 담기", key=f"btn_{item_name}"):
                if st.session_state.balance >= price:
                    # 장바구니에 추가 및 잔액 차감
                    st.session_state.cart[item_name] = st.session_state.cart.get(item_name, 0) + 1
                    st.session_state.balance -= price
                    st.toast(f"🎈 {item_name}이(가) 장바구니에 담겼습니다!", icon="✅")
                else:
                    st.error("잔액이 부족합니다! 돈을 더 넣어주세요.")

# [오른쪽 열: 돈 투입구 및 영수증]
with col2:
    st.subheader("💰 금액 투입")
    
    # 금액 투입 버튼들
    money_cols = st.columns(3)
    with money_cols[0]:
        if st.button("+500원"):
            st.session_state.balance += 500
    with money_cols[1]:
        if st.button("+1,000원"):
            st.session_state.balance += 1000
    with money_cols[2]:
        if st.button("+5,000원"):
            st.session_state.balance += 5000
            
    # 현재 잔액 표시
    st.metric(label="현재 잔액 (Balance)", value=f"{st.session_state.balance:,} 원")
    
    st.divider()
    
    # 장바구니 및 구매 내역
    st.subheader("🛍️ 내 장바구니")
    if st.session_state.cart:
        total_items = 0
        for item, count in st.session_state.cart.items():
            st.write(f"{ITEMS[item][1]} {item} x {count}개")
            total_items += count
        
        # 반환/초기화 버튼
        if st.button("🔴 잔돈 반환 및 초기화"):
            returned_money = st.session_state.balance
            st.session_state.balance = 0
            st.session_state.cart = {}
            st.success(f"거스름돈 {returned_money:,}원이 반환되었습니다. 이용해 주셔서 감사합니다!")
            st.rerun()
    else:
        st.caption("아직 구매한 상품이 없습니다. 돈을 넣고 상품을 선택하세요.")