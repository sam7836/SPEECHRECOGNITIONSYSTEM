import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# List available microphones
mics = sr.Microphone.list_microphone_names()
print("Available Microphones:")
for index, name in enumerate(mics):
    print(f"{index}: {name}")

# Try different microphones to find a working one
for i, mic_name in enumerate(mics):
    try:
        with sr.Microphone(device_index=i) as source:
            print(f"🎙️ Testing microphone: {mic_name} (Index {i})")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for a short test... Speak now!")
            audio = recognizer.listen(source, timeout=3)
            test_text = recognizer.recognize_google(audio)
            print(f"✅ Microphone {mic_name} works! Using Index {i}")
            mic_index = i
            break  # Stop searching after finding a working mic
    except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
        print(f"❌ Microphone {mic_name} did not work. Trying next...")

# If no working mic found, exit
if 'mic_index' not in locals():
    print("⚠️ No working microphone found. Please check your settings.")
    exit()

# Start speech recognition
with sr.Microphone(device_index=mic_index) as source:
    print("Adjusting for ambient noise... Please wait")
    recognizer.adjust_for_ambient_noise(source)
    print("Listening... Speak now!")

    try:
        audio = recognizer.listen(source, timeout=5)
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio. Try again.")
    except sr.RequestError:
        print("⚠️ Could not request results. Check your internet connection.")
    except sr.WaitTimeoutError:
        print("⚠️ No speech detected. Try speaking louder.")
        
# speechrecognition (Simple & Quick)
# Uses various backends like Google Web Speech API, Sphinx, and Wit.ai.
# Works well for simple real-time applications but requires an internet connection for high accuracy (Google API).
# Best for: Quick prototypes, online speech-to-text, lightweight projects.