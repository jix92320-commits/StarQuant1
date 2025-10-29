# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro — 语音播报稳定版
"""
import os
VOICE_DIR = os.path.join(os.getcwd(), "voice_output")
os.makedirs(VOICE_DIR, exist_ok=True)
VOICE_PATH = os.path.join(VOICE_DIR, "voice_ai.mp3")
# 后面所有写临时mp3的地方，改用 VOICE_PATH

import os, tempfile
from gtts import gTTS
from playsound import playsound

def speak_text(text: str):
    try:
        if not text or len(text.strip()) < 5:
            return
        path = os.path.join(tempfile.gettempdir(), "voice_ai.mp3")
        tts = gTTS(text=text, lang='zh-cn')
        tts.save(path)
        playsound(path)
    except Exception as e:
        print("⚠️ 语音模块异常：", e)
