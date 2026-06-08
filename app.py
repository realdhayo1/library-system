from datetime import datetime

CURRENT_YEAR = datetime.now().year


@app.route("/books")
def books():
    return category_search("book")


@app.route("/journals")
def journals():
    return category_search("journal")


@app.route("/research")
def research():
    return category_search("research")


@app.route("/magazines")
def magazines():
    return category_search("magazine")


@app.route("/new-arrivals")
def new_arrivals():

    books = []

    try:
        response = requests.get(
            OPENLIB_URL,
            params={
                "q": "subject:fiction",
                "limit": 50
            }
        )

        data = response.json()

        for item in data.get("docs", []):

            year = item.get("first_publish_year")

            if (
                year and
                CURRENT_YEAR - year <= 5
            ):

                isbn_list = item.get("isbn", [])
                isbn = isbn_list[0] if isbn_list else None

                cover_url = None

                if isbn:
                    cover_url = (
                        f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
                    )

                books.append({
                    "title": item.get("title", "No Title"),
                    "author": (
                        item.get("author_name", ["Unknown"])[0]
                        if item.get("author_name")
                        else "Unknown"
                    ),
                    "year": year,
                    "isbn": isbn if isbn else "Not Available",
                    "cover": cover_url,
                    "key": item.get("key", ""),
                    "availability": random.choice(
                        ["Available", "Checked Out"]
                    )
                })

    except Exception as e:
        print(e)

    return render_template(
        "results.html",
        books=books,
        query="New Arrivals",
        total_results=len(books),
        page=1
    )


def category_search(category):

    books = []

    try:
        response = requests.get(
            OPENLIB_URL,
            params={
                "q": category,
                "page": 1
            }
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

            books.append({
                "title": item.get("title", "No Title"),
                "author": (
                    item.get("author_name", ["Unknown"])[0]
                    if item.get("author_name")
                    else "Unknown"
                ),
                "year": item.get(
                    "first_publish_year",
                    "N/A"
                ),
                "isbn": isbn if isbn else "Not Available",
                "cover": cover_url,
                "key": item.get("key", ""),
                "availability": random.choice(
                    ["Available", "Checked Out"]
                )
            })

        return render_template(
            "results.html",
            books=books,
            query=category.title(),
            total_results=len(books),
            page=1
        )

    except Exception as e:
        print(e)

        return render_template(
            "results.html",
            books=[],
            query=category.title(),
            total_results=0,
            page=1
        )
