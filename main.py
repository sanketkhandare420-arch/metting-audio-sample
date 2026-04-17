import sys
import whisper
import re

def transcribe_audio(file_path):
    """
    Transcribes audio file to text using OpenAI Whisper.
    """
    try:
        model = whisper.load_model("base")  # You can change to "small", "medium", "large" for better accuracy
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

def extract_action_items(text):
    """
    Extracts potential action items from the transcript using NLP when available.
    Falls back to keyword-based sentence scanning if spaCy is unavailable.
    """
    keywords = [
        "will", "need to", "should", "must", "action item", "task",
        "responsible for", "assign", "deadline", "follow up", "follow-up"
    ]

    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            spacy.cli.download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        action_items = []
        for sent in doc.sents:
            sent_text = sent.text.lower()
            if any(keyword in sent_text for keyword in keywords):
                action_items.append(sent.text.strip())
        return action_items
    except Exception as e:
        print(f"spaCy unavailable or failed, using keyword fallback: {e}")

    # Fallback to simple sentence splitting and keyword matching
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    action_items = [sentence.strip() for sentence in sentences if any(keyword in sentence.lower() for keyword in keywords)]
    return action_items

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <audio_file>")
        print("Supported formats: WAV, MP3, M4A, etc. (requires ffmpeg for non-WAV)")
        sys.exit(1)

    audio_file = sys.argv[1]

    print("Transcribing audio...")
    transcript = transcribe_audio(audio_file)

    if not transcript:
        print("Failed to transcribe audio.")
        sys.exit(1)

    print("Transcript:")
    print(transcript)
    print("\n" + "="*50 + "\n")

    print("Extracting action items...")
    actions = extract_action_items(transcript)

    print("Extracted Action Items:")
    if actions:
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
    else:
        print("No action items detected.")

if __name__ == "__main__":
    main()