# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro — 语音播报稳定版
"""
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
