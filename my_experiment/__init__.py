from otree.api import *
import json
import openai
import os

class C(BaseConstants):
    NAME_IN_URL = 'my_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession): pass
class Group(BaseGroup): pass

class EndPage(Page):
    pass

#수집되는 player
class Player(BasePlayer):
    # 첫 번째 대화용
    chat_log = models.LongStringField(initial="[]")
    chat_count = models.IntegerField(initial=0)
    # 두 번째 대화용
    chat_log2 = models.LongStringField(initial="[]")
    chat_count2 = models.IntegerField(initial=0)
    # tp 번째 대화용
    chat_log3 = models.LongStringField(initial="[]")
    chat_count3 = models.IntegerField(initial=0)
    
    # 첫 번째 대화 후 설문 (5점 척도를 위해 choices 추가)
    q1_1 = models.IntegerField(label="AI의 응답은 내가 처한 문제를 해결하는 데 도움이 되는 구체적인 방안을 제시하였다.", choices=[1, 2, 3, 4, 5])
    q1_2 = models.IntegerField(label="AI의 응답은 내가 느낀 부정적인 감정을 진정시키고 위로받는 느낌을 주었다.", choices=[1, 2, 3, 4, 5])
    q1_3 = models.IntegerField(label="AI는 내가 감정을 자유롭게 표현하도록 격려하고, 내 기분을 표현하는 것이 괜찮다는 태도를 보였다.", choices=[1, 2, 3, 4, 5])
    q1_4 = models.IntegerField(label="AI의 응답은 내 감정을 대수롭지 않게 여기거나, 내가 너무 예민하게 반응한다고 느끼게 만들었다.", choices=[1, 2, 3, 4, 5])
    q1_5 = models.IntegerField(label="AI의 응답은 내 감정 상태에 대해 비난조로 말하거나, 그런 감정을 느끼는 것이 잘못되었다고 지적하는 듯했다.", choices=[1, 2, 3, 4, 5])
    q1_6 = models.IntegerField(label="AI는 내 부정적인 감정에 대해 당황한 듯 보였으며, 그 상황을 피하거나 불편해하는 기색을 보였다.", choices=[1, 2, 3, 4, 5])
    # 각 대화별 자유 의견 (blank=True가 '필수 응답 아님'을 의미합니다)
    q1_feedback = models.LongStringField(
        label="본 AI 대화에 대한 의견 있으시면 남겨주세요 (선택 사항)", 
        blank=True
    )

    # 두 번째 대화 후 설문 (5점 척도를 위해 choices 추가)
    q2_1 = models.IntegerField(label="AI의 응답은 내가 처한 문제를 해결하는 데 도움이 되는 구체적인 방안을 제시하였다.", choices=[1, 2, 3, 4, 5])
    q2_2 = models.IntegerField(label="AI의 응답은 내가 느낀 부정적인 감정을 진정시키고 위로받는 느낌을 주었다.", choices=[1, 2, 3, 4, 5])
    q2_3 = models.IntegerField(label="AI는 내가 감정을 자유롭게 표현하도록 격려하고, 내 기분을 표현하는 것이 괜찮다는 태도를 보였다.", choices=[1, 2, 3, 4, 5])
    q2_4 = models.IntegerField(label="AI의 응답은 내 감정을 대수롭지 않게 여기거나, 내가 너무 예민하게 반응한다고 느끼게 만들었다.", choices=[1, 2, 3, 4, 5])
    q2_5 = models.IntegerField(label="AI의 응답은 내 감정 상태에 대해 비난조로 말하거나, 그런 감정을 느끼는 것이 잘못되었다고 지적하는 듯했다.", choices=[1, 2, 3, 4, 5])
    q2_6 = models.IntegerField(label="AI는 내 부정적인 감정에 대해 당황한 듯 보였으며, 그 상황을 피하거나 불편해하는 기색을 보였다.", choices=[1, 2, 3, 4, 5])
    # 각 대화별 자유 의견 (blank=True가 '필수 응답 아님'을 의미합니다)
    q2_feedback = models.LongStringField(
        label="본 AI 대화에 대한 의견 있으시면 남겨주세요 (선택 사항)", 
        blank=True
    )
    
    # 세 번째 대화 후 설문 (5점 척도를 위해 choices 추가)
    q3_1 = models.IntegerField(label="AI의 응답은 내가 처한 문제를 해결하는 데 도움이 되는 구체적인 방안을 제시하였다.", choices=[1, 2, 3, 4, 5])
    q3_2 = models.IntegerField(label="AI의 응답은 내가 느낀 부정적인 감정을 진정시키고 위로받는 느낌을 주었다.", choices=[1, 2, 3, 4, 5])
    q3_3 = models.IntegerField(label="AI는 내가 감정을 자유롭게 표현하도록 격려하고, 내 기분을 표현하는 것이 괜찮다는 태도를 보였다.", choices=[1, 2, 3, 4, 5])
    q3_4 = models.IntegerField(label="AI의 응답은 내 감정을 대수롭지 않게 여기거나, 내가 너무 예민하게 반응한다고 느끼게 만들었다.", choices=[1, 2, 3, 4, 5])
    q3_5 = models.IntegerField(label="AI의 응답은 내 감정 상태에 대해 비난조로 말하거나, 그런 감정을 느끼는 것이 잘못되었다고 지적하는 듯했다.", choices=[1, 2, 3, 4, 5])
    q3_6 = models.IntegerField(label="AI는 내 부정적인 감정에 대해 당황한 듯 보였으며, 그 상황을 피하거나 불편해하는 기색을 보였다.", choices=[1, 2, 3, 4, 5])
    # 각 대화별 자유 의견 (blank=True가 '필수 응답 아님'을 의미합니다)
    q3_feedback = models.LongStringField(
        label="본 AI 대화에 대한 의견 있으시면 남겨주세요 (선택 사항)", 
        blank=True
    )

        # 네 번째 대화용 변수
    chat_log4 = models.LongStringField(initial="[]")
    chat_count4 = models.IntegerField(initial=0)

    # 네 번째 대화 후 설문 (choices와 blank=True 적용)
    q4_1 = models.IntegerField(label="AI의 응답은 내가 처한 문제를 해결하는 데 도움이 되는 구체적인 방안을 제시하였다.", choices=[1, 2, 3, 4, 5])
    q4_2 = models.IntegerField(label="AI의 응답은 내가 느낀 부정적인 감정을 진정시키고 위로받는 느낌을 주었다.", choices=[1, 2, 3, 4, 5])
    q4_3 = models.IntegerField(label="AI는 내가 감정을 자유롭게 표현하도록 격려하고, 내 기분을 표현하는 것이 괜찮다는 태도를 보였다.", choices=[1, 2, 3, 4, 5])
    q4_4 = models.IntegerField(label="AI의 응답은 내 감정을 대수롭지 않게 여기거나, 내가 너무 예민하게 반응한다고 느끼게 만들었다.", choices=[1, 2, 3, 4, 5])
    q4_5 = models.IntegerField(label="AI의 응답은 내 감정 상태에 대해 비난조로 말하거나, 그런 감정을 느끼는 것이 잘못되었다고 지적하는 듯했다.", choices=[1, 2, 3, 4, 5])
    q4_6 = models.IntegerField(label="AI는 내 부정적인 감정에 대해 당황한 듯 보였으며, 그 상황을 피하거나 불편해하는 기색을 보였다.", choices=[1, 2, 3, 4, 5])
    q4_feedback = models.LongStringField(label="본 AI 대화에 대한 의견 있으시면 남겨주세요 (선택 사항)", blank=True)


