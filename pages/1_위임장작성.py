import streamlit as st
from PIL import Image
from app.resource_manager import ResourceManager
from app.tabs import info_input, signature_input, application_preview
import base64
import json
from io import BytesIO
import sys
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# helper_functions import
try:
    from app.helper_functions import render_signature_image
    print("helper_functions 임포트 성공")
except ImportError as e:
    print(f"Import 오류 발생: {e}")
    print(f"현재 Python 경로: {sys.path}")
    st.error("필요한 모듈을 불러올 수 없습니다.")

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 리소스 초기화
resources = ResourceManager()
resources.validate_resources()

# JSON 파일 로드
with open("form_config.json", "r", encoding="utf-8") as f:
    form_configs = json.load(f)

# URL Query Parameters 읽기
query_params = st.query_params
form_type = query_params.get("form_type", "학업성적관리위원회 위임장")

# form_config 가져오기
if form_type in form_configs:
    form_config = form_configs[form_type]
else:
    form_config = form_configs["학업성적관리위원회 위임장"]

# 로고 이미지 로드 및 크기 조정
logo = Image.open("images/logo.png")
# 서브타이틀 높이에 맞추도록 크기 조정 (약 50px 높이)
logo_height = 50
aspect_ratio = logo.size[0] / logo.size[1]
logo_width = int(logo_height * aspect_ratio)
logo = logo.resize((logo_width, logo_height))

# 타이틀과 서브타이틀을 포함할 컨테이너
col1, col2, col3 = st.columns([1, 3, 1])

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

with col2:
    # form_config에서 title 가져오기
    title_text = form_config.get("title", "학업성적관리위원회") + " 위임장"
    st.markdown(f"<h1 style='text-align: center;'>{title_text}</h1>", unsafe_allow_html=True)
    
    # 로고와 서브타이틀을 한 줄에 표시 (비율 조정)
    subcol1, subcol2, subcol3 = st.columns([2, 3, 1])
    with subcol1:
        # 오른쪽 정렬로 로고 표시
        st.markdown(
            f'<div style="display: flex; justify-content: flex-end;">'
            f'<img src="data:image/png;base64,{image_to_base64(logo)}" width="{logo_width}px" height="{logo_height}px">'
            f'</div>',
            unsafe_allow_html=True
        )
    with subcol2:
        # 가운데 정렬로 서브타이틀 표시
        st.markdown(
            '<h3 style="text-align: center; margin-top: 5px;">온양한올고등학교</h3>', 
            unsafe_allow_html=True
        )

# 탭 구성
tabs = st.tabs(["1. 정보 입력", "2. 서명 입력", "3. 신청서 확인 및 PDF 다운로드"])

# 각 탭의 기능 연결
with tabs[0]:
    info_input.render()

with tabs[1]:
    signature_input.render()

with tabs[2]:
    application_preview.render()
# 푸터 추가
st.markdown("---")  # 구분선
st.markdown(
    """
    <div style='text-align: center; color: #666666; padding: 10px;'>
    프로그램 문의: <a href='mailto:kiyun0515@naver.com'>kiyun0515@naver.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

