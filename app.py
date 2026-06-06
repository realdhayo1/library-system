from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

OPENLIB_URL = "https://openlibrary.org/search.json"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")

    books = []

    try:
        response = requests.get(
            OPENLIB_URL,
            params={"q": query},
            timeout=10
        )

        data = response.json()

        for item in data.get("docs", [])[:20]:

            isbn_list = item.get("isbn", [])
            isbn = isbn_list[0] if isbn_list else None

            cover_url = None
            if isbn:
                cover_url = (
                    f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
                )

            work_key = item.get("key", "")
            book_url = (
                f"https://openlibrary.org{work_key}"
                if work_key
                else "#"
            )

            books.append({
                "title": item.get("title", "No Title"),
                "author": (
                    item.get("author_name", ["Unknown"])[0]
                    if item.get("author_name")
                    else "Unknown"
                ),
                "year": item.get("first_publish_year", "N/A"),
                "isbn": isbn if isbn else "Not Available",
                "cover": cover_url,
                "url": book_url
            })

    except Exception as e:
        print("Error:", e)

    return render_template(
        "results.html",
        books=books,
        query=query
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
