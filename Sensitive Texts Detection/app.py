import streamlit as st
import pandas as pd
import re

# -----------------------------
# Rules
# -----------------------------
RULES = {
    "Violence": ["kill", "murder", "shoot", "stab", "attack"],
    "Self-Harm": ["suicide", "hurt myself", "end my life", "cut myself"],
    "Harassment": ["idiot", "stupid", "ugly", "loser", "dumb"],
    "Sexual": ["nude", "sex", "porn", "xxx"],
    "Profanity": ["hell", "damn"]
}

REGEX_RULES = {
    "Profanity": [
        r"\bf\*+k\b",     # f**k
        r"\bsh\*+t\b",    # sh*t
        r"\bb\*+ch\b"     # b**ch
    ]
}


# -----------------------------
# Detection Function
# -----------------------------
def detect_categories(text):
    text_lower = str(text).lower()
    matched_categories = []

    # Keyword matching
    for category, keywords in RULES.items():
        for word in keywords:
            if word in text_lower:
                matched_categories.append(category)
                break

    # Regex matching
    for category, patterns in REGEX_RULES.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                if category not in matched_categories:
                    matched_categories.append(category)
                break

    return matched_categories


def process_dataframe(df, text_col):
    df = df.copy()

    df["categories"] = df[text_col].apply(detect_categories)
    df["toxic"] = df["categories"].apply(lambda x: "Yes" if len(x) > 0 else "No")
    df["categories"] = df["categories"].apply(lambda x: ", ".join(x) if len(x) > 0 else "None")

    return df


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Sensitive Text Detection", page_icon="🛡️", layout="wide")

st.title("🛡️ Sensitive / Toxic Text Detection")
st.write("Check if a text contains toxic or sensitive content. You can also upload a CSV file and download the results.")

st.divider()

# --- Single text check ---
st.subheader("✅ Check Single Text")

user_text = st.text_area("Enter a text message:", height=100)

if st.button("Analyze Text"):
    categories = detect_categories(user_text)
    toxic = "Yes" if len(categories) > 0 else "No"

    st.write("### Result")
    st.write(f"**Toxic:** {toxic}")
    st.write(f"**Categories:** {', '.join(categories) if categories else 'None'}")

st.divider()

# --- CSV Upload ---
st.subheader("📂 Upload CSV for Bulk Detection")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview of Uploaded File")
    st.dataframe(df.head(10))

    st.write("### Select the text column")
    text_col = st.selectbox("Choose column containing text:", df.columns)

    if st.button("Run Bulk Detection"):
        result_df = process_dataframe(df, text_col)

        st.success("✅ Detection completed!")

        st.write("### Output Report (Preview)")
        st.dataframe(result_df.head(20))

        # Summary
        st.write("### 📊 Summary")
        toxic_counts = result_df["toxic"].value_counts()
        st.write("**Toxic vs Non-Toxic:**")
        st.write(toxic_counts)

        # Category count
        st.write("**Category Counts:**")
        category_counts = result_df["categories"].value_counts()
        st.write(category_counts)

        # Download button
        csv_data = result_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Output CSV Report",
            data=csv_data,
            file_name="flagged_report.csv",
            mime="text/csv"
        )