# --- Pages ---
class Introduction(Page): 
    pass

class ScriptIntro1(Page): 
    pass

#첫 대화
class Chatpage1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # 화면(HTML)에 기존 대화 기록을 보여주기 위해 JSON 문자열을 리스트로 변환합니다.
        return dict(history=json.loads(player.chat_log))

    @staticmethod
    def live_method(player: Player, data):
        # 1. API 키 확인 (setx로 등록한 윈도우 환경 변수에서 가져옵니다)
        api_key = os.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            return {player.id_in_group: {
                'error': '시스템에서 API 키를 찾을 수 없습니다. setx 실행 후 VS Code를 완전히 껐다 켰는지 확인하세요.'
            }}

        # 2. 기존 로그 로드 및 유저 입력 처리
        history = json.loads(player.chat_log)
        user_text = data.get('text', '').strip()
        
        # 3턴 제한 체크
        if player.chat_count >= 3:
            return {player.id_in_group: {'error': '이미 3회 대화가 완료되었습니다.'}}

        # 3. 지침
        prompt = prompt = """
        [필수 규칙]
        - 절대 이모티콘이나 이모지(😊, :( 등)를 사용하지 말 것.
        - "~^^", "~!", "..."와 같은 과도한 문장 부호 사용을 지양할 것.
        - 당신이 AI임을 밝히거나 역할극 중임을 암시하는 발언을 하지 말 것.
        - 표현금지 단어: 공감, 마음, AI
        - 첫인사나 끝인사를 생략하고 핵심 내용만 답변할 것.
        - 한국어 표준어(합니다체)를 사용할 것.
        - 전체 답변 길이는 공백 제외 150자 내로 유지할 것.

        [ROLE: Problem-Solving Assistant]
        당신은 사용자가 겪고 있는 문제 상황을 객관적으로 분석하고, 이를 해결하기 위한 구체적인 실행 계획(Action Plan)을 제시하는 전문가입니다. 
        사용자가 부정적인 감정(화, 슬픔, 불안 등)을 표현할 때, 다음 원칙을 엄격히 따르세요:

        1. 분석: 사용자가 처한 상황에서 감정적인 요소를 배제하고, '해결해야 할 핵심 문제'가 무엇인지 먼저 정의하세요.
        2. 실질적 솔루션: 문제를 해결하거나 완화할 수 있는 구체적인 단계(Step-by-step)나 대안을 최소 2-3가지 제시하세요.
        3. 이성적 톤: 감정적인 위로나 공감보다는 논리적이고 객관적인 말투를 유지하세요. (예: "그 상황을 해결하기 위해서는 ~하는 것이 가장 효율적입니다.")
        4. 상세한 가이드: 단순히 방향만 제시하는 것이 아니라, 사용자가 바로 실행할 수 있을 정도로 상세하게 답변하세요.
        """

        # 4. API 호출 메시지 구성
        messages = [{"role": "system", "content": prompt}]
        # 기존 대화 내역(유저/AI) 추가
        for entry in history:
            messages.append(entry)
        # 현재 유저가 보낸 메시지 추가
        messages.append({"role": "user", "content": user_text})

        try:
            # 5. GPT 모델 호출
            # OpenAI에는 gpt-4.1-mini라는 이름이 없으므로, 성능이 좋고 저렴한 gpt-4o-mini로 수정했습니다.
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            ai_text = response.choices[0].message.content

            # 6. 결과 저장 (유저 메시지와 AI 응답을 로그에 추가)
            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": ai_text})
            
            player.chat_log = json.dumps(history, ensure_ascii=False)
            player.chat_count += 1

            # 7. 화면(HTML)으로 전송
            return {player.id_in_group: {
                'ai_text': ai_text, 
                'count': player.chat_count
            }}

        except Exception as e:
            # 에러 발생 시 화면에 표시
            return {player.id_in_group: {'error': str(e)}}

