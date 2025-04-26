import whisper

# 加载模型（可选 tiny, base, small, medium, large）
model = whisper.load_model("base")

# mp3文件路径
audio_path = "your_audio.mp3"

# 识别并生成srt字幕
result = model.transcribe(audio_path, language="zh", task="transcribe", verbose=True)

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# 生成SRT内容
def segments_to_srt(segments):
    srt = ""
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"].strip()
        srt += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt

srt_content = segments_to_srt(result["segments"])

# 保存为srt文件
with open("output.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)