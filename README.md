# JSON-Translation
json文件格式化，可以使用百度翻译接口翻译json内的指定key


```
    input_file = 'live.openapi.json'  # 输入JSON文件路径
    output_file = 'output.json'  # 输出JSON文件路径
    key_to_translate = 'tags'  # 要翻译的键名
    #translate_json_file_tags(input_file, output_file, 'zh', 'en')
    translate_json_file(input_file, output_file, key_to_translate, 'zh', 'en')
    print('翻译完成，已保存到：', output_file)
```
