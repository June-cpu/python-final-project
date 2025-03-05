# Python Final Project

## 📌 Project Overview

This project is a **web scraping and data visualization application** built using Flask, BeautifulSoup, Pandas, and Matplotlib. The application scrapes book data from Goodreads, processes it using Pandas, stores it in a PostgreSQL database, and provides data visualizations through a Flask API.

## 🚀 Features

- **Web Scraping:** Uses `BeautifulSoup` to extract book titles, authors, ratings, and the number of ratings from Goodreads.
- **Binary Search Tree (BST):** Implements a BST to store and manage book data before inserting it into a database.
- **PostgreSQL Database:** Stores scraped book data in a hosted PostgreSQL database on `Neon.tech`.
- **Data Processing:** Cleans and aggregates book data using `Pandas`.
- **Data Visualization:** Uses `Matplotlib` to generate visualizations, such as:
  - **Boxplot** of book ratings by authors.
  - **2D Histogram** comparing scaled number of ratings with average rating.
- **Flask API:** Serves data visualizations dynamically as PNG images.
- **Deployment:** Hosted on a Virtual Machine (VM) and accessible via `Render.com`.

## 📂 Project Structure

```
📦 project-directory
├── app.py            # Main Flask API and web scraping script
├── bst.py            # Binary Search Tree implementation for book storage
├── requirements.txt   # Dependencies and libraries
├── README.md         # Documentation
```

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository

```sh
git clone <repository-url>
cd project-directory
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Database Connection

Modify the `app.py` script with your PostgreSQL credentials:

```python
connection = psycopg2.connect(
    dbname="Books",
    user="Books_owner",
    password="your_password",
    host="your_database_host",
    sslmode="require"
)
```

### 5️⃣ Run the Application

```sh
python app.py
```

The server will start, and you can access it at `http://127.0.0.1:10000/`.

## 🎨 API Endpoints

| Endpoint   | Description                |
| ---------- | -------------------------- |
| `/`        | Welcome message            |
| `/hist2d`  | Returns 2D histogram image |
| `/boxplot` | Returns boxplot image      |

## 🖥 Deployment

This project is hosted on `Render.com` using a Virtual Machine (VM). If you want to deploy:

1. Create an account on [Render](https://render.com/).
2. Deploy the Flask app with a PostgreSQL database.
3. Configure environment variables and database settings accordingly.

## 📝 Future Improvements

- Add more endpoints for more visualizations
- Add more complex data visualizations.
- Optimize web scraping with multi-threading.

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

📌 **Created by:** [Junaid Tafader]

