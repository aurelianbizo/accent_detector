# Audio Transcription and Accent Classification Web App

This is a web application built with Flask that allows users to upload `.wav` or `.mp4` files, or provide a YouTube URL. The app extracts audio from the video, transcribes the speech, and classifies the speaker's accent based on the transcription. It leverages the OpenAI API for accent classification and Google's Speech Recognition API for transcription.

## Features
- **File Upload**: Users can upload `.wav` audio files.
- **MP4 File Support**: Users can upload `.mp4` video files, from which audio will be extracted and transcribed.
- **YouTube URL Support**: Users can input a YouTube URL, and the app will download the video, extract the audio, and transcribe it.
- **Accent Classification**: The transcription is analyzed for accent classification using OpenAI's GPT-4 model. The available accents include:
  - British
  - American
  - Australian
  - Canadian
  - Irish
  - Other

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/accent_detector.git
   
2. Go to folder:

  ```bash
   cd accent_detector

3. Create virtual environment:

  ```bash
  python -m venv <virtualenv_name>

4. Activate virtual env:

 - windows:
  ```bash
  <virtualenv_name>\Scripts\activate
  ```bash
 - macOS/linux:
source <virtualenv_name>/bin/activate

5. Install requirements:
  ```bash
   cd src
   pip install -r requirements.txt

6. Run app:
  ```bash
   python app.py
   
