import os
import requests
from modules.utils import save_audio_from_url

def search_and_download_sound(query, config):
    api_key = os.getenv("FREESOUND_API_KEY")
    if not api_key:
        raise Exception("Missing FREESOUND_API_KEY")

    search_url = f"https://freesound.org/apiv2/search/text/"
    params = {
        "query": query,
        "token": api_key,
        "fields": "id,name,previews",  # Request specific fields
        "filter": "duration:[0 TO 10]"  # Filter for shorter sounds
    }
    
    try:
        res = requests.get(search_url, params=params)
        res.raise_for_status()  # Raise an exception for bad status codes
        
        data = res.json()
        results = data.get("results", [])
        
        if not results:
            print(f"[INFO] No results found for query: {query}")
            return None

        # Get the first result with a preview URL
        for result in results:
            previews = result.get("previews", {})
            if previews and "preview-hq-mp3" in previews:
                sound_url = previews["preview-hq-mp3"]
                file_name = f"audio/outputs/{query.replace(' ', '_')}.mp3"
                save_audio_from_url(sound_url, file_name)
                return file_name

        print(f"[INFO] No preview available for query: {query}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Freesound API request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return None