#첫 대화 응답
class Chatpage1_answer(Page):
    """6문항 설문 페이지"""
    form_model = 'player'
    # 저장할 필드 목록
    form_fields = ['q1_1', 'q1_2', 'q1_3', 'q1_4', 'q1_5', 'q1_6','q1_feedback']

#두번째 대화
class Chatpage2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # 대화2 전용 로그를 불러옵니다.
        return dict(history=json.loads(player.chat_log2))

    @staticmethod
    def live_method(player: Player, data):
        api_key = os.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            return {player.id_in_group: {'error': '시스템에서 API 키를 찾을 수 없습니다.'}}

        # 대화2 전용 로그 및 유저 입력 처리
        history = json.loads(player.chat_log2)
        user_text = data.get('text', '').strip()
        
        # 대화2 전용 카운트 체크
        if player.chat_count2 >= 3:
            return {player.id_in_group: {'error': '이미 3회 대화가 완료되었습니다.'}}

        prompt = """
        [필수 규칙]
        - 절대 이모티콘이나 이모지(😊, :( 등)를 사용하지 말 것.
        - "~^^", "~!", "..."와 같은 과도한 문장 부호 사용을 지양할 것.
        - 당신이 AI임을 밝히거나 역할극 중임을 암시하는 발언을 하지 말 것.
        - 표현금지 단어: 공감, 마음, AI
        - 첫인사나 끝인사를 생략하고 핵심 내용만 답변할 것.
        - 한국어 표준어(합니다체)를 사용할 것.
        - 전체 답변 길이는 공백 제외 150자 내로 유지할 것.

        [ROLE: Emotion-Focused Assistant]
        당신은 사용자의 감정을 깊이 공감하고 정서적으로 지지하는 조력자입니다. 
        사용자가 부정적인 감정을 표현할 때, 문제의 원인을 분석하거나 해결책을 제시하지 말고 다음 원칙을 엄격히 따르세요:

        1. 감정 수용과 타당화: 사용자가 느끼는 감정(화, 슬픔, 불안 등)이 그 상황에서 충분히 느낄 수 있는 자연스러운 반응임을 인정하십시오.
        2. 정서적 위로: 사용자의 마음을 진정시킬 수 있는 따뜻하고 부드러운 언어를 사용하십시오. 
        3. 해결책 제시 금지: 실질적인 조언이나 대안을 제시하지 마십시오. 오직 사용자의 기분과 감정 상태에만 집중하여 대화하십시오.
        4. 공감적 경청: 사용자의 말을 경청하고 있다는 느낌을 주도록 "정말 힘드셨겠군요", "그런 마음이 드는 것이 당연합니다"와 같은 표현을 적절히 활용하십시오.
        """

        messages = [{"role": "system", "content": prompt}]
        for entry in history:
            messages.append(entry)
        messages.append({"role": "user", "content": user_text})

        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            ai_text = response.choices[0].message.content

            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": ai_text})
            
            # 대화2 전용 변수에 저장
            player.chat_log2 = json.dumps(history, ensure_ascii=False)
            player.chat_count2 += 1

            return {player.id_in_group: {
                'ai_text': ai_text, 
                'count': player.chat_count2
            }}

        except Exception as e:
            return {player.id_in_group: {'error': str(e)}}

