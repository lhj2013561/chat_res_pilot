from os import environ

SESSION_CONFIGS = [
    dict(
        name='my_experiment',
        display_name="AI 대화 파일럿",
        app_sequence=['my_experiment'],
        num_demo_participants=1,
    ),
]

# --- oTree 기본 설정 (삭제되면 에러가 발생합니다) ---
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, 
    participation_fee=0.00, 
    doc=""
)

# 언어 및 통화 설정
LANGUAGE_CODE = 'ko'
REAL_WORLD_CURRENCY_CODE = 'KRW'
USE_POINTS = True

# 관리자 보안 설정
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6734182590123' # 임의의 숫자 조합