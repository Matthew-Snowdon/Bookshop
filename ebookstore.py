import sqlite3
from tabulate import tabulate

# Create a connection to the ebookstore database
conn = sqlite3.connect('ebookstore.db')

# Create a books table if it doesn't exist
conn.execute('''CREATE TABLE IF NOT EXISTS books
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              Title TEXT NOT NULL,
              Author TEXT NOT NULL,
              Qty INTEGER NOT NULL)''')

# Insert some sample data into the books table
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('A Tale of Two Cities', 'Charles Dickens', 30)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('The Lord of the Rings', 'J.R.R Tolkien', 37)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('Alice in Wonderland', 'Lewis Carroll', 12)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('Adventures of Sherlock Holmes', 'Sir Arthur Conan Doyle', 5)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('To Kill a Mockingbird', 'Harper Lee', 54)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('1984', 'George Orwell', 22)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('Pride and Prejudice', 'Jane Austen', 22)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('The Bell Jar', 'Sylvia Plath', 47)")
conn.execute("INSERT INTO books (Title, Author, Qty) VALUES "
             "('Wuthering Heights', 'Emily Brontë', 27)")

# Save changes to the database
conn.commit()


# Define functions to add, update, delete, and search books in the database
def add_book():
    """Adds a new book to the ebookstore database.

      Prompts the user to enter the title, author, and quantity of the new
      book, and then inserts the book into the 'books' table in the database.

      Raises a ValueError if the user enters an invalid quantity value (i.e.,
      a non-integer value).

      Raises an Exception if there is an error inserting the new book into the
      database.
      """
    while True:
        try:
            title = input("Enter the title of the book: ")
            author = input("Enter the name of the author: ")
            qty = int(input("Enter the quantity of books: "))
            conn.execute("INSERT INTO books (Title, Author, Qty) VALUES (?, "
                         "?, ?)",
                         (title, author, qty))
            conn.commit()
            print("Book added successfully.")
            break
        except ValueError:
            print("Invalid input for quantity. Please enter a valid integer "
                  "value.")
        except Exception as e:
            print("Error:", e)


def update_book():
    """
        Updates the information of a book in the database.

        Prompts the user to enter the id of the book they want to update,
        as well as the new title, author, and quantity of books. If the user
        enters an invalid input for the book id or quantity, an appropriate
        error message is displayed. If an error occurs while updating the
        database, an error message is displayed.

        Raises:
            ValueError: If the user enters an invalid input for the book id or
            quantity.
            sqlite3.Error: If an error occurs while updating the database.

        """
    try:
        book_id = int(input("Enter the id of the book you want to update: "))
        title = input("Enter the new title of the book: ")
        author = input("Enter the new name of the author: ")
        qty = int(input("Enter the new quantity of books: "))
        conn.execute("UPDATE books SET Title=?, Author=?, Qty=? WHERE id=?",
                     (title, author, qty, book_id))
        conn.commit()
        print("Book updated successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number for the book id "
              "and quantity.")
    except sqlite3.Error as e:
        print("An error occurred:", e)


def delete_book():
    """
    Deletes a book from the database based on its id.

    Prompts the user to enter the id of the book to be deleted. If the id is
    invalid or if the book is not found, an appropriate error message is
    displayed. If the book is found and deleted successfully, a success message
    is displayed.

    Raises:
        ValueError: if the user enters an invalid id for the book.
        Exception: if there is an error while deleting the book from the
            database.

    """
    while True:
        try:
            book_id = int(input("Enter the id of the book you want to "
                                "delete: "))
            conn.execute("DELETE FROM books WHERE id=?", (book_id,))
            if conn.total_changes == 0:
                print("Book with id", book_id, "not found.")
            else:
                conn.commit()
                print("Book deleted successfully.")
            break
        except ValueError:
            print("Invalid input for book id. Please enter a valid integer "
                  "value.")
        except Exception as e:
            print("Error:", e)


def search_books():
    """
    Search the database for books matching a search term entered by the user.

    The function prompts the user to enter a search term (either a book
    title or author name), and retrieves all books whose title or author
    name contains the search term. The results are printed to the console.

    If the search is successful and books are found, their details are printed
    to the console. If no books are found, a message is displayed indicating
    that no books were found.

    If an error occurs while executing the SQL query, an error message is
    printed to the console.

    Raises:
        sqlite3.Error: if an error occurs while executing the SQL query
    """
    try:
        search_term = input("Enter the title or author of the book you want "
                            "to search for: ")
        cursor = conn.execute("SELECT * FROM books WHERE Title LIKE ? OR "
                              "Author LIKE ?",
                              ('%' + search_term + '%', '%' +
                               search_term + '%'))
        books = cursor.fetchall()
        if len(books) == 0:
            print("No books found.")
        else:
            for book in books:
                print(f"id: {book[0]}, title: {book[1]}, author: {book[2]}, "
                      f"qty: {book[3]}")
    except sqlite3.Error as e:
        print("An error occurred:", e)


def display_books():
    """
    Retrieves all books from the database and displays them in a formatted
    table.
    """
    cursor = conn.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    table = tabulate(rows, headers, tablefmt="fancy_grid")
    print(table)


# Define the main function to display the menu and handle user input
def main():
    """
    Main function for the ebookstore database program. Displays a menu of
    options for the user to select from and performs the corresponding
    action based on their choice. Continues to prompt the user until they
    choose to exit the program.

       Options:
       1. Enter book
       2. Update book
       3. Delete book
       4. Search books
       5. Display books
       0. Exit
    """
    while True:
        print("\nWelcome to the ebookstore database!")
        print("Please select an option from the menu below:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. Display books")
        print("0. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_book()
        elif choice == 2:
            update_book()
        elif choice == 3:
            delete_book()
        elif choice == 4:
            search_books()
        elif choice == 5:
            display_books()
        elif choice == 0:
            print("Goodbye!")
            conn.close()
            return
        else:
            print("Invalid choice. Please enter a number from 0 to 5.")


# calling functions to display the table and menu
display_books()
main()
