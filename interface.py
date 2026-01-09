import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from engine import QuantumImageProcessor
import io
import uuid
import time
import urllib.parse
import os

# --- 引擎初始化 (防止 NameError) ---
@st.cache_resource
def init_processor():
    return QuantumImageProcessor()

processor = init_processor()

# --- 核心配置：多国语言极简版 (无 Emoji) ---
LANG = {
    "EN": {
        "title": "Q-Memento: Quantum Moment Foundry",
        "sidebar_hdr": "Parameters",
        "btn": "Capture Quantum Moment",
        "img_download": "Save Image",
        "cert_download": "Download Certificate",
        "metric": "Quantum Energy Index",
        "guide_title": "Instructions",
        "steps": [
            "1. Upload a photo as the initial state.",
            "2. Select a mode for artistic evolution.",
            "3. Click to freeze a unique quantum moment.",
            "Note: Every image is globally unique."
        ],
        "share_hdr": "Social Verification",
        "modes": ["Collapse", "Tunneling", "Entanglement"]
    },
    "ZH": {
        "title": "Q-Memento 量子时刻纪念站",
        "sidebar_hdr": "设置参数",
        "btn": "开始捕捉量子瞬间",
        "img_download": "保存纪念图片",
        "cert_download": "下载认证证书",
        "metric": "量子能量激发指数",
        "guide_title": "操作指引",
        "steps": [
            "1. 上传照片作为量子演化的基底。",
            "2. 选择一种量子艺术演化模式。",
            "3. 点击按钮，捕捉不可重复的随机瞬间。",
            "注：每一张生成的图片在全网都是唯一的。"
        ],
        "share_hdr": "社交验证与分享",
        "modes": ["星尘模式 (Collapse)", "穿梭模式 (Tunneling)", "幻影模式 (Entanglement)"]
    },
    "DE": {
        "title": "Q-Memento: Quantenmoment-Gießerei",
        "sidebar_hdr": "Konfiguration",
        "btn": "Moment Erfassen",
        "img_download": "Bild Speichern",
        "cert_download": "Zertifikat Herunterladen",
        "metric": "Quantenenergie-Index",
        "guide_title": "Anleitung",
        "steps": ["1. Foto hochladen.", "2. Modus wählen.", "3. Moment einfrieren."],
        "share_hdr": "Soziale Verifizierung",
        "modes": ["Kollaps", "Tunnelbau", "Verschränkung"]
    },
    "FR": {
        "title": "Q-Memento: Moments Quantiques",
        "sidebar_hdr": "Configuration",
        "btn": "Capturer le Moment",
        "img_download": "Enregistrer",
        "cert_download": "Certificat",
        "metric": "Indice d'Énergie",
        "guide_title": "Instructions",
        "steps": ["1. Télécharger.", "2. Sélectionner.", "3. Capturer."],
        "share_hdr": "Vérification Sociale",
        "modes": ["Effondrement", "Effet Tunnel", "Intrication"]
    },
    "IT": {
        "title": "Q-Memento: Momenti Quantistici",
        "sidebar_hdr": "Configurazione",
        "btn": "Cattura Momento",
        "img_download": "Salva",
        "cert_download": "Certificato",
        "metric": "Indice di Energia",
        "guide_title": "Istruzioni",
        "steps": ["1. Carica.", "2. Seleziona.", "3. Cattura."],
        "share_hdr": "Verifica Sociale",
        "modes": ["Collasso", "Effetto Tunnel", "Entanglement"]
    }
}

