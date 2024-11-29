import streamlit as st
import json
import os
import pyperclip

# 페이지 설정
st.set_page_config(page_title="선생님 페이지", page_icon="👨‍🏫")

# 초기 비밀번호 설정
PASSWORD = "teacher123"

# 인증 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def show_login():
    """로그인 화면"""
    # 중앙 정렬을 위한 컬럼 설정
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>선생님 페이지</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>접근하려면 비밀번호를 입력하세요.</p>", unsafe_allow_html=True)
        
        # 비밀번호 입력 필드
        password = st.text_input("비밀번호", type="password", key="password")
        
        # 로그인 버튼을 중앙에 배치
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            login_button = st.button("로그인")
        
        if login_button:
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")

def show_teacher_page():
    """선생님 페이지 메인"""
    st.markdown("<h1 style='text-align: center;'>선생님 페이지</h1>", unsafe_allow_html=True)
    st.write("위원회를 추가하고 학부모용 링크를 생성할 수 있습니다.")

    # 로그아웃 버튼을 오른쪽 상단에 배치
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("로그아웃"):
            st.session_state.authenticated = False
            st.rerun()

    # JSON 파일 경로
    json_file = "form_config.json"

    # 위원회 목록 표시
    st.subheader("📋 위원회 목록")
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            form_configs = json.load(f)
            
        # 그리드 형식으로 위원회 표시
        cols = st.columns(3)  # 3열 그리드
        for idx, (committee_name, config) in enumerate(form_configs.items()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                        <div style="
                            padding: 20px;
                            border-radius: 10px;
                            border: 1px solid #ddd;
                            margin: 10px 0;
                            background-color: white;">
                            <h3 style="margin: 0 0 10px 0;">{committee_name}</h3>
                            <p style="color: #666; margin: 5px 0;">위임장 제목: {config['title']} 위임장</p>
                        </div>
                        """, unsafe_allow_html=True)
                    if st.button("삭제", key=f"delete_{committee_name}"):
                        del form_configs[committee_name]
                        with open(json_file, "w", encoding="utf-8") as f:
                            json.dump(form_configs, f, ensure_ascii=False, indent=4)
                        st.success(f"'{committee_name}' 위원회가 삭제되었습니다.")
                        st.rerun()
    else:
        st.error("위원회 설정 파일이 없습니다.")

    # 위원회 추가
    st.write("---")
    st.subheader("➕ 위원회 추가")
    with st.form("new_form"):
        committee_name = st.text_input("위원회 이름")
        submit_button = st.form_submit_button("위원회 추가")
        
        if submit_button:
            if committee_name:
                # 동적으로 타이틀과 텍스트 생성
                form_configs[committee_name] = {
                    "title": committee_name,
                    "image_texts": [
                        f"{committee_name} 결정 사항에 동의합니다"
                    ]
                }
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(form_configs, f, ensure_ascii=False, indent=4)
                st.success(f"'{committee_name}' 위원회가 추가되었습니다.")
                st.rerun()
            else:
                st.error("위원회 이름을 입력하세요.")

    # 링크 생성
    st.write("---")
    st.subheader("🔗 위원회 링크 생성")
    if os.path.exists(json_file):
        selected_form = st.selectbox("위원회 선택", list(form_configs.keys()))
        base_url = st.text_input("앱 기본 URL", "https://parkkiyun-delegation-main-aymqew.streamlit.app/")
        
        # 생성된 링크를 세션 상태에 저장
        if "generated_link" not in st.session_state:
            st.session_state.generated_link = None
            
        if st.button("링크 생성"):
            if selected_form:
                st.session_state.generated_link = f"{base_url}?form_type={selected_form}"
        
        # 저장된 링크가 있으면 표시
        if st.session_state.generated_link:
            st.code(st.session_state.generated_link)
            
            # 복사 버튼
            if st.button("링크 복사"):
                pyperclip.copy(st.session_state.generated_link)
                st.success("링크가 클립보드에 복사되었습니다!")

# 메인 로직
if st.session_state.authenticated:
    show_teacher_page()
else:
    show_login()
