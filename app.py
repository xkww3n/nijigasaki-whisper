import streamlit as st
from pathlib import Path
from config import load_config
from audio_processor import process_uploaded_file, process_multiple_uploaded_files
from openai_client import transcribe_audio, batch_transcribe_audio

def main():
    st.set_page_config(
        page_title="Nijigasaki Whisper"
    )
    
    st.title("Nijigasaki Whisper", anchor=False)
    st.markdown("---")

    if not st.user.is_logged_in:
        st.button("登录", on_click=st.login)
        st.stop()

    st.success(f"欢迎，{st.user.name} 同学")
    st.button("登出", on_click=st.logout)
    
    config = load_config()
    if not config:
        st.stop()
    
    st.subheader("上传文件", anchor=False)

    uploaded_files = st.file_uploader(
        "选择音频或视频文件",
        type=config["app"]["supported_audio_formats"] + config["app"]["supported_video_formats"],
        accept_multiple_files=True
    )
    
    output_format = st.radio(
        "选择转写格式",
        options=["txt", "srt"],
        format_func=lambda x: "纯文本" if x == "txt" else "SRT 字幕",
        horizontal=True
    )
    
    if uploaded_files:
        file_count = len(uploaded_files)
        
        if st.button(f"开始转写 {file_count} 个文件", type="primary"):
            with st.spinner("处理文件中..."):
                if file_count > 1:
                    audio_paths, original_filenames = process_multiple_uploaded_files(uploaded_files)
                    
                    if audio_paths:
                        st.subheader("批量转写处理", anchor=False)
                        
                        content, mime_type, filename = batch_transcribe_audio(
                            audio_paths, original_filenames, config, output_format
                        )
                        
                        if content:
                            st.success(f"成功处理 {len(audio_paths)} 个文件")
                            st.download_button(
                                label="下载转写结果",
                                data=content,
                                file_name=filename,
                                mime=mime_type
                            )
                        else:
                            st.error("转写结果为空，无法下载")

                        for audio_path in audio_paths:
                            audio_path.unlink(missing_ok=True)
                    else:
                        st.error("处理文件时出错")
                
                else:
                    uploaded_file = uploaded_files[0]
                    uploaded_path = Path(uploaded_file.name)
                    audio_path = process_uploaded_file(uploaded_file)
                    
                    if audio_path:
                        transcription = transcribe_audio(audio_path, config, output_format)
                        
                        if transcription:
                            result = transcription.choices[0].message.content
                            if result:
                                st.subheader("转写结果", anchor=False)
                                st.text_area("转写结果", value=result, height=300, label_visibility="hidden", disabled=True)
                                st.download_button(
                                    label="下载转写结果",
                                    data=result,
                                    file_name=f"{uploaded_path.stem}.{output_format}",
                                    mime="text/plain"
                                )
                            else:
                                st.error("转写结果为空，无法下载")
                                
                        audio_path.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
