from pathlib import Path
import markovify
import re



def generate_by_idea(model, idea, n=1000, result=10, tr=100):
    words = idea.lower().split()
    out = []

    for _ in range(n):
        s = model.make_sentence(tries=tr)
        if not s:
            continue

        score = sum(s.lower().count(w) for w in words)
        if score > 0:
            out.append((score, s))

    out.sort(reverse=True)
    return [s for score, s in out[:result]]

if __name__=="__main__":
    pesen_files_list = [
        # "Soldatenko_Eva.250281.fb2.txt",
        # "Soldatenko_Kogda-utonet-cherepaha.529623.fb2.txt",
        # "Soldatenko_Malenkaya-opera.629214.fb2.txt",
        "Soldatenko_Razvody-sbornik-.565292.fb2.txt",
        "Soldatenko_Santehnik_1_Santehnik-ego-kot-zhena-i-drugie-podrobnosti.194865.fb2.txt",
        "Soldatenko_Santehnik_2_Santehnik-Tvoyo-moyo-koleno.347883.fb2.txt",
        "Soldatenko_Santehnik_3_Posledniy-santehnik.4306`91.fb2.txt",
        "Soldatenko_Santehnik_4_Santehnik-s-pylu-i-s-zharom.533217.fb2.txt",
        "Soldatenko_Ves-santehnik-v-odnoy-stopke.393617.fb2.txt",
        # "Soldatenko_Zhiraf.227925.fb2.txt",
        "jj_pesen.txt"
    ]
    gnomo_files_list = ["jj_gnomomamochka.txt", "jj_gnomo_otrageniya.txt"]
    
    target_dir = ["txt_gnomo", "txt_pesen"]

    idea_text = """Всем привет. Да здравствует синагога!"""

    
    texts = []
    for i in range(len(gnomo_files_list)):
        text_file = Path("..", "data", target_dir[0], gnomo_files_list[i])

        # load text
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)

    all_books = " ".join(texts)
    # train model
    model_slava = markovify.Text(all_books, state_size=2)

    sentences = generate_by_idea(model=model_slava, idea=idea_text, result=3, tr=20) 

    for i in range(len(sentences)):
        print(sentences[i])
