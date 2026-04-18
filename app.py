from flask import Flask, request, render_template, flash, redirect, url_for, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
from main import transcribe_audio, extract_action_items
import re
from deep_translator import GoogleTranslator
from gtts import gTTS
import uuid
import json
from models import db, Meeting
import subprocess
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meeting_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Database initialization error: {e}")

# Download spacy model if not present
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spacy model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
except Exception as e:
    print(f"Spacy model initialization warning: {e}")

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg', 'webm'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize models
SUMMARIZATION_AVAILABLE = False
summarizer = None

try:
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator()
    TRANSLATION_AVAILABLE = True
except ImportError:
    translator = None
    TRANSLATION_AVAILABLE = False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def translate_text(text, target_lang='es'):
    """Translate text to target language"""
    if not TRANSLATION_AVAILABLE:
        return f"Translation not available. Original text: {text}"
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return f"Translation failed: {text}"

def summarize_text(text):
    """Summarize the given text"""
    # Simple fallback summarization - take first few sentences
    sentences = text.split('.')
    summary_sentences = sentences[:3]  # Take first 3 sentences
    summary = '. '.join(summary_sentences)
    if len(summary) > 200:
        summary = summary[:200] + "..."
    return f"Simple summary: {summary}"

def format_as_dialogue(text):
    """Convert transcript to dialogue format"""
    try:
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        dialogue = []
        for i, sentence in enumerate(sentences):
            speaker = f"Speaker {1 if i % 2 == 0 else 2}"
            dialogue.append(f"{speaker}: {sentence.strip()}")
        return '\n\n'.join(dialogue)
    except Exception as e:
        print(f"Dialogue formatting error: {e}")
        return text

def generate_audio_from_text(text, lang='en'):
    """Generate audio file from text using gTTS"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = f"translated_audio_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tts.save(filepath)
        return filepath
    except Exception as e:
        print(f"TTS error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Get processing options
            translate = 'translate' in request.form
            target_lang = request.form.get('target_lang', 'es')
            summarize = 'summarize' in request.form
            dialogue = 'dialogue' in request.form
            generate_audio = 'generate_audio' in request.form

            try:
                # Process the audio file
                transcript = transcribe_audio(filepath)
                if not transcript:
                    flash('Failed to transcribe audio. Please check the file format.')
                    os.remove(filepath)  # Clean up
                    return redirect(request.url)

                actions = extract_action_items(transcript)

                # Apply additional processing
                translated_text = None
                summary = None
                dialogue_text = None
                audio_file_path = None

                if translate:
                    translated_text = translate_text(transcript, target_lang)
                    if generate_audio and translated_text:
                        # Map language codes to gTTS supported languages
                        lang_map = {
                            'es': 'es', 'fr': 'fr', 'de': 'de', 'it': 'it', 'pt': 'pt',
                            'ru': 'ru', 'ja': 'ja', 'ko': 'ko', 'zh-cn': 'zh-cn',
                            'ar': 'ar', 'hi': 'hi'
                        }
                        tts_lang = lang_map.get(target_lang, 'en')
                        audio_file_path = generate_audio_from_text(translated_text, tts_lang)
                        audio_file_name = os.path.basename(audio_file_path) if audio_file_path else None
                    else:
                        audio_file_name = None
                else:
                    audio_file_name = None
                
                if summarize:
                    summary = summarize_text(transcript)
                
                if dialogue:
                    dialogue_text = format_as_dialogue(transcript)

                # Clean up the uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)

                # Save analysis to database
                meeting = Meeting(
                    filename=filename,
                    transcript=transcript,
                    action_items=json.dumps(actions),
                    translated_text=translated_text,
                    summary=summary,
                    dialogue_text=dialogue_text,
                    audio_file_name=audio_file_name,
                    target_lang=target_lang if translate else None
                )
                db.session.add(meeting)
                db.session.commit()

                return render_template('result.html',
                                       transcript=transcript,
                                       actions=actions,
                                       translated_text=translated_text,
                                       summary=summary,
                                       dialogue_text=dialogue_text,
                                       audio_file_name=audio_file_name,
                                       target_lang=target_lang,
                                       meeting_id=meeting.id)
            except Exception as e:
                print(f"Processing error: {e}")
                import traceback
                traceback.print_exc()
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash(f'Error processing audio: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Supported formats: WAV, MP3, M4A, FLAC, OGG, WEBM')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/history')
def history():
    """Display past meeting analyses"""
    page = request.args.get('page', 1, type=int)
    meetings = Meeting.query.order_by(Meeting.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('history.html', meetings=meetings)

@app.route('/history/<int:meeting_id>')
def view_meeting(meeting_id):
    """View a past meeting analysis"""
    meeting = Meeting.query.get_or_404(meeting_id)
    return render_template('meeting_detail.html', meeting=meeting)

@app.route('/history/<int:meeting_id>/delete', methods=['POST'])
def delete_meeting(meeting_id):
    """Delete a meeting from history"""
    meeting = Meeting.query.get_or_404(meeting_id)
    
    # Delete associated audio file if it exists
    if meeting.audio_file_name:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], meeting.audio_file_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
    
    db.session.delete(meeting)
    db.session.commit()
    flash('Meeting deleted from history.')
    return redirect(url_for('history'))

@app.route('/download/<filename>')
def download_file(filename):
    """Serve audio files for download"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=f"translated_audio_{filename}")
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash('Error downloading file')
        return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)