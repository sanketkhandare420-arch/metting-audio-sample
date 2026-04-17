# Audio Action-Item Extractor

With the rise of remote work and virtual collaboration, meetings have become a core part of professional communication. However, extracting meaningful outcomes—especially action items—from long discussions remains a challenge.

This project falls under the domain of Artificial Intelligence and Natural Language Processing (NLP). The proposed system is an Audio Action-Item Extractor that converts meeting audio into text and intelligently identifies actionable tasks, decisions, and responsibilities. Instead of manually reviewing recordings, the system uses speech-to-text and NLP techniques to automate the extraction of key points.

This invention-based solution improves productivity by reducing manual effort and ensuring that important tasks are not overlooked.

## Features

- **Professional Web Interface**: Modern, responsive design with Bootstrap styling
- **File Upload**: Drag-and-drop audio file upload with format validation
- **Real-time Processing**: Automatic transcription and action item extraction
- **Translation**: Translate transcripts to multiple languages (Spanish, French, German, etc.)
- **Text-to-Speech Audio Generation**: Generate downloadable audio files from translated text
- **Summarization**: Generate concise summaries of meeting content
- **Dialogue Format**: Convert transcripts into structured dialogue format
- **Results Display**: Clean presentation of transcript, translation, summary, dialogue, and action items
- **Audio Download**: Download translated content as MP3 audio files
- **Error Handling**: User-friendly error messages for invalid files or processing failures
- **Audio Format Support**: WAV, MP3, M4A, FLAC, OGG (FFmpeg required for non-WAV)
- **AI-Powered**: Uses OpenAI Whisper for speech-to-text, spaCy for NLP, and transformers for summarization

## Installation

1. Clone or download this repository.
2. Install dependencies: `pip install -r requirements.txt`

## Usage

### Web Application (Recommended)
Run the web application for a professional user interface:

```bash
python app.py
```

Then open your browser and go to `http://localhost:5000`

Upload an audio file and select from the following processing options:
- ✅ **Translate**: Convert transcript to another language
- ✅ **Generate translated audio**: Create downloadable MP3 from translated text
- ✅ **Generate summary**: Get concise meeting overview
- ✅ **Format as dialogue**: Convert to conversational format

The results page will display all processed outputs with download links for generated audio files.

### Command Line
Run the main script with an audio file:

```bash
python main.py path/to/audio/file.wav
```

The script will output the transcribed text and extracted action items.

## Dependencies

- openai-whisper: For speech-to-text
- transformers: For NLP tasks
- torch: Backend for models
- Other utilities</content>
<parameter name="filePath">c:\Users\USER\Desktop\metting audio sample\README.md