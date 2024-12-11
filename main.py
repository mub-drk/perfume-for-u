try:
    from transformers import pipeline
except ModuleNotFoundError:
    print("The 'transformers' library is not installed. Please install it by running 'pip install transformers'.")

    def fallback_personality_analysis(answers):
        """Fallback method for personality analysis if the transformers library is not available."""
        print("\nUsing fallback personality analysis...\n")
        if answers["adventure"].lower() == "yes" and answers["outgoing"].lower() == "yes":
            return "ADVENTUROUS"
        elif answers["calm"].lower() == "yes" and answers["creative"].lower() == "yes":
            return "CALM"
        elif answers["outgoing"].lower() == "yes":
            return "OUTGOING"
        else:
            return "RESERVED"

    def initialize_model():
        return None
else:
    def initialize_model():
        """Initializes a local lightweight model for personality analysis."""
        try:
            print("Loading local LLM model...")
            model = pipeline("text-classification", model="distilbert-base-uncased")
            print("Model loaded successfully.")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

def get_personality_and_perfume(model, answers):
    """Analyzes personality based on user input and suggests a perfume."""
    print("\nAnalyzing your personality...\n")

    # Combine answers into a single text for analysis
    input_text = " ".join([f"{key}: {value}" for key, value in answers.items()])

    # Use the model to determine personality traits
    if model:
        try:
            prediction = model(input_text)
            personality = prediction[0]['label']  # Assuming the label gives the personality type
        except Exception as e:
            print(f"Error during model prediction: {e}")
            personality = "Unknown"
    else:
        personality = fallback_personality_analysis(answers)

    # Suggest perfume based on personality
    perfumes = {
        "ADVENTUROUS": ("Bleu de Chanel", "Woody Aromatic"),
        "CALM": ("Jo Malone Peony & Blush Suede", "Floral"),
        "OUTGOING": ("Dior Sauvage", "Fresh Spicy"),
        "RESERVED": ("Chanel No. 5", "Floral Aldehyde")
    }

    perfume = perfumes.get(personality.upper(), ("Generic Perfume", "Unknown"))

    # Display results
    print(f"Personality: {personality}")
    print(f"Suggested Perfume: {perfume[0]} ({perfume[1]})")

def main():
    """Main function to run the program."""
    print("Welcome to the Personality and Perfume Suggestion Program!\n")

    # Asking questions
    questions = [
        "What is your gender? (Male/Female/Other): ",
        "Do you enjoy adventure and trying new things? (Yes/No): ",
        "Do you prefer calming and soothing experiences? (Yes/No): ",
        "Are you outgoing and sociable? (Yes/No): ",
        "Do you consider yourself creative and imaginative? (Yes/No): "
    ]

    # Collect answers
    answers = {}
    keys = ["gender", "adventure", "calm", "outgoing", "creative"]

    for question, key in zip(questions, keys):
        try:
            answers[key] = input(question).strip()
        except (EOFError, ValueError):
            print(f"\nUnable to process input for '{key}'. Defaulting to 'Unknown'.")
            answers[key] = "Unknown"

    # Initialize the model and process results
    model = initialize_model()
    get_personality_and_perfume(model, answers)

if __name__ == "__main__":
    main()
