from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html",
        books=[],
        query=""
    )

@app.route("/search")
def search():

    query = request.args.get("q", "").strip()

    if not query:
        return render_template(
            "index.html",
            books=[],
            query=""
        )

    try:

        response = requests.get(
            f"https://openlibrary.org/search.json?q={query}",
            timeout=10
        )

        data = response.json()

        books = []

        for item in data.get("docs", [])[:20]:

            title = item.get("title")
            authors = item.get("author_name")

            if not title or not authors:
                continue

            cover_id = item.get("cover_i")

            if cover_id:
                cover = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            else:
                cover = ""

            isbn_list = item.get("isbn", [])

            books.append({
                "title": title,
                "author": ", ".join(authors),
                "year": item.get("first_publish_year", "N/A"),
                "isbn": isbn_list[0] if isbn_list else "N/A",
                "cover": cover
            })

    except Exception:
        books = []

    return render_template(
        "index.html",
        books=books,
        query=query
    )

if __name__ == "__main__":
    app.run(debug=True)
