'''
Author: Zachary Tolen
Spring Semester 2024
OpenAI and GoogleAI Integration
'''

import os
import sys
import datetime
import pygame
import pyaudio
import openai
from google.cloud import texttospeech
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize Google Text-to-Speech client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/zacht/OneDrive/Documents/Desktop/SoftwareEngineering/midyear-machine-420112-0d06b60d7b54.json"
tts_client = texttospeech.TextToSpeechClient()
speech_client = speech.SpeechClient()

# Set up OpenAI API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not set in environment variables.")

def listen_and_transcribe():
    # Audio recording parameters
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()

    # Start the audio stream
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Listening... Speak now!")

    # Listen for 5 seconds
    frames = []
    for _ in range(0, int(RATE / CHUNK * 5)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished listening.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # The response from Google Speech Recognition
    audio_content = b''.join(frames)
    audio = RecognitionAudio(content=audio_content)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US'
)

    response = speech_client.recognize(config=config, audio=audio)

    # Print the recognized text
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript

    return ""

def text_to_speech(text, base_filename="output.mp3"):
    # Generate a timestamped filename to avoid overwriting and conflicts
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{base_filename}"
    full_path = os.path.join(os.environ['USERPROFILE'], filename)

    tts_client = texttospeech.TextToSpeechClient()

    # Set up the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Specify the voice selection parameters using the exact voice name
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-B"  # This specifies the exact voice to be used
    )

    # Configure the audio settings
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # Set the audio format, e.g., MP3
    )

    # Perform the Text-to-Speech request
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save the audio to a file using the full path
    with open(full_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Response spoken and saved to '{full_path}'.")

    # Load and play the saved audio file
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def construct_prompt(message_log):
    # Constructing a more structured prompt
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in message_log]) + "\n"


def send_message(message_log, model="gpt-4-turbo", max_tokens=400, temperature=0.8):
    # Format the message_log into a single string prompt
    prompt_text = construct_prompt(message_log)
    print("Prompt sent to API:", prompt_text)
    try:
        response = openai.chat.completions.create(
            model = model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            messages= message_log
        )
        print("API Response:", response)  # Debug: print the full API response
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I encountered an error while processing your request."


def main(model, max_tokens, temperature):
    message_log = [
        {"role": "system", "content": "You are Willie the Wolverine, the mascot for Utah Valley University. Your job is to talk to student, ask them about their major or field of study, their year in school, and their experience levels, and then suggest interesting projects they can be involed in or work on as a student that fit their area of expertise."},
        {"role": "assistant", "content": "Hey, Wolverine!"}
    ]

    # Speak initial greeting
    text_to_speech(message_log[1]["content"])

    while True:
        user_input = listen_and_transcribe()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # Add user input to the message log
        message_log.append({"role": "user", "content": user_input})
        print("Current conversation history:", message_log)

        # Get response from OpenAI and add it to the message log
        response_text = send_message(message_log, model, max_tokens, temperature)
        message_log.append({"role": "assistant", "content": response_text})

        print(f"AI assistant: {response_text}")
        text_to_speech(response_text)

if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "gpt-4-turbo"
    max_tokens = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    temperature = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
    main(model, max_tokens, temperature)
