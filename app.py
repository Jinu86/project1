import streamlit as st
import openai
import datetime
from typing import List, Dict

# GPT API 키 설정 (환경변수나 Secrets에 저장 권장)
openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else "YOUR_API_KEY"

# 할 일 저장소 (메모리 기반)
todo_list: List[Dict] = []

# GPT를 이용해 할 일 파싱하기
def parse_task(user_input: str) -> Dict:
    prompt = f"""
    다음 문장에서 할 일, 마감일, 중요도, 예상 소요 시간을 추정해서 JSON 형태로 정리해줘:
    "{user_input}"

    예시:
    입력: "내일까지 발표 자료 만들어야 해"
    출력: {{"task": "발표 자료 만들기", "deadline": "2025-05-14", "importance": "높음", "duration": "2시간"}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 텍스트를 일정 정보로 변환하는 도우미야."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        content = response['choices'][0]['message']['content']
        task_data = eval(content) if isinstance(content, str) else content
        return task_data
    except Exception as e:
        st.error("GPT 파싱 오류: " + str(e))
        return {}

# 우선순위 계산 기준
def sort_tasks(task_list: List[Dict]) -> List[Dict]:
    def priority_key(task):
        score = 0
        if task.get("importance") == "높음":
            score += 2
        if task.get("deadline"):
            try:
                d = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d")
                days_left = (d - datetime.datetime.today()).days
                score += max(0, 5 - days_left)
            except:
                pass
        return -score

    return sorted(task_list, key=priority_key)

# Streamlit 앱 시작
st.set_page_config(page_title="GPT 일정 도우미", layout="wide")
st.title("🗓️ GPT 일정 도우미")

st.markdown("""
자연어로 할 일을 입력하세요. 예: "오늘 밤까지 보고서 작성해야 해"
""")

user_input = st.text_input("할 일 입력:")

if st.button("추가하기") and user_input:
    task = parse_task(user_input)
    if task:
        todo_list.append(task)

# 완료한 일 체크
delete_task = st.selectbox("완료한 일이 있나요?", ["선택 안 함"] + [t["task"] for t in todo_list])
if delete_task != "선택 안 함":
    todo_list = [t for t in todo_list if t["task"] != delete_task]

# 정렬된 할 일 목록 표시
st.subheader("📌 오늘의 할 일 우선순위")
if todo_list:
    for task in sort_tasks(todo_list):
        st.markdown(f"- **{task['task']}** (📅 {task.get('deadline', '미정')}, ⏱ {task.get('duration', '알 수 없음')}, ⭐ {task.get('importance', '보통')})")
else:
    st.info("할 일을 입력해주세요!") 