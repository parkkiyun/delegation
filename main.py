import streamlit as st
import importlib.util
import os

# 페이지 설정 (main.py에서만 설정)
st.set_page_config(page_title="멀티페이지 앱", page_icon="📄", layout="wide")

# teacher_pages 디렉토리 경로
TEACHER_PAGES_DIR = "teacher_pages"

# 디렉토리가 없으면 에러 처리
if not os.path.exists(TEACHER_PAGES_DIR):
    st.error(f"'{TEACHER_PAGES_DIR}' 디렉토리를 찾을 수 없습니다. 프로젝트 루트에 디렉토리를 생성하세요.")
else:
    # teacher_pages 폴더에서 파일 목록 가져오기
    page_files = sorted([f for f in os.listdir(TEACHER_PAGES_DIR) if f.endswith(".py")])

    # 사이드바에서 페이지 선택
    st.sidebar.title("선생님 메뉴")
    selected_page = st.sidebar.selectbox("메뉴 선택", page_files)

    # 페이지 로드 함수
    def load_teacher_page(page_file):
        page_path = os.path.join(TEACHER_PAGES_DIR, page_file)
        module_name = page_file.replace(".py", "")

        spec = importlib.util.spec_from_file_location(module_name, page_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    # 선택한 페이지 로드
    if page_files:
        load_teacher_page(selected_page)
    else:
        st.warning("선생님 페이지가 없습니다. 'teacher_pages/' 디렉토리에 파일을 추가하세요.")
