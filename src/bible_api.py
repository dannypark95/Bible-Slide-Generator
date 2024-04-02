import requests

def esvBibleChapter(book, chapter, api_key):
    verse = 1
    result = []
    previous_passage_text = None

    while True:
        url = f"https://api.esv.org/v3/passage/text/?q={book}+{chapter}:{verse}&include-passage-references=false&include-verse-numbers=false&include-first-verse-numbers=false&include-footnotes=false&include-headings=false&include-short-copyright=false"

        # Define your API key in the headers for authorization
        headers = {"Authorization": f"Token {api_key}"
        }
    
        # Make the GET request with the URL and headers
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract the passage text
            passage_text = data.get("passages", [""])[0].replace('\n', '').strip()

            # Check if the passage text is the same as the previous verse's text
            if passage_text == previous_passage_text:
                # We've reached the end of the chapter
                break

            previous_passage_text = passage_text

            result.append(passage_text)
        else:
            print("Failed to retrieve the passage.")
            break

        verse+=1
        
    return result