from face_engine import get_embedding

image_path = "../photos/test.jpg"

embedding = get_embedding(image_path)

print("Face detected successfully!")
print("Embedding length:", len(embedding))
print("First 10 values:")
print(embedding[:10])