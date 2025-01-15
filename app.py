import requests
from bs4 import BeautifulSoup
import re
from bst import BinarySearchTree
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import io
from flask import Flask, send_file

# ================ WEB SCRAPING =====================
def fetch_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch web page. Status code: {response.status_code}")

def scrape_books(url, bst):
    html = fetch_data(url)
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', class_='tableList')

    for row in table.find_all('tr'):
        title_tag = row.find('a', class_='bookTitle')
        title = title_tag.text.strip() if title_tag else "N/A"

        author_tag = row.find('a', class_='authorName')
        author = author_tag.text.strip() if author_tag else "N/A"

        rating_tag = row.find('span', class_='minirating')
        if rating_tag:
            rating_text = rating_tag.text.strip()
            rating_match = re.search(r'([\d.]+) avg rating', rating_text)
            num_ratings_match = re.search(r'— ([\d,]+) ratings', rating_text)

            rating = rating_match.group(1) if rating_match else "N/A"
            num_ratings = num_ratings_match.group(1).replace(',', '') if num_ratings_match else "N/A"
        else:
            rating = "N/A"
            num_ratings = "N/A"

        if title != "N/A" and author != "N/A" and rating != "N/A" and num_ratings != "N/A":
            bst.insert(title, {"author": author, "rating": rating, "num_ratings": num_ratings})

book_tree = BinarySearchTree()

urls = [
    'https://www.goodreads.com/list/show/153.Most_Exciting_Upcoming_YA_Books',
    'https://www.goodreads.com/list/show/153.Most_Exciting_Upcoming_YA_Books?page=2'
]
for i in range(1, 2):
    urls.append(f'https://www.goodreads.com/list/show/43.Best_Young_Adult_Books?page={i}')
    urls.append(f'https://www.goodreads.com/list/show/36335.Indie_Authors_to_Watch?page={i}')

for url in urls:
    scrape_books(url, book_tree)

#==================== DATABASE CONNECTION ================
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="Books",
            user="Books_owner",
            password="siwrt4dqXZ1g",
            host="ep-shiny-bush-a57fyw9f.us-east-2.aws.neon.tech",
            sslmode="require"
        )
        connection.autocommit = True
        print("Connected to the database successfully")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")

db_connection = connect_to_db()

def insert_book_data(db_connection, book_data):
    try:
        cursor = db_connection.cursor()
        query = """
        INSERT INTO books (title, author, rating, num_ratings)
        VALUES (%s, %s, %s, %s);
        """
        for book in book_data:
            cursor.execute(query, (book['title'], book['author'], book['rating'], book['num_ratings']))
        print("Book data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

books_data = [{"title": key, **data} for key, data in book_tree.inorder()]
insert_book_data(db_connection, books_data)

# =============================== PANDAS ===============================
def fetch_data_to_dataframe(connection):
    query = "SELECT * FROM books;"
    cursor = connection.cursor()
    cursor.execute(query)

    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    dataframe = pd.DataFrame(records, columns=column_names)
    cursor.close()

    return dataframe


def clean_and_transform(dataframe):
    dataframe['rating'] = dataframe['rating'].astype(float)
    dataframe['num_ratings'] = dataframe['num_ratings'].astype(int)
    dataframe.rename(columns={'title': 'book_title', 'author': 'book_author'}, inplace=True)
    dataframe = dataframe.ffill() 
    return dataframe


def aggregate_data(dataframe):
    aggregated_df = dataframe.groupby('book_author').agg({
        'rating': 'mean',
        'num_ratings': 'sum'
    }).reset_index()
    aggregated_df['rating'] = aggregated_df['rating'].round(1)
    return aggregated_df

df = fetch_data_to_dataframe(db_connection)
df_cleaned = clean_and_transform(df)
df_aggregated = aggregate_data(df_cleaned)

# ============================ MATPLOTLIB ============================
def plot_average_ratings(dataframe):
    plt.figure(figsize=(10, 5))
    plt.bar(dataframe['book_author'], dataframe['rating'], color='skyblue')
    plt.title('Average Ratings by Author')
    plt.xlabel('Author')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.tight_layout()

def plot_total_ratings(dataframe):
    plt.figure(figsize=(10, 5))
    plt.plot(dataframe['book_author'], dataframe['num_ratings'], marker='o', color='green')
    plt.title('Total Ratings by Author')
    plt.xlabel('Author')
    plt.ylabel('Total Ratings')
    plt.xticks(rotation=45)
    plt.tight_layout()

# ============================ FLASK API ============================
app = Flask(__name__)
plt.switch_backend('Agg')

@app.route('/average_ratings')
def average_ratings():
    plot_average_ratings(df_aggregated)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/total_ratings')
def total_ratings():
    plot_total_ratings(df_aggregated)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/')
def home():
    return "Welcome to the Book Data Visualization API! Use /average_ratings or /total_ratings to view visualizations."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
