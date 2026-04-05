import mysql.connector

# 🔗 Connect to database
def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="UMARCSE#3",
            database="lung_app"
        )
        return db
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Error: {err}")
        return None


# 💾 Save prediction result (WITH USER)
def save_result(username, filename, result, confidence):
    db = connect_db()

    if db is None:
        print("❌ Database connection failed")
        return

    try:
        cursor = db.cursor()

        query = """
        INSERT INTO results (username, filename, result, confidence)
        VALUES (%s, %s, %s, %s)
        """

        values = (username, filename, result, float(confidence))

        cursor.execute(query, values)
        db.commit()

        print("✅ Data saved successfully")

    except mysql.connector.Error as err:
        print(f"❌ Error saving data: {err}")

    finally:
        cursor.close()
        db.close()


# 📊 Fetch user-specific records
def get_results(username):
    db = connect_db()

    if db is None:
        return []

    try:
        cursor = db.cursor()

        query = "SELECT * FROM results WHERE username=%s ORDER BY created_at DESC"
        cursor.execute(query, (username,))

        data = cursor.fetchall()
        return data

    except mysql.connector.Error as err:
        print(f"❌ Error fetching data: {err}")
        return []

    finally:
        cursor.close()
        db.close()