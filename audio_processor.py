import filetype
import ffmpeg
from pathlib import Path

def ffmpeg_convert(path, format):
    (
        ffmpeg
        .input(path)
        .output(f'{path}.{format}')
        .run()
    )
    return Path(f'{path}.{format}')

def process_uploaded_file(uploaded_file):
    tmp_store = Path("./tmp")
    tmp_store.mkdir(exist_ok=True)
    tmp_file = tmp_store/str(hash(uploaded_file.getvalue()))
    with open(tmp_file, mode="wb") as f:
        f.write(uploaded_file.getvalue())

    file_type = filetype.guess(tmp_file)

    if file_type:
        if file_type.mime == "audio/mpeg":
            audio_path = tmp_file
        elif file_type.mime in {
              "video/3gpp",
              "video/mp4",
              "video/x-m4v",
              "video/x-matroska",
              "video/webm",
              "video/quicktime",
              "video/x-msvideo",
              "video/x-ms-wmv",
              "video/mpeg",
              "video/x-flv",
              "audio/aac",
              "audio/mp4",
              "audio/ogg",
              "audio/x-flac",
              "audio/x-wav"
            }:
            audio_path = ffmpeg_convert(tmp_file, "mp3")
            tmp_file.unlink()
    return audio_path

def process_multiple_uploaded_files(uploaded_files):
    audio_paths = []
    original_filenames = []
    
    for uploaded_file in uploaded_files:
        audio_path = process_uploaded_file(uploaded_file)
        if audio_path:
            audio_paths.append(audio_path)
            original_filenames.append(uploaded_file.name)
    
    return audio_paths, original_filenames
