import sys
import os
import re
import requests
from bs4 import BeautifulSoup
import json
import subprocess


def download_audio_from_xiaoyuzhou(url, output_filename=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 1. 先尝试直接查找 audio 标签
    audio_tag = soup.find("audio")
    audio_url = None
    if audio_tag and audio_tag.get("src"):
        candidate = audio_tag["src"]
        if candidate.startswith("https://media.xyzcdn.net/") and candidate.endswith(".m4a"):
            audio_url = candidate
    if not audio_url:
        # 2. 查找所有 script 标签，尝试提取正确的音频链接
        for script in soup.find_all("script"):
            if script.string and ("xyzcdn.net" in script.string or ".m4a" in script.string):
                # 用正则提取 https://media.xyzcdn.net/ 开头、.m4a 结尾的链接
                match = re.search(r'https://media\\.xyzcdn\\.net/[^"]+?\\.m4a', script.string)
                if not match:
                    match = re.search(r'https://media\.xyzcdn\.net/[^"\s]+?\.m4a', script.string)
                if match:
                    audio_url = match.group(0)
                    break
                # 或者尝试解析 JSON
                try:
                    data = json.loads(script.string)
                    # 递归查找 xyzcdn.net m4a 链接
                    def find_m4a(obj):
                        if isinstance(obj, dict):
                            for v in obj.values():
                                result = find_m4a(v)
                                if result:
                                    return result
                        elif isinstance(obj, list):
                            for item in obj:
                                result = find_m4a(item)
                                if result:
                                    return result
                        elif isinstance(obj, str):
                            if obj.startswith("https://media.xyzcdn.net/") and obj.endswith(".m4a"):
                                return obj
                        return None
                    audio_url = find_m4a(data)
                    if audio_url:
                        break
                except Exception:
                    continue

    if not audio_url:
        print("未找到音频链接！")
        return

    print(f"检测到音频链接: {audio_url}")
    
    # 获取原始文件名和后缀
    origin_filename = audio_url.split("/")[-1].split("?")[0]
    _, ext = os.path.splitext(origin_filename)
    if output_filename:
        filename = output_filename + ext
    else:
        filename = origin_filename
    output_path = filename

    with requests.get(audio_url, stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"音频已保存到: {output_path}")

    # 如果是m4a，自动转换为mp3
    if ext.lower() == ".m4a":
        mp3_filename = (output_filename if output_filename else os.path.splitext(origin_filename)[0]) + ".mp3"
        mp3_path = mp3_filename
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", output_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path
            ], check=True)
            print(f"已自动转换为MP3: {mp3_path}")
        except Exception as e:
            print(f"自动转换为MP3失败: {e}")


def main():
    if len(sys.argv) < 2:
        print("用法: python download_audio.py <小宇宙播客链接> [保存文件名]")
        sys.exit(1)
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.xiaoyuzhoufm.com/episode/66567094efabaae3a11c7fd8"
    output_filename = sys.argv[2] if len(sys.argv) > 2 else "S5E9"
    download_audio_from_xiaoyuzhou(url, output_filename)


if __name__ == "__main__":
    main() 