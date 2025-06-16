from modules.prompt_parser import extract_keywords_and_emotions
from modules.freesound_search import search_and_download_sound
from modules.utils import load_config

def main():
    config = load_config("config/config.yaml")
    prompt = input("Enter a prompt: ")
    
    keywords, emotions = extract_keywords_and_emotions(prompt)
    primary_keyword = keywords[0] if keywords else "sound"

    print(f"[INFO] Searching Freesound for: {primary_keyword}")
    file_path = search_and_download_sound(primary_keyword, config)
    
    if file_path:
        print(f"[SUCCESS] Sound downloaded: {file_path}")
    else:
        print("[ERROR] No sound found.")

if __name__ == '__main__':
    main()
