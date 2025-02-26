from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import re
from rapidfuzz import process, fuzz

app = FastAPI()

# --- 1. Memuat data referensi dari Singkatan.xlsx ---
df_institutions = pd.read_excel('Singkatan.xlsx')

# Membuat dictionary singkatan -> nama lengkap
institution_mapping = {
    row['Singkatan'].strip().upper(): row['Nama'].strip().upper()
    for _, row in df_institutions.iterrows()
    if pd.notna(row['Singkatan']) and row['Singkatan'].strip() != ''
}

# Membuat daftar nama resmi institusi untuk fuzzy matching
official_names = list({row['Nama'].strip().upper()
                       for _, row in df_institutions.iterrows()
                       if pd.notna(row['Nama']) and row['Nama'].strip() != ''})


def is_abbreviation(word, mapping):
    return word.strip().upper() in mapping


def replace_abbreviation(text, mapping):
    words = text.split()
    for i, word in enumerate(words):
        if word in mapping:
            words[i] = mapping[word]  # Ganti singkatan dengan nama lengkap
    return " ".join(words)


def clean_after_institution(text):
    pattern = r"(UNIVERSITAS|INSTITUT|POLITEKNIK|SEKOLAH TINGGI) [A-Z ]+"
    match = re.search(pattern, text)
    if match:
        return match.group(0)  # Hanya ambil nama institusi
    return text  # Jika tidak ada yang cocok, tetap gunakan teks asli


def clean_text(text, mapping, official_names, fuzzy_threshold=85):
    text = text.upper().strip()
    
    # --- Penanganan pola tanda kurung ---
    m = re.search(r'^(.*?)\((.*?)\)(.*)$', text)
    if m:
        left = m.group(1).strip()
        paren_content = m.group(2).strip()
        right = m.group(3).strip()
        
        if is_abbreviation(left, mapping) and paren_content:
            full_name = paren_content
            words_in_right = right.split()
            if words_in_right and words_in_right[-1].upper() == left.strip().upper():
                right = ' '.join(words_in_right[:-1]).strip()
            text = (full_name + " " + right).strip()
        elif is_abbreviation(paren_content, mapping):
            text = (left + " " + right).strip()
        else:
            text = (left + " " + right).strip()

    # --- Mengganti singkatan dengan nama lengkap ---
    text = replace_abbreviation(text, mapping)

    # --- Ekstraksi berdasarkan keyword institusi ---
    text = clean_after_institution(text)

    # --- Fuzzy matching ---
    best_match, score, _ = process.extractOne(text, official_names, scorer=fuzz.token_sort_ratio)
    if score >= fuzzy_threshold:
        text = best_match
    elif len(text.split()) > 8:
        best_match, score, _ = process.extractOne(text, official_names, scorer=fuzz.token_sort_ratio)
        if score >= 60:
            text = best_match

    text = ' '.join(text.split())
    return text


class InputData(BaseModel):
    name: str


@app.post("/clean/")
async def clean_name(data: InputData):
    cleaned_name = clean_text(data.name, institution_mapping, official_names)
    return {"cleaned": cleaned_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
