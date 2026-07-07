import json
import os
import shutil
from datetime import datetime

# ==========================================
# PERSONAL BLOG MANAGEMENT SYSTEM
# ==========================================

DATABASE_FILE = "blog_database.json"
BACKUP_FILE = "blog_backup.json"
EXPORT_FOLDER = "exported_blogs"

# ==========================================
# INITIALIZE APPLICATION
# ==========================================

def initialize():

    if not os.path.exists(DATABASE_FILE):

        with open(DATABASE_FILE, "w", encoding="utf-8") as file:

            json.dump([], file, indent=4)

    if not os.path.exists(EXPORT_FOLDER):

        os.makedirs(EXPORT_FOLDER)


# ==========================================
# LOAD DATABASE
# ==========================================

def load_database():

    with open(DATABASE_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


# ==========================================
# SAVE DATABASE
# ==========================================

def save_database(database):

    with open(DATABASE_FILE, "w", encoding="utf-8") as file:

        json.dump(database, file, indent=4)


# ==========================================
# GENERATE BLOG ID
# ==========================================

def generate_blog_id(database):

    if len(database) == 0:

        return 1

    return max(post["id"] for post in database) + 1


# ==========================================
# WORD COUNT
# ==========================================

def word_count(content):

    return len(content.split())


# ==========================================
# READING TIME
# ==========================================

def reading_time(words):

    minutes = max(1, round(words / 200))

    return f"{minutes} Minute(s)"


# ==========================================
# CREATE BLOG
# ==========================================

def create_blog():

    database = load_database()

    print("\n" + "=" * 60)
    print("CREATE NEW BLOG")
    print("=" * 60)

    title = input("Title      : ").strip()

    author = input("Author     : ").strip()

    category = input("Category   : ").strip()

    tags = input("Tags (comma separated) : ").strip()

    print("\nEnter Blog Content")
    print("Press ENTER twice to finish.\n")

    lines = []

    while True:

        line = input()

        if line == "":

            break

        lines.append(line)

    content = "\n".join(lines)

    if title == "" or author == "" or content == "":

        print("\nRequired fields cannot be empty.")

        return

    total_words = word_count(content)

    blog = {

        "id": generate_blog_id(database),

        "title": title,

        "author": author,

        "category": category,

        "tags": [

            tag.strip()

            for tag in tags.split(",")

            if tag.strip()

        ],

        "content": content,

        "word_count": total_words,

        "reading_time": reading_time(total_words),

        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

        "updated_at": "Never"

    }

    database.append(blog)

    save_database(database)

    print("\nBlog Published Successfully!")

    print(f"Blog ID : {blog['id']}")


# ==========================================
# VIEW BLOG LIST
# ==========================================

def view_blog_list():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    print("\n" + "=" * 70)
    print("BLOG LIST")
    print("=" * 70)

    for blog in database:

        print(f"ID           : {blog['id']}")
        print(f"Title        : {blog['title']}")
        print(f"Author       : {blog['author']}")
        print(f"Category     : {blog['category']}")
        print(f"Words        : {blog['word_count']}")
        print(f"Reading Time : {blog['reading_time']}")
        print("-" * 70)
# ==========================================
# VIEW COMPLETE BLOG
# ==========================================

def view_blog():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    try:

        blog_id = int(input("\nEnter Blog ID : "))

    except ValueError:

        print("Invalid Blog ID.")

        return

    for blog in database:

        if blog["id"] == blog_id:

            print("\n" + "=" * 80)
            print("BLOG DETAILS")
            print("=" * 80)

            print(f"ID            : {blog['id']}")
            print(f"Title         : {blog['title']}")
            print(f"Author        : {blog['author']}")
            print(f"Category      : {blog['category']}")
            print(f"Tags          : {', '.join(blog['tags'])}")
            print(f"Word Count    : {blog['word_count']}")
            print(f"Reading Time  : {blog['reading_time']}")
            print(f"Created At    : {blog['created_at']}")
            print(f"Updated At    : {blog['updated_at']}")

            print("\nCONTENT")
            print("-" * 80)
            print(blog["content"])
            print("=" * 80)

            return

    print("\nBlog Not Found.")


# ==========================================
# SEARCH BY TITLE
# ==========================================

def search_title():

    database = load_database()

    keyword = input("\nEnter Title Keyword : ").lower().strip()

    found = False

    for blog in database:

        if keyword in blog["title"].lower():

            found = True

            print("\n----------------------------")
            print(f"ID       : {blog['id']}")
            print(f"Title    : {blog['title']}")
            print(f"Author   : {blog['author']}")
            print(f"Category : {blog['category']}")

    if not found:

        print("\nNo Matching Blogs Found.")


# ==========================================
# SEARCH BY AUTHOR
# ==========================================

def search_author():

    database = load_database()

    keyword = input("\nEnter Author Name : ").lower().strip()

    found = False

    for blog in database:

        if keyword in blog["author"].lower():

            found = True

            print("\n----------------------------")
            print(f"ID       : {blog['id']}")
            print(f"Title    : {blog['title']}")
            print(f"Category : {blog['category']}")
            print(f"Created  : {blog['created_at']}")

    if not found:

        print("\nNo Blogs Found.")


# ==========================================
# SEARCH BY CATEGORY
# ==========================================

def search_category():

    database = load_database()

    keyword = input("\nEnter Category : ").lower().strip()

    found = False

    for blog in database:

        if keyword in blog["category"].lower():

            found = True

            print("\n----------------------------")
            print(f"ID       : {blog['id']}")
            print(f"Title    : {blog['title']}")
            print(f"Author   : {blog['author']}")

    if not found:

        print("\nNo Blogs Found.")


# ==========================================
# SEARCH BY TAG
# ==========================================

def search_tag():

    database = load_database()

    keyword = input("\nEnter Tag : ").lower().strip()

    found = False

    for blog in database:

        tags = [tag.lower() for tag in blog["tags"]]

        if keyword in tags:

            found = True

            print("\n----------------------------")
            print(f"ID       : {blog['id']}")
            print(f"Title    : {blog['title']}")
            print(f"Author   : {blog['author']}")
            print(f"Tags     : {', '.join(blog['tags'])}")

    if not found:

        print("\nNo Blogs Found.")
# ==========================================
# EDIT BLOG
# ==========================================

def edit_blog():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    try:

        blog_id = int(input("\nEnter Blog ID to Edit : "))

    except ValueError:

        print("Invalid Blog ID.")

        return

    for blog in database:

        if blog["id"] == blog_id:

            print("\nLeave blank to keep existing value.\n")

            title = input(f"Title [{blog['title']}] : ").strip()

            author = input(f"Author [{blog['author']}] : ").strip()

            category = input(f"Category [{blog['category']}] : ").strip()

            tags = input(
                f"Tags [{', '.join(blog['tags'])}] : "
            ).strip()

            print("\nEnter New Content")

            print("Press ENTER twice to keep existing content.\n")

            lines = []

            while True:

                line = input()

                if line == "":

                    break

                lines.append(line)

            if title != "":

                blog["title"] = title

            if author != "":

                blog["author"] = author

            if category != "":

                blog["category"] = category

            if tags != "":

                blog["tags"] = [

                    tag.strip()

                    for tag in tags.split(",")

                    if tag.strip()

                ]

            if len(lines) > 0:

                blog["content"] = "\n".join(lines)

                blog["word_count"] = word_count(

                    blog["content"]

                )

                blog["reading_time"] = reading_time(

                    blog["word_count"]

                )

            blog["updated_at"] = datetime.now().strftime(

                "%d-%m-%Y %H:%M:%S"

            )

            save_database(database)

            print("\nBlog Updated Successfully.")

            return

    print("\nBlog Not Found.")


# ==========================================
# DELETE BLOG
# ==========================================

def delete_blog():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    try:

        blog_id = int(input("\nEnter Blog ID to Delete : "))

    except ValueError:

        print("Invalid Blog ID.")

        return

    for blog in database:

        if blog["id"] == blog_id:

            choice = input(

                f"Delete '{blog['title']}' ? (Y/N): "

            ).upper()

            if choice == "Y":

                database.remove(blog)

                save_database(database)

                print("\nBlog Deleted Successfully.")

            else:

                print("\nDeletion Cancelled.")

            return

    print("\nBlog Not Found.")


# ==========================================
# SORT BLOGS BY TITLE
# ==========================================

def sort_by_title():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    database.sort(

        key=lambda blog: blog["title"].lower()

    )

    print("\n========== BLOGS (A-Z) ==========\n")

    for blog in database:

        print(

            f"{blog['id']} - {blog['title']}"

        )


# ==========================================
# RECENT BLOGS
# ==========================================

def recent_blogs():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    recent = sorted(

        database,

        key=lambda blog: blog["created_at"],

        reverse=True

    )

    print("\n========== RECENT BLOGS ==========\n")

    for blog in recent[:5]:

        print(

            f"{blog['id']} - {blog['title']}"

        )

        print(

            f"Created : {blog['created_at']}"

        )

        print("-" * 40)


# ==========================================
# LONGEST BLOG
# ==========================================

def longest_blog():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    blog = max(

        database,

        key=lambda post: post["word_count"]

    )

    print("\n========== LONGEST BLOG ==========\n")

    print(f"Title : {blog['title']}")

    print(f"Words : {blog['word_count']}")

    print(f"Author: {blog['author']}")
# ==========================================
# SHORTEST BLOG
# ==========================================

def shortest_blog():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    blog = min(

        database,

        key=lambda post: post["word_count"]

    )

    print("\n========== SHORTEST BLOG ==========\n")

    print(f"Title : {blog['title']}")

    print(f"Words : {blog['word_count']}")

    print(f"Author: {blog['author']}")


# ==========================================
# BLOG STATISTICS
# ==========================================

def blog_statistics():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    total_posts = len(database)

    total_words = sum(

        blog["word_count"]

        for blog in database

    )

    average_words = round(

        total_words / total_posts,

        2

    )

    authors = set()

    categories = set()

    tags = set()

    for blog in database:

        authors.add(

            blog["author"]

        )

        categories.add(

            blog["category"]

        )

        for tag in blog["tags"]:

            tags.add(tag)

    print("\n" + "=" * 70)

    print("BLOG STATISTICS")

    print("=" * 70)

    print(f"Total Blogs       : {total_posts}")

    print(f"Total Authors     : {len(authors)}")

    print(f"Total Categories  : {len(categories)}")

    print(f"Total Tags        : {len(tags)}")

    print(f"Total Words       : {total_words}")

    print(f"Average Words     : {average_words}")

    print("=" * 70)


# ==========================================
# EXPORT BLOG TO HTML
# ==========================================

def export_html():

    database = load_database()

    if len(database) == 0:

        print("\nNo Blogs Available.")

        return

    try:

        blog_id = int(

            input("\nEnter Blog ID : ")

        )

    except ValueError:

        print("Invalid Blog ID.")

        return

    for blog in database:

        if blog["id"] == blog_id:

            filename = os.path.join(

                EXPORT_FOLDER,

                f"blog_{blog_id}.html"

            )

            html = f"""

<html>

<head>

<title>{blog['title']}</title>

</head>

<body>

<h1>{blog['title']}</h1>

<h3>Author : {blog['author']}</h3>

<h4>Category : {blog['category']}</h4>

<p><b>Tags:</b> {', '.join(blog['tags'])}</p>

<hr>

<pre>

{blog['content']}

</pre>

</body>

</html>

"""

            with open(

                filename,

                "w",

                encoding="utf-8"

            ) as file:

                file.write(html)

            print(

                "\nBlog Exported Successfully."

            )

            print(

                f"Location : {filename}"

            )

            return

    print("\nBlog Not Found.")


# ==========================================
# BACKUP DATABASE
# ==========================================

def backup_database():

    shutil.copy(

        DATABASE_FILE,

        BACKUP_FILE

    )

    print(

        "\nDatabase Backup Created."

    )


# ==========================================
# RESTORE DATABASE
# ==========================================

def restore_database():

    if not os.path.exists(

        BACKUP_FILE

    ):

        print(

            "\nBackup File Not Found."

        )

        return

    shutil.copy(

        BACKUP_FILE,

        DATABASE_FILE

    )

    print(

        "\nDatabase Restored Successfully."

    )
# ==========================================
# APPLICATION DASHBOARD
# ==========================================

def dashboard():

    database = load_database()

    print("\n" + "=" * 75)
    print("        PERSONAL BLOG MANAGEMENT SYSTEM")
    print("=" * 75)

    print(f"Total Blogs : {len(database)}")

    if len(database) > 0:

        latest = max(
            database,
            key=lambda blog: blog["id"]
        )

        print(f"Latest Blog : {latest['title']}")
        print(f"Latest Author : {latest['author']}")

    print("=" * 75)


# ==========================================
# MAIN MENU
# ==========================================

def menu():

    while True:

        dashboard()

        print("\n1. Create Blog")
        print("2. View Blog List")
        print("3. View Complete Blog")
        print("4. Search by Title")
        print("5. Search by Author")
        print("6. Search by Category")
        print("7. Search by Tag")
        print("8. Edit Blog")
        print("9. Delete Blog")
        print("10. Sort Blogs")
        print("11. Recent Blogs")
        print("12. Longest Blog")
        print("13. Shortest Blog")
        print("14. Blog Statistics")
        print("15. Export Blog to HTML")
        print("16. Backup Database")
        print("17. Restore Database")
        print("18. Exit")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":

            create_blog()

        elif choice == "2":

            view_blog_list()

        elif choice == "3":

            view_blog()

        elif choice == "4":

            search_title()

        elif choice == "5":

            search_author()

        elif choice == "6":

            search_category()

        elif choice == "7":

            search_tag()

        elif choice == "8":

            edit_blog()

        elif choice == "9":

            delete_blog()

        elif choice == "10":

            sort_by_title()

        elif choice == "11":

            recent_blogs()

        elif choice == "12":

            longest_blog()

        elif choice == "13":

            shortest_blog()

        elif choice == "14":

            blog_statistics()

        elif choice == "15":

            export_html()

        elif choice == "16":

            backup_database()

        elif choice == "17":

            restore_database()

        elif choice == "18":

            print("\nThank you for using Personal Blog Management System.")

            break

        else:

            print("\nInvalid Choice. Please Try Again.")

        input("\nPress Enter to Continue...")


# ==========================================
# PROGRAM ENTRY
# ==========================================

def main():

    initialize()

    menu()


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n\nApplication Closed by User.")

    except FileNotFoundError as error:

        print("\nFile Error :", error)

    except PermissionError as error:

        print("\nPermission Error :", error)

    except json.JSONDecodeError:

        print("\nDatabase File is Corrupted.")

    except Exception as error:

        print("\nUnexpected Error :", error)
