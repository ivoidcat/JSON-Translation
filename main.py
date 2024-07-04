import requests
import json
import hashlib
import time

# 需要替换成您申请的百度翻译API的key
appid = ""
secretKey = ""
count = 0
def get_sign(text):
    m = hashlib.md5()
    sign_str = appid + text + "123" + secretKey
    sign = m.update(sign_str.encode('utf-8'))
    return m.hexdigest()

def translate(text):
    #PARAM_FROM_TO_OR_Q_EMPTY
    if text == '':
        return text
    global count
    time.sleep(0.03)
    params = {
        'q': text,
        'appid': appid,
        'salt': '123',
        'from': 'zh',
        'to': 'en',
        'sign': get_sign(text)
    }
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    response = requests.get(url, params=params,proxies={'http': '', 'https': ''})
    result = response.json()
    print(result)
    count += 1
    print(count, result["trans_result"][0]["dst"])
    return result["trans_result"][0]["dst"]
    return result

def translate_json(data, key_to_translate, from_lang='zh', to_lang='en'):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == key_to_translate and isinstance(value, str):
                data[key] = translate(value)
            else:
                translate_json(value, key_to_translate, from_lang, to_lang)
    elif isinstance(data, list):
        for item in data:
            translate_json(item, key_to_translate, from_lang, to_lang)
    return data

#翻译某个键
def translate_json_file(input_file, output_file, key_to_translate, from_lang='zh', to_lang='en'):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 翻译JSON数据中指定键的值
    data = translate_json(data, key_to_translate, from_lang, to_lang)

    # 保存翻译后的JSON数据
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def translate_tags(data, from_lang='zh', to_lang='en'):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'tags' and isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], str):
                        value[i] = translate(value[i])
            else:
                translate_tags(value, from_lang, to_lang)
    elif isinstance(data, list):
        for item in data:
            translate_tags(item, from_lang, to_lang)
    return data

#翻译遍历tags
def translate_json_file_tags(input_file, output_file, from_lang='zh', to_lang='en'):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 翻译JSON数据中所有tags数组中的值
    data = translate_tags(data, from_lang, to_lang)

    # 保存翻译后的JSON数据
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_file = 'live.openapi.json'  # 输入JSON文件路径
    output_file = 'output.json'  # 输出JSON文件路径
    key_to_translate = 'tags'  # 要翻译的键名
    #translate_json_file_tags(input_file, output_file, 'zh', 'en')
    translate_json_file(input_file, output_file, key_to_translate, 'zh', 'en')
    print('翻译完成，已保存到：', output_file)
