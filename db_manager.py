import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            if self.conn.is_connected():
                print("Successfully connected to the database")
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cursor = None

    def insert_summary(self, video_url, transcript, summary):
        if not self.conn or not self.cursor:
            print("Database connection is not available")
            return

        try:
            # Ensure no pending results before executing a new query
            self._process_pending_results()

            sql = "INSERT INTO summarizer (video_url, transcript, summary) VALUES (%s, %s, %s)"
            values = (video_url, transcript, summary)
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"Summary successfully inserted for video: {video_url}")
        except Error as e:
            print(f"Error inserting summary into MySQL: {e}")

    def fetch_transcript(self, video_url):
        if not self.conn or not self.cursor:
            print("Database connection is not available")
            return None

        try:
            # Ensure no pending results before executing a new query
            self._process_pending_results()

            sql = "SELECT transcript FROM summarizer WHERE video_url = %s"
            self.cursor.execute(sql, (video_url,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Error fetching transcript from MySQL: {e}")
            return None

    def _process_pending_results(self):
        # Method to process or clear any pending results
        while True:
            if self.cursor.nextset() is None:
                break

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("MySQL connection closed")

