import streamlit as st
import json
import os

# JSON 파일 경로
json_file = "form_config.json"

def render():
    st.title("선생님 페이지")
    st.write("신청서를 관리하고 학부모용 링크를 생성할 수 있습니다.")

    # 신청서 목록 표시
    st.subheader("신청서 목록")
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            form_configs = json.load(f)
        st.json(form_configs)
    else:
        st.error("신청서 설정 파일이 없습니다.")

    # 새 신청서 추가
    st.write("---")
    st.subheader("새 신청서 추가")
    new_form_name = st.text_input("신청서 이름")
    new_form_title = st.text_input("신청서 타이틀")
    new_form_texts = st.text_area("삽입할 텍스트 (쉼표로 구분)", "")

    if st.button("신청서 추가"):
        if new_form_name and new_form_title:
            form_configs[new_form_name] = {
                "title": new_form_title,
                "image_texts": [text.strip() for text in new_form_texts.split(",")]
            }
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(form_configs, f, ensure_ascii=False, indent=4)
            st.success(f"'{new_form_name}' 신청서가 추가되었습니다.")
        else:
            st.error("모든 필드를 입력하세요.")

    # 링크 생성
    st.write("---")
    st.subheader("신청서 링크 생성")
    selected_form = st.selectbox("신청서 선택", list(form_configs.keys()))
    base_url = st.text_input("앱 기본 URL", "https://your-app-url.com")

    if st.button("링크 생성"):
        if selected_form:
            generated_link = f"{base_url}?user_type=parent&form_type={selected_form}"
            st.code(generated_link)
