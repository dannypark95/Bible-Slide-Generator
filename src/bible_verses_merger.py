import pandas as pd
import requests
from tqdm import tqdm
import time
import re

def esvBibleChapter(book, chapter, api_key):
    """
    Fetches a chapter from the ESV Bible API, handling rate limits with a countdown, and ensures no verses are skipped.
    """
    verse = 1
    verses_data = []
    previous_passage_text = None

    with tqdm(desc=f"Fetching verses for {book} {chapter}", unit="verse") as pbar:
        while True:
            # ESV API request setup
            url = f"https://api.esv.org/v3/passage/text/?q={book}+{chapter}:{verse}" \
                  f"&include-passage-references=false" \
                  f"&include-verse-numbers=false" \
                  f"&include-first-verse-numbers=false" \
                  f"&include-footnotes=false" \
                  f"&include-headings=false" \
                  f"&include-short-copyright=false"

            headers = {"Authorization": f"Token {api_key}"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                passage_text = data.get("passages", [""])[0].replace('\n', '').strip()

                if passage_text == previous_passage_text or passage_text == "":
                    pbar.set_postfix_str("Completed chapter.")
                    break

                previous_passage_text = passage_text
                verses_data.append({'book_name_eng': book, 'chapter': chapter, 'verse': verse, 'text_eng': passage_text})
                pbar.update(1)
                verse += 1  # Increment verse only on successful fetch
            elif response.status_code == 429:  # Throttling response
                detail_message = response.json().get('detail', '')
                retry_after_match = re.search(r'\b\d+\b', detail_message)
                if retry_after_match:
                    retry_after = int(retry_after_match.group()) + 1  # Add one extra second
                else:
                    retry_after = 31  # Default to a reasonable retry time if not found
                for remaining in range(retry_after, 0, -1):
                    pbar.set_postfix_str(f"Rate limited. Retrying in {remaining} seconds...")
                    time.sleep(1)
                pbar.set_postfix_str('')
            else:
                print("Retrying due to failure...")
                time.sleep(2)  # Wait for 2 seconds before retrying without incrementing the verse

    return pd.DataFrame(verses_data)

def fetch_and_merge_bible_verses(book_eng, chapter, api_key):
    """
    Fetches ESV Bible verses and merges them with Korean Bible verses.
    """
    # Load data
    bible_books_df = pd.read_csv('../data/bible_books.csv')
    woorimal_df = pd.read_csv('../data/woorimal_bible.csv')

    # Merge to include English book names in woorimal_df
    woorimal_df = pd.merge(woorimal_df, bible_books_df[['book_name_kor', 'book_name_eng']], on='book_name_kor', how='left')

    # Fetch English Bible verses
    esv_df = esvBibleChapter(book_eng, chapter, api_key)

    # Prepare for merging
    woorimal_df['chapter'] = woorimal_df['chapter'].astype(int)
    woorimal_df['verse'] = woorimal_df['verse'].astype(int)
    esv_df['chapter'] = esv_df['chapter'].astype(int)
    esv_df['verse'] = esv_df['verse'].astype(int)

    # Merge
    merged_df = pd.merge(woorimal_df, esv_df, on=['book_name_eng', 'chapter', 'verse'], how='inner')

    # Final DataFrame preparation
    final_df = merged_df[['book_name_kor', 'book_name_eng', 'chapter', 'verse', 'text_kor', 'text_eng']]

    return final_df