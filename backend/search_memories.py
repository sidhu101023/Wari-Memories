import json
import numpy as np
from face_engine import get_embedding


DATABASE_FILE = "face_database.json"


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    similarity = np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

    return float(similarity)


def find_memories(selfie_path, threshold=0.60):

    # Generate embedding for selfie
    selfie_embedding = get_embedding(selfie_path)

    # Load stored database
    with open(DATABASE_FILE, "r") as file:
        database = json.load(file)

    matches = []

    for photo in database:

        similarity = cosine_similarity(
            selfie_embedding,
            photo["embedding"]
        )

        if similarity >= threshold:

            matches.append({
                "filename": photo["filename"],
                "similarity": similarity
            })

    # Highest similarity first
    matches.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return matches


if __name__ == "__main__":

    selfie_path = "../photos/test.jpg"

    results = find_memories(selfie_path)

    print("\n==============================")
    print("YOUR WARI MEMORIES")
    print("==============================")

    if not results:
        print("No matching memories found.")

    else:

        for result in results:

            print(
                f"{result['filename']} "
                f"→ similarity: "
                f"{result['similarity']:.3f}"
            )