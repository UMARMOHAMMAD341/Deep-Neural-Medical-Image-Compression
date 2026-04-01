import mysql.connector

# 🔗 Connect to database
def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="UMARCSE#3",   # 🔴 change this
            database="lung_app"
        )
        return db
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None


# 💾 Save prediction result
def save_result(filename, result, confidence):
    db = connect_db()
    
    if db is None:
        print("❌ Database connection failed")
        return

    try:
        cursor = db.cursor()

        query = """
        INSERT INTO results (filename, result, confidence)
        VALUES (%s, %s, %s)
        """

        values = (filename, result, float(confidence))

        cursor.execute(query, values)
        db.commit()

        print("✅ Data saved successfully")

    except mysql.connector.Error as err:
        print(f"❌ Error saving data: {err}")

    finally:
        db.close()


# 📊 Fetch all records (optional - for history)
def get_results():
    db = connect_db()
    
    if db is None:
        return []

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM results ORDER BY created_at DESC")
        data = cursor.fetchall()
        return data

    except mysql.connector.Error as err:
        print(f"❌ Error fetching data: {err}")
        return []

    finally:
        db.close()