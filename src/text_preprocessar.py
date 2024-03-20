import re
import unicodedata


def normalize_text(text):
    """
    Normalize text by converting to lowercase, removing punctuation,
    and eliminating accents and diacritics.

    Parameters:
    - text: The text to normalize.

    Returns:
    - The normalized text.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove accents and diacritics
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    # Remove punctuation (excluding simple punctuation like '.', '!', '?')
    text = re.sub(r'[\,\;\:\(\)\[\]\"\'\“\”\‘\’\—\-\/\+\*\&\^\%\$\#\@\!\=\`\<\>\~\|\\]', ' ', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def preprocess_texts(texts):
    """
    Apply normalization to a list of texts.

    Parameters:
    - texts: A list of texts to preprocess.

    Returns:
    - A list of normalized texts.
    """
    return [normalize_text(text) for text in texts]


if __name__ == "__main__":
    # Example usage
    example_texts = ["Este é um texto exemplo! Será que funciona?", "Testando a normalização de TEXTOS..."]
    normalized_texts = preprocess_texts(example_texts)
    print("Normalized texts:", normalized_texts)
