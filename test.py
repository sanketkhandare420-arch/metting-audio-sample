import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import extract_action_items

# Sample meeting transcript
sample_transcript = """
Good morning everyone. Let's start the meeting. First, I want to discuss the project timeline. John, you mentioned that the development phase will be completed by next Friday. Is that still accurate?

Yes, that's correct. I will finish the coding by Friday and send the code for review.

Great. After that, we need to do testing. Sarah, can you handle the testing phase? You should start on Monday.

Sure, I will take care of the testing. I must ensure all features are working properly.

Also, regarding the documentation, we should update the user manual. Mike, you are responsible for that. Please have it done by end of next week.

Okay, I will work on the documentation.

Finally, let's schedule a follow-up meeting next Tuesday to review the progress.
"""

def test_extraction():
    print("Sample Transcript:")
    print(sample_transcript)
    print("\n" + "="*50 + "\n")

    actions = extract_action_items(sample_transcript)

    print("Extracted Action Items:")
    if actions:
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
    else:
        print("No action items detected.")

if __name__ == "__main__":
    test_extraction()