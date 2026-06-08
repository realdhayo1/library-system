from flask import Flask, render_template, request
import requests, random

app = Flask(__name__)

OPENLIB = "https://openlibrary.org/search.json"

def fetch_books(query, limit=8):
    try:
        r = requests.get(OPENLIB, params={"q": query}, timeout=10)
        docs = r.json().get("docs", [])[:limit]
        books = []
        for item in docs:
            isbn = item.get("isbn", [None])[0]
            books.append({
                "title": item.get("title", "No Title"),
                "author": item.get("author_name", ["Unknown"])[0] if item.get("author_name") else "Unknown",
                "year": item.get("first_publish_year", "N/A"),
                "isbn": isbn or "Not Available",
                "cover": f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg" if isbn else "https://via.placeholder.com/180x260?text=No+Cover",
                "availability": random.choice(["Available", "Checked Out"])
            })
        return books
    except:
        return []

@app.route("/")
def home():
    q = request.args.get("q", "")
    results = fetch_books(q, 20) if q else []
    featured = fetch_books("fiction", 4)
    recommended = fetch_books("bestseller", 6)
    return render_template("catalog.html",
                           results=results,
                           featured=featured,
                           recommended=recommended,
                           query=q)

if __name__ == "__main__":
    app.run(debug=True)
