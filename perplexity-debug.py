import requests

# 从文件读取 API key
def read_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# 假设 API key 存储在当前目录的 'api_key.txt' 文件中
api_key = read_api_key('api_key.txt')

def make_api_request(api_key, prompt):
    url = 'https://api.perplexity.ai/chat/completions'  # 假设这是正确的 API 端点
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'sonar-medium-online',  # 更改为 Perplexity AI 支持的模型
        'messages': [{'role': 'user', 'content': prompt}]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# 主程序
if __name__ == "__main__":
    api_key = read_api_key('api_key.txt')
    
    while True:
        prompt = input("Enter your question (type 'quit' to exit): ")
        if prompt.lower() == 'quit':
            break
        
        response = make_api_request(api_key, prompt)
        print("\nAnswer:", response)
        print("\n" + "-"*50 + "\n")

