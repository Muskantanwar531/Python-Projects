import pandas as pd
import re

# -----------------------------
# 1) Keyword Rules (Simple)
# -----------------------------
RULES = {
    "Violence": ["kill", "murder", "shoot", "stab", "attack"],
    "Self-Harm": ["suicide", "hurt myself", "end my life", "cut myself"],
    "Harassment": ["idiot", "stupid", "ugly", "loser", "dumb"],
    "Sexual": ["nude", "sex", "porn", "xxx"],
    "Profanity": ["hell", "damn"]
}

# -----------------------------
# 2) Regex Rules (Advanced)
# (For censored abusive words)
# -----------------------------
REGEX_RULES = {
    "Profanity": [
        r"\bf\*+k\b",     # f**k
        r"\bsh\*+t\b",    # sh*t
        r"\bb\*+ch\b"     # b**ch
    ]
}


# -----------------------------
# 3) Function: Detect categories
# -----------------------------
def detect_categories(text):
    text_lower = str(text).lower()
    matched_categories = []

    # Keyword matching
    for category, keywords in RULES.items():
        for word in keywords:
            if word in text_lower:
                matched_categories.append(category)
                break  # stop checking more words for this category

    # Regex matching
    for category, patterns in REGEX_RULES.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                if category not in matched_categories:
                    matched_categories.append(category)
                break

    return matched_categories


# -----------------------------
# 4) Main Program
# -----------------------------
def main():
    input_file = "data/sample_text.csv"
    output_file = "output/flagged_report.csv"

    # Read CSV
    df = pd.read_csv(input_file)

    # Check if required column exists
    if "text" not in df.columns:
        print("ERROR: Your CSV must contain a column named 'text'")
        return

    # Apply detection
    df["categories"] = df["text"].apply(detect_categories)

    # Toxic label
    df["toxic"] = df["categories"].apply(lambda x: "Yes" if len(x) > 0 else "No")

    # Convert list to readable string
    df["categories"] = df["categories"].apply(lambda x: ", ".join(x) if len(x) > 0 else "None")

    # Save output
    df.to_csv(output_file, index=False)

    # Print summary
    print("✅ Toxic detection completed successfully!")
    print(f"📄 Output saved to: {output_file}")

    print("\n--- Summary ---")
    print(df["toxic"].value_counts())


if __name__ == "__main__":
    main()
