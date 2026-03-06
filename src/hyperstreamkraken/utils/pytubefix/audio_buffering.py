from io import BytesIO
import subprocess
from pytubefix import Stream, YouTube  # pyright: ignore[reportMissingTypeStubs]


def buffer_audio(video: YouTube) -> bytes:
    audio_stream: Stream | None = video.streams.get_audio_only()

    if audio_stream is None:
        raise ValueError(f"Audio stream of {video.watch_url} is None.")

    m4a_buffer = BytesIO()
    _ = audio_stream.stream_to_buffer(m4a_buffer)
    _ = m4a_buffer.seek(0)

    mp3_process = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            "pipe:0",
            "-f",
            "mp3",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "192k",
            "pipe:1",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    audio_bytes, _ = mp3_process.communicate(m4a_buffer.read())
    return audio_bytes
