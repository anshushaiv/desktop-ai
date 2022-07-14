import assistant as a

def main():
    assistant = a.Assistant()
    assistant.load_voice_properties()
    assistant.load_misc_properties()
    assistant.assist()
    assistant.save_voice_properties()
    assistant.save_misc_properties()

if __name__ == "__main__":
    main()