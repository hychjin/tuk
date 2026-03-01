from google import genai 
from PIL import Image
import os
import requests


# 분류표 정의 (프롬프트에 포함될 내용)
CLASSIFICATION_TABLE = """
대분류 및 소분류 리스트:
1. 가방: 1.여성용가방, 2.남성용가방, 3.기타가방
2. 귀금속: 1.반지, 2.목걸이, 3.귀걸이, 4.시계, 5.기타
3. 도서용품: 1.학습서적, 2.소설, 3.컴퓨터서적, 4.만화책, 5.기타서적
4. 서류: 1.서류, 2.기타물품
5. 쇼핑백: 1.쇼핑백
6. 스포츠용품: 1.스포츠용품
7. 악기: 1.건반악기, 2.타악기, 3.관악기, 4.현악기, 5.기타악기
8. 유가증권: 1.어음, 2.상품권, 3.채권, 4.기타
9. 의류: 1.여성의류, 2.남성의류, 3.아기의류, 4.모자, 5.신발, 6.기타의류
10. 자동차: 1.자동차열쇠, 2.네비게이션, 3.자동차번호판, 4.임시번호판, 5.기타용품
11. 전자기기: 1.태블릿, 2.스마트워치, 3.무선이어폰, 4.카메라, 5.기타용품
12. 지갑: 1.여성용지갑, 2.남성용지갑, 3.기타지갑
13. 증명서: 1.신분증, 2.면허증, 3.여권, 4.기타
14. 컴퓨터: 1.삼성노트북, 2.LG노트북, 3.애플노트북, 4.기타
15. 카드: 1.신용(체크)카드, 2.일반카드, 3.교통카드, 4.기타카드
16. 현금
17. 휴대폰: 1.삼성휴대폰, 2.LG휴대폰, 3.아이폰, 4.기타휴대폰, 5.기타통신기기
18. 기타물품
"""

def analyze_image_with_ai(image_path, user_prompt):
    client = genai.Client(api_key="AIzaSyAGgsdPadhnI5dTYsnpaaDLP0qSstj2SP0")
    
    if not os.path.isfile(image_path):
        print(f"오류: '{image_path}' 파일이 존재하지 않습니다.")
        return None
    try:
        img = Image.open(image_path)
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[user_prompt, img]
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI 분석 중 오류 발생: {e}")
        return None

# 서버 전송 
def send_to_server(major_name, sub_name, image_path):
    server_url = "http://localhost:3000/api/analysis"
    payload = {
        "major_name": major_name,
        "sub_name": sub_name,
        "image_path": os.path.abspath(image_path)
    }
    
    try:
        response = requests.post(server_url, json=payload)
        if response.status_code == 200:
            print(f"서버 저장 성공: {major_name} > {sub_name}")
        else:
            print(f"서버 전송 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"네트워크 오류: {e}")

if __name__ == "__main__":
    image_file = "/Users/jin/Desktop/example/sorter/output.jpg" 
    
    # 프롬프트 
    prompt = f"""
    다음 규칙에 따라 이미지를 분석해줘:
    1. 아래 [리스트]에서 '대분류'와 '소분류' 명칭을 선택할 것.
    2. 출력 형식: '대분류이름.소분류이름' (예: 지갑.남성용지갑)
    3. 소분류가 없으면 '현금.' 처럼 마침표로 끝낼 것.
    [리스트]
    {CLASSIFICATION_TABLE}
    """
    
    result = analyze_image_with_ai(image_file, prompt)
    
    if result and "." in result:
        # 결과 파싱 및 서버 전송 호출
        major, sub = result.split(".", 1)
        send_to_server(major.strip(), sub.strip(), image_file)
    else:
        print("분석 결과 형식이 올바르지 않습니다:", result)