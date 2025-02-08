import requests

def get_book_data(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    response = requests.get(url)
    data = response.json()

    if data["numFound"] > 0:
        book = data["docs"][0]
        return {
            "title": book.get("title", "Unknown"),
            "author": book.get("author_name", ["Unknown"])[0],
            "description": book.get("first_sentence", ["No description available"])[0],
            "cover": f"https://covers.openlibrary.org/b/id/{book.get('cover_i', '')}-L.jpg",
        }
    return None