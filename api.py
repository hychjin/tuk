'AIzaSyCOBtV8SKCpsamprXGG3q0rLT9V-eMKzn8'
from google import genai 
from PIL import Image
import os
# 분류표 정의 (프롬프트에 포함될 내용)
CLASSIFICATION_TABLE = """
대분류 및 소분류 리스트:
1. 가방: 1.여성용가방, 2.남성용가방, 3.기타가방
2. 귀금속: 1.반지, 2.목걸이, 3.귀걸이, 4.시계, 5.기타
3. 도서용품: 1.학습서적, 2.소설, 3.컴퓨터서적, 4.만화책, 5.기타서적
4. 서류: 1.서류, 2.기타물품
5. 쇼핑백: 1.쇼핑백
6. 스포츠용품: 1.스포츠용품
7. 악기: 건반악기, 1.타악기, 2.관악기, 3.현악기, 4.기타악기
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
19. 유류품: 1.무안공항유류품, 2.유류품
20. 무주물: 무주물
"""

def analyze_image_with_ai(image_path, user_prompt):
    # API 클라이언트 설정 (API 키)
    client = genai.Client(api_key="AIzaSyCOBtV8SKCpsamprXGG3q0rLT9V-eMKzn8")
    
    # 이미지 파일 확인 및 로드
    if not os.path.isfile(image_path):
        print(f"오류: '{image_path}' 파일이 존재하지 않습니다. 경로를 확인하세요.")
        return None
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"이미지 로드 중 오류 발생: {e}")
        return None

    # AI에 분석 요청
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[user_prompt, img]
        )
        return response.text
    except Exception as e:
        print(f"AI 분석 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    image_file = "/Users/jin/Desktop/example/opencv/output.jpg" 
    'prompt = "이 이미지 안에 있는 객체들을 탐지하고, 무엇인지 설명해줘."'
    # AI 지시사항
    prompt = f"""
    너는 분실물 분류 전문가야. 다음 규칙에 따라 이미지를 분석해줘:
    1. 아래 제공된 [대분류 및 소분류 리스트]에서만 선택할 것.
    2. 출력 형식은 반드시 '대분류번호. 소분류번호' 형식으로 한 줄만 출력할 것. 
       (예: 11.3)
    3. 만약 소분류가 없는 항목(예: 16. 현금)은 '번호.' 으로 출력할 것.
    4. 확실하지 않다면 해당 대분류의 '기타' 항목을 선택할 것.

    [대분류 및 소분러 리스트]
    {CLASSIFICATION_TABLE}
    """
    result = analyze_image_with_ai(image_file, prompt)
    
    if result:
        print("\n--- AI 분석 결과 ---")
        print(result)
        
    # 파일로 저장
    with open("sort_result.txt", "w", encoding="utf-8") as f:
        f.write(result)