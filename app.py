from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

OPENLIB_URL = "https://openlibrary.org/search.json"


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# SEARCH BOOKS USING OPENLIBRARY API
# -------------------------
@app.route("/search")
def search():
    query = request.args.get("q", "")

    books = []

    try:
        response = requests.get(OPENLIB_URL, params={"q": query})
        data = response.json()

        # OpenLibrary stores books inside "docs"
        for item in data.get("docs", []):
            books.append({
                "title": item.get("title", "No Title"),
                "author": item.get("author_name", ["Unknown"])[0] if item.get("author_name") else "Unknown",
                "year": item.get("first_publish_year", "N/A")
            })

    except Exception as e:
        print("Error:", e)

    return render_template("results.html", books=books, query=query)


# -------------------------
# RUN APP (FOR DEPLOYMENT)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)