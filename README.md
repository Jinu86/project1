# GPT 일정 도우미

GPT를 활용한 자연어 기반 할 일 관리 애플리케이션입니다.

## 기능

- 자연어로 할 일 입력
- GPT를 통한 할 일, 마감일, 중요도, 예상 소요 시간 자동 파싱
- 우선순위에 따른 할 일 정렬
- 완료한 일 체크 및 삭제

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yourusername/gpt-todo-assistant.git
cd gpt-todo-assistant
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. OpenAI API 키 설정
   - `.streamlit/secrets.toml` 파일 생성 (예시 파일 참고)
   - OpenAI API 키 입력

## 실행 방법

```bash
streamlit run app.py
```

## 주의사항

- 이 애플리케이션은 메모리 기반으로 작동하므로 새로고침 시 데이터가 초기화됩니다.
- OpenAI API 사용에 따른 비용이 발생할 수 있습니다. 