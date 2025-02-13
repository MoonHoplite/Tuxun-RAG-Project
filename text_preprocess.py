"""预处理文本"""
import re
from pathlib import Path
import os


def clean_file_data(input_path: str, output_path: str=None) -> None:
    if output_path is None:
        output_path = os.path.dirname(input_path)
        print(output_path)
    
    emoji = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF' u'\u2600-\u2B55 \U00010000-\U0010ffff]+')
    s = re.compile(r'\(https?://\S+|www\.\S+\)')
    pattern = r'</?font([^>]*)>'
    spattern = r'<sup>\[?[0-9]+\]?</?sup>'
    
    data = ""
    file_name = os.path.basename(input_path).replace(".md", "_cleaned.txt")
    
    with open(input_path,'r',encoding='utf-8') as f:
        line_text = f.read()
        data += line_text
    
    data = re.sub(emoji,'',data)
    data = re.sub(pattern,'',data)
    data = re.sub(s, '', data)
    data = re.sub(spattern,'',data)
    data = re.sub(r'\n','',data)
    data = re.sub(r'!\[\]','',data)
    data = re.sub(r'\*\*','',data)
    data = re.sub(r'<br/?>','',data)
    data = re.sub(r'\|','',data)
    data = re.sub(r' +',' ',data)
    data = re.sub(r'\:\-\-\-\:','',data)
    data = re.sub(r'#+','',data)
    data = re.sub(r'</?sup>','',data)

    ##要自己改路径
    with open(f"{output_path}/{file_name}",'w',encoding='utf-8') as h:
        h.write(data)


def preprocess(folder_path: Path=Path("raw_data")) -> None:
    "Preprocess all .md files in the folder"
    for filename in folder_path.rglob('*.md'):
        clean_file_data(filename)