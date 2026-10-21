import os
import json
from face_engine import get_embedding

PHOTO_FOLDER = "../photos"
DATABASE_FILE = "face_database.json"


def build_database():

    database = []

    for filename in os.listdir(PHOTO_FOLDER):

        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(PHOTO_FOLDER, filename)

        print(f"\nProcessing: {filename}")

        try:
            embedding = get_embedding(image_path)

            database.append({
                "filename": filename,
                "embedding": embedding
            })

            print("✅ Face embedding created")

        except Exception as e:
            print(f"❌ Could not process {filename}")
            print("Reason:", e)

    with open(DATABASE_FILE, "w") as file:
        json.dump(database, file)

    print("\n================================")
    print("Face database created successfully!")
    print("Total photos:", len(database))
    print("================================")


if __name__ == "__main__":
    build_database()