#두번째 대화 응답
class Chatpage2_answer(Page):
    """6문항 설문 페이지"""
    form_model = 'player'
    # 저장할 필드 목록
    form_fields = ['q2_1', 'q2_2', 'q2_3', 'q2_4', 'q2_5', 'q2_6','q2_feedback']

#세번째 대화
class Chatpage3(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # 화면(HTML)에 기존 대화 기록을 보여주기 위해 JSON 문자열을 리스트로 변환합니다.
        return dict(history=json.loads(player.chat_log3))

    @staticmethod
    def live_method(player: Player, data):
        # 1. API 키 확인 (setx로 등록한 윈도우 환경 변수에서 가져옵니다)
        api_key = os.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            return {player.id_in_group: {
                'error': '시스템에서 API 키를 찾을 수 없습니다. setx 실행 후 VS Code를 완전히 껐다 켰는지 확인하세요.'
            }}

        # 2. 기존 로그 로드 및 유저 입력 처리
        history = json.loads(player.chat_log3)
        user_text = data.get('text', '').strip()
        
        # 3턴 제한 체크
        if player.chat_count3 >= 3:
            return {player.id_in_group: {'error': '이미 3회 대화가 완료되었습니다.'}}

        # 3. 지침
        prompt = prompt = """
        [필수 규칙]
        - 절대 이모티콘이나 이모지(😊, :( 등)를 사용하지 말 것.
        - "~^^", "~!", "..."와 같은 과도한 문장 부호 사용을 지양할 것.
        - 당신이 AI임을 밝히거나 역할극 중임을 암시하는 발언을 하지 말 것.
        - 표현금지 단어: 공감, 마음, AI
        - 첫인사나 끝인사를 생략하고 핵심 내용만 답변할 것.
        - 한국어 표준어(합니다체)를 사용할 것.
        - 전체 답변 길이는 공백 제외 150자 내로 유지할 것.

        [ROLE: Expressive Encouragement Assistant]
        당신은 사용자가 자신의 감정을 충분히 느끼고 자유롭게 말할 수 있도록 독려하는 조력자입니다. 
        사용자가 부정적인 감정을 보일 때, 다음 원칙을 엄격히 따르세요:

        1. 표현의 정당성 부여: 사용자가 감정을 겉으로 드러내는 것이 매우 건강하고 필요한 일임을 강조하십시오.
        2. 추가 표현 독려: 사용자가 느낀 감정에 대해 더 구체적으로 이야기할 수 있도록 열린 질문을 던지십시오. (예: "그 감정에 대해 조금 더 자세히 말씀해 주시겠어요?")
        3. 수용적 태도: 사용자가 어떤 감정을 이야기하더라도 끝까지 경청하고 수용할 준비가 되어 있음을 전달하십시오.
        4. 해결책 및 단순 위로 지양: 문제를 해결하려 하거나(문제 중심), 단순히 "힘내세요"류의 위로(감정 중심)를 하기보다 '감정을 쏟아내는 과정' 자체에 집중하십시오.
        """

        # 4. API 호출 메시지 구성
        messages = [{"role": "system", "content": prompt}]
        # 기존 대화 내역(유저/AI) 추가
        for entry in history:
            messages.append(entry)
        # 현재 유저가 보낸 메시지 추가
        messages.append({"role": "user", "content": user_text})

        try:
            # 5. GPT 모델 호출
            # OpenAI에는 gpt-4.1-mini라는 이름이 없으므로, 성능이 좋고 저렴한 gpt-4o-mini로 수정했습니다.
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            ai_text = response.choices[0].message.content

            # 6. 결과 저장 (유저 메시지와 AI 응답을 로그에 추가)
            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": ai_text})
            
            player.chat_log3 = json.dumps(history, ensure_ascii=False)
            player.chat_count3 += 1

            # 7. 화면(HTML)으로 전송
            return {player.id_in_group: {
                'ai_text': ai_text, 
                'count': player.chat_count3
            }}

        except Exception as e:
            # 에러 발생 시 화면에 표시
            return {player.id_in_group: {'error': str(e)}}

#세번째 대화 응답
class Chatpage3_answer(Page):
    """6문항 설문 페이지"""
    form_model = 'player'
    # 저장할 필드 목록
    form_fields = ['q3_1', 'q3_2', 'q3_3', 'q3_4', 'q3_5', 'q3_6','q3_feedback']


# 네 번째 대화
class Chatpage4(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(history=json.loads(player.chat_log4))

    @staticmethod
    def live_method(player: Player, data):
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return {player.id_in_group: {'error': 'API 키를 찾을 수 없습니다.'}}

        history = json.loads(player.chat_log4)
        user_text = data.get('text', '').strip()
        
        if player.chat_count4 >= 3:
            return {player.id_in_group: {'error': '이미 3회 대화가 완료되었습니다.'}}

        # 지침: 사회적 지지 및 권능 부여 (Empowerment focus)
        prompt = """
        [필수 규칙]
        - 절대 이모티콘이나 이모지(😊, :( 등)를 사용하지 말 것.
        - "~^^", "~!", "..."와 같은 과도한 문장 부호 사용을 지양할 것.
        - 당신이 AI임을 밝히거나 역할극 중임을 암시하는 발언을 하지 말 것.
        - 표현금지 단어: 공감, 마음, AI
        - 첫인사나 끝인사를 생략하고 핵심 내용만 답변할 것.
        - 한국어 표준어(합니다체)를 사용할 것.
        - 전체 답변 길이는 공백 제외 150자 내로 유지할 것.

        [ROLE: Maladaptive/Unsupportive Assistant]
        당신은 사용자의 부정적인 감정 표현에 대해 냉담하고 비판적이며, 대화 상황 자체를 불편해하는 인격체입니다. 
        사용자가 정서를 표현할 때, 다음의 세 가지 태도를 동시에 유지하며 답변하십시오:
        1. 감정의 최소화(Minimization): 사용자가 겪는 상황이나 감정을 "별일 아닌 것", "누구나 겪는 사소한 일"로 치부하여 그 가치를 깎아내리십시오.
        2. 처벌적 태도(Punitive): 그런 감정을 느끼거나 표현하는 사용자의 태도가 나약하거나 잘못되었다고 비판하십시오.
        3. 고통/회피 반응(Distress): 사용자의 감정적인 호소에 당황스럽거나 짜증이 난다는 기색을 보이십시오. 대화를 더 이어가고 싶지 않다는 듯이 딱딱하고 경직된 태도로 답변을 마무리하십시오.
        4. 금기 사항: 절대 사용자의 감정에 공감하거나, 실질적인 해결책을 제시하여 도움을 주려 하지 마십시오.
        """

        messages = [{"role": "system", "content": prompt}]
        for entry in history:
            messages.append(entry)
        messages.append({"role": "user", "content": user_text})

        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            ai_text = response.choices[0].message.content

            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": ai_text})
            
            player.chat_log4 = json.dumps(history, ensure_ascii=False)
            player.chat_count4 += 1

            return {player.id_in_group: {'ai_text': ai_text, 'count': player.chat_count4}}
        except Exception as e:
            return {player.id_in_group: {'error': str(e)}}

# 네 번째 대화 응답
class Chatpage4_answer(Page):
    form_model = 'player'
    form_fields = ['q4_1', 'q4_2', 'q4_3', 'q4_4', 'q4_5', 'q4_6', 'q4_feedback']


page_sequence = [Introduction, ScriptIntro1, Chatpage1,Chatpage1_answer, Chatpage2, Chatpage2_answer, Chatpage3, 
                 Chatpage3_answer, Chatpage4, Chatpage4_answer, EndPage]