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
   ```
   
2. Go to folder:

 Navigate to the rpoject folder
  ```bash
   cd accent_detector
  ```
3. Create virtual environment:

Use this commmand to create a virtual enviornment
  ```bash
  python -m venv <virtualenv_name>
  ```

4. Activate virtual env:

On windows use the following command
  ```bash
  <virtualenv_name>\Scripts\activate
  ```

On macOS/Linux use the following command
  ```bash
source <virtualenv_name>/bin/activate
  ```

If working on Windows but you use MINGW64 terminal use:
  ```bash
source <virtual_name>/Scripts/activate
  ```

5. Install requirements:
   
First navigate to the src folder
  ```bash
   cd src
  ```
Then install the required dependencies by running
  ```bash
   pip install -r requirements.txt
  ```

6. Openai API Key
   
 In the .env file change the openai_api_key with your private key
  ```bash
  OPENAI_API_KEY='private_key'
  ```

7. Run app:
8. 
  ```bash
   python app.py
  ```

The application will run at http://127.0.0.1:5000/ by default.
   
