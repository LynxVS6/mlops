from app.model import MODEL_PATH, train_and_save_model


if __name__ == "__main__":
    train_and_save_model()
    print(f"Model saved to {MODEL_PATH}")
