from pytube import YouTube
import whisper
import pandas as pd

# video_url = "https://www.youtube.com/watch?v=p3j4qwVNTGk" 
# audio_file = YouTube(video_url).streams.filter(only_audio=True).first().download(filename="audio.mp4")
audio_file = "audio.mp4"

whisper_model = whisper.load_model("tiny")

# transcript_text = result["text"]
# transcript_text = ts.translate_text(transcript_text,translator='bing',to_language='ja')

transcription = whisper_model.transcribe(audio_file, language='ar',fp16=False,verbose=False)

df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])
print(df)

possibilities = [ 'سلو عليكم رحمة الله وركاته','سلام عليكم','أسلام','عليكم', 'السلام','ورحمة','ورحمتو','وبركاته','وبركاتهو','بركاته','السلام عليكم','سلام عليكم','سلام']
hastowork = 'سلام عليكم'
print(df['text'][0])

startTimes = []

for ind in df.index: 
    if any(word in df['text'][ind] for word in possibilities):
        startTimes.append(df['start'][ind])
        
        
print(startTimes)