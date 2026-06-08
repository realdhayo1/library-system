from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

OPENLIB_URL = "https://openlibrary.org/search.json"


@app.route("/")
def home():
    return render_template("index.html", books=None, query=None, total_results=0)


@app.route("/search")
def search():

    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))

    books = []
    total_results = 0

    try:
        response = requests.get(
            OPENLIB_URL,
            params={"q": query, "page": page},
            timeout=10
        )

        data = response.json()
        total_results = data.get("numFound", 0)

        for item in data.get("docs", [])[:20]:

            isbn_list = item.get("isbn", [])
            isbn = isbn_list[0] if isbn_list else None

            cover = (
                f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
                if isbn else None
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
                "cover": cover,
                "key": item.get("key", "")
            })

    except Exception as e:
        print("Error:", e)

    return render_template(
        "index.html",
        books=books,
        query=query,
        total_results=total_results,
        page=page
    )


@app.route("/book/<path:work_key>")
def book_details(work_key):

    try:
        url = f"https://openlibrary.org/{work_key}.json"
        res = requests.get(url)
        data = res.json()

        return f"""
        <h1>{data.get('title','No Title')}</h1>
        <p>{data.get('description','No description')}</p>
        <br>
        <a href='/'>Back</a>
        """

    except:
        return "Book not found"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
