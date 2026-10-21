from deepface import DeepFace


def get_embedding(image_path):
    result = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet512",
        detector_backend="retinaface",
        enforce_detection=True
    )

    return result[0]["embedding"]