from openai import OpenAI
import streamlit as st
import base64
import os
import zipfile
from pathlib import Path
import tempfile

def setup_openai_client(config):
    try:
        client = OpenAI(
            api_key=config["openai"]["api_key"],
            base_url=config["openai"]["api_base"]
        )
        return client
    except Exception as e:
        st.exception(e)
        return None

def transcribe_audio(audio_file_path, config, format):
    client = setup_openai_client(config)
    if not client:
        return None
    
    if format == "txt":
        selected_prompt = "请以纯文本格式输出转写结果，一句话一行，不要添加Markdown代码块标记等任何额外内容"
    else:
        selected_prompt = "请以SRT字幕格式输出转写结果，一句话一行，不要添加Markdown代码块标记等任何额外内容"

    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.chat.completions.create(
                model="gpt-4o-audio-preview",
                messages=[
                    {"role": "system", "content":
                        '''
                        你是一名音频转写员，
                        请严格按照用户要求的格式，
                        直接返回转写结果，
                        不要解释你收到/回答的内容，
                        也不要在返回内容中添加Markdown代码块标记等任何额外内容
                        '''
                    },
                    {"role": "user", "content": [
                            {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": base64.b64encode(audio_file.read()).decode('utf-8'),
                                    "format": "mp3"
                                }
                            },
                            {
                                "type": "text",
                                "text": selected_prompt
                            },
                        ]
                    }
                ]
            )
        return response
    except Exception as e:
        st.error(f"转写音频时出错: {str(e)}")
        return None

def batch_transcribe_audio(audio_files_paths, original_filenames, config, format):
    if not audio_files_paths:
        return None, None, None
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        output_files = []
        
        for i, (audio_path, original_name) in enumerate(zip(audio_files_paths, original_filenames)):
            progress_text = f"处理文件 {i+1}/{len(audio_files_paths)}: {original_name}"
            st.text(progress_text)
            
            transcription = transcribe_audio(audio_path, config, format)
            
            if transcription:
                result = transcription.choices[0].message.content
                if result:
                    output_filename = f"{Path(original_name).stem}.{format}"
                    output_path = temp_dir_path / output_filename
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result)
                    
                    output_files.append(output_path)
        
        if not output_files:
            return None, None, None
        
        if len(output_files) == 1:
            with open(output_files[0], "rb") as f:
                content = f.read()
            return content, "text/plain", output_files[0].name
        
        zip_path = temp_dir_path / "transcriptions.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_path in output_files:
                zipf.write(file_path, arcname=file_path.name)
        
        with open(zip_path, "rb") as f:
            content = f.read()
        
        return content, "application/zip", "transcriptions.zip"
