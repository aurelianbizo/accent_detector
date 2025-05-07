from flask import Flask, request, jsonify, render_template
import moviepy  as mp
import speech_recognition as sr
import openai
import os
from dotenv import load_dotenv
import yt_dlp

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Initialize Flask app
app = Flask(__name__)

# Path to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY 

def download_video(url, output_path='video.mp4'):
    # Set options for the download
    ydl_opts = {
        'format': 'best',  # You can specify the format or quality here (e.g., 'best', 'worst', etc.)
        'outtmpl': output_path,  # Output file path
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_audio_from_video(video_file, audio_file):
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)
    print(f"Audio extracted and saved as {audio_file}.")


# Step 1: Transcribe the audio file
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_file)
    
    with audio as source:
        audio_data = recognizer.record(source)
    
    try:
        print("Transcribing audio...")
        text = recognizer.recognize_google(audio_data)
        print("Transcription complete.")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with Google API: {e}")
        return None

# Step 2: Use OpenAI to classify accent
def classify_accent(text):
    prompt = f"Based on the following text, classify the speaker's accent: {text}. The options are British, American, Australian, Canadian, Irish, or other accents. Please provide also the accuracy of the classification in the form of accuracy=0.XX. You should always use equal sign(=) for the accuracy."
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{'role': 'user', 'content': prompt}]
    )
    accent = response.choices[0].message.content
    if 'British' in accent:
        single_accent = 'British'
    elif 'American' in accent:
        single_accent = 'American'
    elif 'Australian' in accent:
        single_accent = 'Australian'
    elif 'Canadian' in accent:
        single_accent = 'Canadian'
    elif 'Irish' in accent:
        single_accent = 'Irish'
    else:
        single_accent = 'Other'
    
    accuracy = accent.split('=')[-1].strip()[:4]
    #accent = accent.split('accuracy=')[0].strip()
    print(f"Classified Accent: {accent}")
    return accent, single_accent, accuracy

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_submission():
    # Check if the form contains a file
    if 'file' in request.files and request.files['file']:
        # Handle file upload
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print(f"File saved at: {file_path}")
        if file.filename.endswith('.wav'):
            # If it's a .wav file, just transcribe the audio
            transcription = transcribe_audio(file_path)
            
            if transcription:
                accent, single_accent, accuracy = classify_accent(transcription)
                return render_template('result.html', transcription=transcription, accent=accent, single_accent=single_accent, accuracy=accuracy)
            else:
                return jsonify({'error': 'Unable to transcribe the audio.'}), 400
        elif file.filename.endswith('.mp4'):
            # If it's a .mp4 file, extract audio and then transcribe
            audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.wav')
            extract_audio_from_video(file_path, audio_file)
            transcription = transcribe_audio(audio_file)
            
            if transcription:
                accent, single_accent, accuracy = classify_accent(transcription)
                return render_template('result.html', transcription=transcription, accent=accent, single_accent=single_accent, accuracy=accuracy)
            else:
                return jsonify({'error': 'Unable to transcribe the audio from the video.'}), 400
        else:
            return jsonify({'error': 'Only WAV or MP4 files are allowed'}), 400

    # Check if the form contains a URL
    elif 'url' in request.form and request.form['url']:
        # Handle YouTube URL
        url = request.form['url']
        print(f"Downloading video from URL: {url}")

        # Download video
        download_video(url, 'downloaded_video.mp4')
        
        # Extract audio from the video and save as WAV
        extract_audio_from_video('downloaded_video.mp4', 'downloaded_audio.wav')
        
        # Transcribe the audio from the video
        transcription = transcribe_audio('downloaded_audio.wav')
        
        if transcription:
            accent, single_accent, accuracy = classify_accent(transcription)
            return render_template('result.html', transcription=transcription, accent=accent, single_accent=single_accent, accuracy=accuracy)
        else:
            return jsonify({'error': 'Unable to transcribe the audio from the video.'}), 400
    else:
        return jsonify({'error': 'No file or URL provided'}), 400


# Step 4: Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
