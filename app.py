from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", books=[])

@app.route("/search")
def search():

    query = request.args.get("q")

    if not query:
        return render_template("index.html", books=[])

    url = f"https://openlibrary.org/search.json?q={query}"

    response = requests.get(url)

    data = response.json()

    books = []

    for book in data.get("docs", [])[:20]:

        cover_id = book.get("cover_i")

        if cover_id:
            cover = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        else:
            cover = "https://via.placeholder.com/180x260?text=No+Cover"

        books.append({
            "title": book.get("title", "Unknown Title"),
            "author": ", ".join(book.get("author_name", ["Unknown Author"])),
            "year": book.get("first_publish_year", "N/A"),
            "isbn": book.get("isbn", ["N/A"])[0],
            "cover": cover
        })

    return render_template(
        "index.html",
        books=books,
        search_query=query
    )

if __name__ == "__main__":
    app.run(debug=True)