# --- 证书生成逻辑 (使用本地背景图) ---
def create_pro_certificate(token, prob, mode):
    W, H = 1200, 750
    bg_path = "cert_bg.jpg"
    
    # 尝试加载本地背景图，否则使用备用的深色底色
    if os.path.exists(bg_path):
        cert = Image.open(bg_path).convert("RGB").resize((W, H))
    else:
        cert = Image.new("RGB", (W, H), "#02050A")
        draw_temp = ImageDraw.Draw(cert)
        for i in range(0, W, 60): draw_temp.line([(i, 0), (i, H)], fill="#0A1E3D", width=1)
        for i in range(0, H, 60): draw_temp.line([(0, i), (W, i)], fill="#0A1E3D", width=1)

    draw = ImageDraw.Draw(cert)
    accent = "#00F2FF"
    
    # 装饰边框
    m = 40
    draw.rectangle([m, m, W-m, H-m], outline="#1E3A5F", width=2)
    
    # 证书核心文字信息
    draw.text((W//2, 110), "QUANTUM MOMENT CERTIFICATE", fill=accent, font_size=50, anchor="mm")
    
    y_start = 280
    data = [
        ("TOKEN ID", f"{token}"),
        ("PHYSICAL ENTROPY", f"{prob:.10%}"),
        ("OBSERVER MODE", f"{mode.upper()}"),
        ("TIMESTAMP", f"{time.strftime('%Y-%m-%d %H:%M:%S')}"),
        ("AUTH", "HADAMARD-GATE / WAVEFUNCTION COLLAPSE")
    ]
    
    for i, (label, val) in enumerate(data):
        draw.text((180, y_start + i*75), f"// {label}", fill="#4A90E2", font_size=22)
        draw.text((500, y_start + i*75), val, fill="#FFFFFF", font_size=26)

    footer = "VERIFIED BY Q-MEMENTO ENGINE | GLOBALLY UNIQUE DIGITAL ASSET"
    draw.text((W//2, H-80), footer, fill="#1E3A5F", font_size=18, anchor="mm")
    return cert

# --- UI 布局 ---
st.set_page_config(page_title="Q-Memento Pro", layout="wide")

lang_list = ["EN", "ZH", "DE", "FR", "IT"]
lang_choice = st.sidebar.selectbox("Language Selection", lang_list, index=0)
t = LANG[lang_choice]

# 侧边栏说明
st.sidebar.markdown(f"### {t['guide_title']}")
for step in t['steps']:
    st.sidebar.write(step)

st.sidebar.divider()

# 参数设置
st.sidebar.header(t["sidebar_hdr"])
mode_display = st.sidebar.selectbox("Mode", t['modes'])
mode_keys = ["collapse", "tunneling", "entanglement"]
# 自动映射索引
mode_idx = t['modes'].index(mode_display)
current_mode_key = mode_keys[mode_idx]

shots = st.sidebar.slider("Sampling Shots", 512, 4096, 2048)

# 主界面
st.title(t["title"])
st.write("---")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    c1, c2 = st.columns(2)
    with c1: st.image(img, use_container_width=True, caption="Initial State")
    
    if st.button(t["btn"], type="primary", use_container_width=True):
        with st.spinner("Calculating Quantum State..."):
            counts = processor.run_quantum_sampling(shots=shots)
            res_np = processor.process_image(np.array(img), counts, mode_key=current_mode_key)
            token = str(uuid.uuid4()).upper()[:16]
            prob = counts.get('1', 0) / shots
            
            st.session_state['res_img'] = Image.fromarray(res_np)
            st.session_state['cert_img'] = create_pro_certificate(token, prob, current_mode_key)
            st.session_state['token'] = token
            st.session_state['last_prob'] = prob

    if 'res_img' in st.session_state:
        with c2:
            st.image(st.session_state['res_img'], use_container_width=True)
            st.metric(t["metric"], f"{st.session_state['last_prob']:.4%}")
            
            cd1, cd2 = st.columns(2)
            buf1 = io.BytesIO(); st.session_state['res_img'].save(buf1, format="PNG")
            cd1.download_button(t["img_download"], buf1.getvalue(), "quantum_moment.png", use_container_width=True)
            
            buf2 = io.BytesIO(); st.session_state['cert_img'].save(buf2, format="PNG")
            cd2.download_button(t["cert_download"], buf2.getvalue(), "certificate.png", use_container_width=True)

            # X 分享逻辑
            st.divider()
            st.subheader(t["share_hdr"])
            share_text = f"My unique Quantum Memento. Token: {st.session_state['token']} via #QMemento"
            st.code(share_text, language=None)
            x_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}"
            st.link_button("Share to X (Twitter)", x_url, use_container_width=True)
        
        st.divider()
        st.subheader("Certificate Preview")
        st.image(st.session_state['cert_img'], use_container_width=True)
