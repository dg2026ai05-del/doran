import streamlit as st
import re

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="물리학 공식 사전",
    page_icon="⚛️",
    layout="wide",
)

# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background: #0d1117; }

.main-header {
    text-align: center;
    padding: 2.5rem 1rem 1.8rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 2rem;
}
.tag {
    display: inline-block;
    background: rgba(88,166,255,0.15);
    color: #58a6ff;
    border: 1px solid #58a6ff55;
    border-radius: 999px;
    font-size: 0.73rem;
    font-weight: 600;
    padding: 0.18rem 0.9rem;
    letter-spacing: 0.08em;
    margin-bottom: 0.85rem;
}
.main-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #e6edf3;
    margin: 0 0 0.35rem;
}
.main-header p { color: #7d8590; font-size: 0.88rem; margin: 0; }

.unit-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 1.8rem 1.4rem;
    text-align: center;
    transition: all 0.2s ease;
}
.unit-card .icon { font-size: 2.5rem; margin-bottom: 0.7rem; }
.unit-card h3 { color: #e6edf3; font-size: 1.1rem; font-weight: 700; margin: 0 0 0.3rem; }
.unit-card p  { color: #7d8590; font-size: 0.8rem; margin: 0; line-height: 1.5; }

.formula-btn {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 3px solid #58a6ff;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.55rem;
}
.formula-btn h4 { color: #e6edf3; font-size: 0.95rem; margin: 0 0 0.2rem; font-weight: 600; }
.formula-btn p  { color: #7d8590; font-size: 0.79rem; margin: 0; }

.section-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
}
.sec-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.blue  { color: #58a6ff; }
.green { color: #3fb950; }
.amber { color: #d29922; }

.var-row {
    display: flex;
    gap: 1rem;
    padding: 0.38rem 0;
    border-bottom: 1px solid #21262d;
    font-size: 0.86rem;
}
.var-row:last-child { border-bottom: none; }
.var-sym { color: #79c0ff; min-width: 140px; font-weight: 500; }
.var-dsc { color: #8b949e; }

.step {
    padding: 0.42rem 0;
    color: #c9d1d9;
    font-size: 0.87rem;
    line-height: 1.7;
    border-bottom: 1px solid #21262d;
}
.step:last-child { border-bottom: none; }

.example-q {
    background: rgba(210,153,34,0.09);
    border: 1px solid #d2991f44;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.6rem;
}
.example-q .ql { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; color: #d29922; margin-bottom: 0.4rem; }
.example-q .qt { color: #e6edf3; font-size: 0.88rem; line-height: 1.6; }

.example-a {
    background: rgba(63,185,80,0.07);
    border: 1px solid #3fb95044;
    border-radius: 10px;
    padding: 1rem 1.3rem;
}
.example-a .al { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; color: #3fb950; margin-bottom: 0.4rem; }
.example-a .at { color: #c9d1d9; font-size: 0.87rem; line-height: 1.85; }

.breadcrumb {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    padding: 0.6rem 1rem;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    color: #7d8590;
}
.bc-link { color: #58a6ff; }
.bc-sep  { color: #30363d; }
.bc-cur  { color: #c9d1d9; }

.stButton > button {
    background: #21262d !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.84rem !important;
    padding: 0.38rem 1rem !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #30363d !important;
    border-color: #58a6ff !important;
    color: #e6edf3 !important;
}
.stMarkdown p { color: #c9d1d9; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 데이터 (2022개정 고등 물리학 3단원)
# ─────────────────────────────────────────
DATA = {
    "(1) 힘과 에너지": {
        "icon": "🔭",
        "desc": "운동, 힘, 에너지 보존 법칙",
        "formulas": {
            "등가속도 운동 3공식": {
                "latex": [
                    r"v = v_0 + at",
                    r"s = v_0 t + \dfrac{1}{2}at^2",
                    r"v^2 = v_0^2 + 2as",
                ],
                "desc": "초속도 $v_0$, 가속도 $a$ 로 직선 운동하는 물체의 속도·변위를 시간 $t$ 의 함수로 나타낸 운동 방정식입니다.",
                "vars": {
                    "$v$": "나중 속도 (m/s)",
                    "$v_0$": "초기 속도 (m/s)",
                    "$a$": "가속도 (m/s²)",
                    "$t$": "시간 (s)",
                    "$s$": "변위 (m)",
                },
                "derivation": [
                    "① **1식**: 가속도 정의 $a = \\Delta v / \\Delta t$ 에서 $v = v_0 + at$",
                    "② **2식**: 속도-시간 그래프 넓이(사다리꼴) = 변위 → $s = v_0 t + \\frac{1}{2}at^2$",
                    "③ **3식**: ①에서 $t = \\frac{v-v_0}{a}$ 를 ②에 대입 → $v^2 = v_0^2 + 2as$",
                ],
                "example": {
                    "q": "정지 상태에서 출발한 자동차가 가속도 $2\\,\\text{m/s}^2$ 로 달릴 때, 5초 후의 속도와 이동 거리를 구하시오.",
                    "a": [
                        "속도: $v = 0 + 2 \\times 5 = 10\\,\\text{m/s}$",
                        "변위: $s = \\frac{1}{2} \\times 2 \\times 25 = 25\\,\\text{m}$",
                    ],
                },
            },
            "뉴턴 제2법칙": {
                "latex": [r"F = ma"],
                "desc": "물체에 작용하는 알짜힘 $F$ 는 질량 $m$ 과 가속도 $a$ 의 곱과 같습니다.",
                "vars": {
                    "$F$": "알짜힘 (N)",
                    "$m$": "질량 (kg)",
                    "$a$": "가속도 (m/s²)",
                },
                "derivation": [
                    "① 운동량의 시간 변화율이 힘에 비례: $F \\propto \\Delta p / \\Delta t$",
                    "② 질량 일정 시 $\\Delta p / \\Delta t = ma$",
                    "③ 비례상수 = 1 (단위 정의) → $F = ma$",
                ],
                "example": {
                    "q": "질량 $5\\,\\text{kg}$ 인 물체에 알짜힘 $20\\,\\text{N}$ 이 작용할 때 가속도는?",
                    "a": ["$a = F/m = 20/5 = 4\\,\\text{m/s}^2$"],
                },
            },
            "운동에너지 & 일-에너지 정리": {
                "latex": [
                    r"E_k = \dfrac{1}{2}mv^2",
                    r"W = \Delta E_k",
                ],
                "desc": "운동하는 물체가 가지는 에너지. 알짜힘이 한 일은 운동에너지 변화량과 같습니다.",
                "vars": {
                    "$E_k$": "운동에너지 (J)",
                    "$m$": "질량 (kg)",
                    "$v$": "속도 (m/s)",
                    "$W$": "알짜힘이 한 일 (J)",
                },
                "derivation": [
                    "① $W = Fs = mas$ 에 $2as = v^2 - v_0^2$ 적용",
                    "② $W = \\frac{1}{2}mv^2 - \\frac{1}{2}mv_0^2 = \\Delta E_k$",
                    "③ 정지 기준 → $E_k = \\frac{1}{2}mv^2$",
                ],
                "example": {
                    "q": "질량 $4\\,\\text{kg}$, 속도 $3\\,\\text{m/s}$ 인 물체의 운동에너지는?",
                    "a": ["$E_k = \\frac{1}{2} \\times 4 \\times 9 = 18\\,\\text{J}$"],
                },
            },
            "역학적 에너지 보존": {
                "latex": [r"\dfrac{1}{2}mv^2 + mgh = \text{일정}"],
                "desc": "마찰이 없을 때 운동에너지와 중력 퍼텐셜에너지의 합은 보존됩니다.",
                "vars": {
                    "$\\frac{1}{2}mv^2$": "운동에너지 (J)",
                    "$mgh$": "중력 퍼텐셜에너지 (J)",
                    "$g$": "중력가속도 $9.8\\,\\text{m/s}^2$",
                    "$h$": "높이 (m)",
                },
                "derivation": [
                    "① 중력만 작용: 중력이 한 일 = 퍼텐셜에너지 감소",
                    "② 일-에너지 정리: 운동에너지 증가 = 퍼텐셜에너지 감소",
                    "③ $\\Delta E_k + \\Delta E_p = 0$ → $E_k + E_p = $ 일정",
                ],
                "example": {
                    "q": "높이 $10\\,\\text{m}$ 에서 정지 상태로 떨어진 물체가 지면 직전의 속도는? ($g=10$)",
                    "a": [
                        "$mgh = \\frac{1}{2}mv^2$",
                        "$v = \\sqrt{2 \\times 10 \\times 10} \\approx 14.1\\,\\text{m/s}$",
                    ],
                },
            },
            "만유인력 법칙": {
                "latex": [r"F = G\dfrac{m_1 m_2}{r^2}"],
                "desc": "질량 $m_1$, $m_2$ 인 두 물체 사이에 작용하는 인력. 거리의 제곱에 반비례합니다.",
                "vars": {
                    "$G$": "만유인력 상수 $6.674\\times10^{-11}\\,\\text{N·m}^2/\\text{kg}^2$",
                    "$m_1, m_2$": "두 물체의 질량 (kg)",
                    "$r$": "두 물체 사이 거리 (m)",
                },
                "derivation": [
                    "① 케플러 제3법칙 → 구심력 $\\propto 1/r^2$",
                    "② 두 질량에 각각 비례: $F \\propto m_1 m_2$",
                    "③ 비례상수 $G$ 도입 → $F = Gm_1m_2/r^2$",
                ],
                "example": {
                    "q": "질량 $6\\,\\text{kg}$ 과 $4\\,\\text{kg}$ 인 두 물체가 $2\\,\\text{m}$ 떨어졌을 때 인력은?",
                    "a": [
                        "$F = 6.674\\times10^{-11} \\times \\frac{24}{4} = 4.0\\times10^{-10}\\,\\text{N}$",
                    ],
                },
            },
        },
    },
    "(2) 전기와 자기": {
        "icon": "⚡",
        "desc": "전하, 전기장, 자기장, 전자기 유도",
        "formulas": {
            "쿨롱 법칙": {
                "latex": [r"F = k\dfrac{q_1 q_2}{r^2}"],
                "desc": "두 점전하 사이에 작용하는 전기력. 거리의 제곱에 반비례합니다.",
                "vars": {
                    "$k$": "쿨롱 상수 $8.99\\times10^9\\,\\text{N·m}^2/\\text{C}^2$",
                    "$q_1, q_2$": "전하량 (C)",
                    "$r$": "두 전하 사이 거리 (m)",
                },
                "derivation": [
                    "① 실험: $F \\propto q_1 q_2$, $F \\propto 1/r^2$",
                    "② 역제곱 법칙 + 비례상수 $k = 1/(4\\pi\\epsilon_0)$",
                    "③ $F = kq_1q_2/r^2$",
                ],
                "example": {
                    "q": "$2\\,\\mu\\text{C}$ 과 $3\\,\\mu\\text{C}$ 의 전하가 $0.1\\,\\text{m}$ 떨어진 경우 전기력은?",
                    "a": [
                        "$F = 8.99\\times10^9 \\times \\frac{2\\times10^{-6}\\times3\\times10^{-6}}{0.01}$",
                        "$= 5.39\\,\\text{N}$",
                    ],
                },
            },
            "옴의 법칙": {
                "latex": [r"V = IR"],
                "desc": "도체 양단의 전압은 전류와 저항의 곱. 전기회로 분석의 기본 법칙입니다.",
                "vars": {
                    "$V$": "전압 (V)",
                    "$I$": "전류 (A)",
                    "$R$": "저항 (Ω)",
                },
                "derivation": [
                    "① 옴 실험: 금속 도체에서 $V \\propto I$ (온도 일정)",
                    "② 비례상수를 저항 $R$ 로 정의",
                    "③ 미시적: $R = \\rho L / A$",
                ],
                "example": {
                    "q": "저항 $15\\,\\Omega$ 에 $3\\,\\text{A}$ 가 흐를 때 전압은?",
                    "a": ["$V = 3 \\times 15 = 45\\,\\text{V}$"],
                },
            },
            "전기 에너지와 전력": {
                "latex": [
                    r"P = VI = I^2R = \dfrac{V^2}{R}",
                    r"E = Pt",
                ],
                "desc": "전기 소자에서 소비되는 전력과 전기 에너지를 나타냅니다.",
                "vars": {
                    "$P$": "전력 (W)",
                    "$E$": "전기 에너지 (J)",
                    "$t$": "시간 (s)",
                },
                "derivation": [
                    "① $P = W/t = QV/t = IV$",
                    "② $V = IR$ 대입 → $P = I^2R = V^2/R$",
                    "③ 에너지 = 전력 × 시간: $E = Pt$",
                ],
                "example": {
                    "q": "$220\\,\\text{V}$, $11\\,\\Omega$ 의 전열기를 10분 사용 시 전기 에너지는?",
                    "a": [
                        "$P = 220^2/11 = 4400\\,\\text{W}$",
                        "$E = 4400 \\times 600 = 2.64\\times10^6\\,\\text{J}$",
                    ],
                },
            },
            "패러데이 전자기 유도 법칙": {
                "latex": [r"\mathcal{E} = -N\dfrac{\Delta\Phi_B}{\Delta t}"],
                "desc": "자기 선속의 변화율에 의해 기전력이 유도됩니다. 발전기의 원리입니다.",
                "vars": {
                    "$\\mathcal{E}$": "유도 기전력 (V)",
                    "$N$": "코일 감은 수 (회)",
                    "$\\Phi_B = BA$": "자기 선속 (Wb)",
                    "$\\Delta t$": "시간 변화 (s)",
                },
                "derivation": [
                    "① 패러데이 실험: 자속 변화 → 전류 유도",
                    "② 렌츠 법칙: 유도 전류는 자속 변화를 방해 (음의 부호)",
                    "③ 정량화 → $\\mathcal{E} = -N\\Delta\\Phi_B/\\Delta t$",
                ],
                "example": {
                    "q": "100회 코일의 자기선속이 $0.1\\,\\text{s}$ 동안 $0.05\\,\\text{Wb}$ 변화 시 유도 기전력은?",
                    "a": ["$|\\mathcal{E}| = 100 \\times 0.05/0.1 = 50\\,\\text{V}$"],
                },
            },
        },
    },
    "(3) 빛과 물질": {
        "icon": "🌈",
        "desc": "파동, 빛의 성질, 광전효과, 물질파",
        "formulas": {
            "파동의 기본 관계식": {
                "latex": [r"v = f\lambda"],
                "desc": "파동의 속도는 진동수와 파장의 곱. 모든 파동에 적용됩니다.",
                "vars": {
                    "$v$": "파동 속도 (m/s)",
                    "$f$": "진동수 (Hz)",
                    "$\\lambda$": "파장 (m)",
                },
                "derivation": [
                    "① 파동은 1주기 $T$ 마다 파장 $\\lambda$ 만큼 이동",
                    "② $v = \\lambda / T$",
                    "③ $f = 1/T$ 이므로 $v = f\\lambda$",
                ],
                "example": {
                    "q": "진동수 $440\\,\\text{Hz}$, 파장 $0.78\\,\\text{m}$ 인 소리의 속도는?",
                    "a": ["$v = 440 \\times 0.78 \\approx 343\\,\\text{m/s}$"],
                },
            },
            "스넬 법칙 (굴절 법칙)": {
                "latex": [r"n_1 \sin\theta_1 = n_2 \sin\theta_2"],
                "desc": "빛이 서로 다른 매질 경계면을 지날 때 입사각과 굴절각의 관계.",
                "vars": {
                    "$n_1, n_2$": "각 매질의 굴절률 (무차원)",
                    "$\\theta_1$": "입사각 (법선 기준)",
                    "$\\theta_2$": "굴절각 (법선 기준)",
                },
                "derivation": [
                    "① 빛 속도: $v_1 = c/n_1$, $v_2 = c/n_2$",
                    "② 하위헌스 원리: $\\sin\\theta_1/v_1 = \\sin\\theta_2/v_2$",
                    "③ 정리 → $n_1\\sin\\theta_1 = n_2\\sin\\theta_2$",
                ],
                "example": {
                    "q": "공기($n=1.0$) → 유리($n=1.5$), 입사각 $30°$ 일 때 굴절각은?",
                    "a": [
                        "$\\sin\\theta_2 = \\sin30°/1.5 = 0.333$",
                        "$\\theta_2 \\approx 19.5°$",
                    ],
                },
            },
            "광전효과 (아인슈타인 방정식)": {
                "latex": [r"E_k = hf - W"],
                "desc": "금속에 빛이 닿을 때 방출되는 광전자의 최대 운동에너지. 빛의 입자성 증명.",
                "vars": {
                    "$E_k$": "광전자 최대 운동에너지 (J 또는 eV)",
                    "$h$": "플랑크 상수 $6.626\\times10^{-34}\\,\\text{J·s}$",
                    "$f$": "입사광 진동수 (Hz)",
                    "$W$": "일함수 (금속마다 다름)",
                },
                "derivation": [
                    "① 광자 에너지 $hf$ 가 금속 전자에 전달",
                    "② 전자를 꺼내는 최소 에너지 = 일함수 $W$",
                    "③ 남은 에너지 → 운동에너지: $E_k = hf - W$",
                ],
                "example": {
                    "q": "일함수 $4.0\\,\\text{eV}$, 진동수 $1.5\\times10^{15}\\,\\text{Hz}$ 빛 입사. 최대 운동에너지는? ($h = 4.14\\times10^{-15}\\,\\text{eV·s}$)",
                    "a": [
                        "$hf = 4.14\\times10^{-15} \\times 1.5\\times10^{15} = 6.21\\,\\text{eV}$",
                        "$E_k = 6.21 - 4.0 = 2.21\\,\\text{eV}$",
                    ],
                },
            },
            "드브로이 물질파 파장": {
                "latex": [r"\lambda = \dfrac{h}{p} = \dfrac{h}{mv}"],
                "desc": "운동하는 입자도 파동성을 가지며 파장을 갖습니다. 양자역학의 핵심 개념입니다.",
                "vars": {
                    "$\\lambda$": "드브로이 파장 (m)",
                    "$h$": "플랑크 상수 $6.626\\times10^{-34}\\,\\text{J·s}$",
                    "$p = mv$": "운동량 (kg·m/s)",
                },
                "derivation": [
                    "① 아인슈타인 광자 운동량: $p = h/\\lambda$",
                    "② 드브로이 가설: 입자에도 동일 적용",
                    "③ 정리 → $\\lambda = h/mv$",
                ],
                "example": {
                    "q": "전자($m = 9.11\\times10^{-31}\\,\\text{kg}$)가 $10^6\\,\\text{m/s}$ 로 운동 시 드브로이 파장은?",
                    "a": [
                        "$\\lambda = \\frac{6.626\\times10^{-34}}{9.11\\times10^{-31}\\times10^6}$",
                        "$= 7.27\\times10^{-10}\\,\\text{m} \\approx 0.73\\,\\text{nm}$",
                    ],
                },
            },
        },
    },
}


# ─────────────────────────────────────────
# 세션 상태
# ─────────────────────────────────────────
for k, v in [("page", "unit"), ("unit", None), ("formula", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

def go(page, unit=None, formula=None):
    st.session_state.page    = page
    st.session_state.unit    = unit
    st.session_state.formula = formula
    st.rerun()


# ─────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <div class="tag">2022 개정교육과정 · 고등학교 물리학</div>
  <h1>⚛️ 물리학 공식 사전</h1>
  <p>단원을 선택하고 공식을 탐색하세요</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 단원 선택 페이지
# ─────────────────────────────────────────
if st.session_state.page == "unit":
    cols = st.columns(3, gap="large")
    for i, (unit_name, unit_data) in enumerate(DATA.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="unit-card">
              <div class="icon">{unit_data['icon']}</div>
              <h3>{unit_name}</h3>
              <p>{unit_data['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("단원 선택 →", key=f"u_{i}"):
                go("formula", unit=unit_name)


# ─────────────────────────────────────────
# 공식 선택 페이지
# ─────────────────────────────────────────
elif st.session_state.page == "formula":
    unit      = st.session_state.unit
    unit_data = DATA[unit]

    st.markdown(f"""
    <div class="breadcrumb">
      <span class="bc-link">물리학</span>
      <span class="bc-sep">›</span>
      <span class="bc-cur">{unit}</span>
    </div>
    """, unsafe_allow_html=True)

    col_back, _ = st.columns([1, 9])
    with col_back:
        if st.button("← 단원 목록"):
            go("unit")

    st.markdown(f"### {unit_data['icon']} {unit}")
    st.markdown(f"<p style='color:#7d8590;font-size:0.87rem;margin-bottom:1.5rem'>{unit_data['desc']}</p>",
                unsafe_allow_html=True)

    for fname, fdata in unit_data["formulas"].items():
        st.markdown(f"""
        <div class="formula-btn">
          <h4>{fname}</h4>
          <p>{fdata['desc'][:50]}…</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("자세히 보기 →", key=f"f_{fname}"):
            go("detail", unit=unit, formula=fname)


# ─────────────────────────────────────────
# 공식 상세 페이지
# ─────────────────────────────────────────
elif st.session_state.page == "detail":
    unit  = st.session_state.unit
    fname = st.session_state.formula
    fdata = DATA[unit]["formulas"][fname]

    st.markdown(f"""
    <div class="breadcrumb">
      <span class="bc-link">물리학</span>
      <span class="bc-sep">›</span>
      <span class="bc-link">{unit}</span>
      <span class="bc-sep">›</span>
      <span class="bc-cur">{fname}</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, _ = st.columns([1.3, 1.8, 7])
    with c1:
        if st.button("← 공식 목록"):
            go("formula", unit=unit)
    with c2:
        if st.button("↩ 단원 목록"):
            go("unit")

    st.markdown(f"## {fname}")
    st.markdown(f"<p style='color:#7d8590;font-size:0.9rem;margin-bottom:1.5rem'>{fdata['desc']}</p>",
                unsafe_allow_html=True)

    # 공식
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title blue">📐 핵심 공식</div>', unsafe_allow_html=True)
    for latex in fdata["latex"]:
        st.latex(latex)
    st.markdown('</div>', unsafe_allow_html=True)

    # 변수 설명
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title blue">📋 변수 설명</div>', unsafe_allow_html=True)
    for sym, desc in fdata["vars"].items():
        st.markdown(f"""
        <div class="var-row">
          <span class="var-sym">{sym}</span>
          <span class="var-dsc">{desc}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 유도 과정
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title green">🔬 유도 과정</div>', unsafe_allow_html=True)
    for step in fdata["derivation"]:
        st.markdown(f'<div class="step">', unsafe_allow_html=True)
        st.markdown(step)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 예제 문제
    st.markdown(f"""
    <div class="example-q">
      <div class="ql">📝 예제 문제</div>
      <div class="qt">{fdata['example']['q']}</div>
    </div>
    """, unsafe_allow_html=True)

    answer_lines = "<br>".join(fdata["example"]["a"])
    st.markdown(f"""
    <div class="example-a">
      <div class="al">✅ 풀이</div>
      <div class="at">{answer_lines}</div>
    </div>
    """, unsafe_allow_html=True)

    # 풀이 수식 렌더링
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔢 수식 렌더링 보기"):
        for line in fdata["example"]["a"]:
            matches = re.findall(r'\$(.*?)\$', line)
            for m in matches:
                st.latex(m)
