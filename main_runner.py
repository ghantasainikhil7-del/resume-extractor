import pandas as pd
import multiprocessing
from tqdm import tqdm
from os_walk import get_resume_files
from resume_extractor import extract_text
from resume_parser import extract_name, extract_email, extract_phone, extract_skills


def process_resume(args):

    index, file = args

    text = extract_text(file)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    return (index, [name, email, phone, skills])


def main():

    files = get_resume_files("data")

    print("Total resumes:", len(files))

    indexed_files = list(enumerate(files))

    pool = multiprocessing.Pool(4)

    results = []

    for result in tqdm(pool.imap(process_resume, indexed_files), total=len(indexed_files)):
        results.append(result)

    pool.close()
    pool.join()

    results.sort(key=lambda x: x[0])

    data = [r[1] for r in results]

    df = pd.DataFrame(data, columns=["Name","Email","Phone","Skills"])

    import os
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/resume_data.csv", index=False)

    print("Extraction completed")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()