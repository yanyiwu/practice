import whisper

# 加载模型（可选 tiny, base, small, medium, large）
model = whisper.load_model("base")

# mp3文件路径
audio_path = "your_audio.mp3"

# 识别并生成srt字幕
result = model.transcribe(audio_path, language="zh", task="transcribe", verbose=True)

# 保存为srt文件
with open("output.srt", "w", encoding="utf-8") as f:
    f.write(result["srt"])