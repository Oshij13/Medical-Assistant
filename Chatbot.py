import speech_recognition as sr
import random
import json

def read_dataset(file_path):
    dataset = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            intents = data["intents"]
            for intent in intents:
                tag = intent["tag"]
                patterns = intent["patterns"]
                responses = intent["responses"]
                for pattern in patterns:
                    dataset[pattern] = responses
    except FileNotFoundError:
        print("Error: Dataset file not found.")
    except Exception as e:
        print(f"Error while reading dataset: {e}")
    return dataset


def type_input():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "back":
            return None
        else:
            return user_input

def speech_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("You: Speak something...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio).lower()
        print(f"Recognized Speech: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
    except sr.RequestError:
        print("There was an issue with the speech recognition. Please try again.")
    return ""

def chat_bot_response(user_input, dataset):
    user_input = user_input.lower()
    responses = dataset.get(user_input, ["I'm sorry, I don't understand."])
    return random.choice(responses)


def main():
    file_path = r"C:\Users\oshij\OneDrive\Pictures\Desktop\intents (1).json"
    dataset = read_dataset(file_path)

    print("ChatBot: Hello! I'm here to chat with you.")

    chosen_input_method = None

    while True:
        if chosen_input_method is None:
            print("\nSelect input mode:")
            print("1. Type")
            print("2. Speak")
            print("3. Exit")

            choice = input("Enter your choice (1/2/3): ")

            if choice == "1":
                chosen_input_method = type_input
            elif choice == "2":
                chosen_input_method = speech_input
            elif choice == "3":
                print("ChatBot: Goodbye!")
                break
            else:
                print("Invalid choice. Please select again.")
                continue

        user_input = chosen_input_method()

        if user_input is None:
            chosen_input_method = None
            continue

        if user_input == "exit":
            print("ChatBot: Goodbye!")
            break

        response = chat_bot_response(user_input, dataset)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    main()
