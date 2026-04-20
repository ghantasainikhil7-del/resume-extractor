import os


def get_resume_files(folder):

    files = []

    for root, dirs, filenames in os.walk(folder):
        for file in filenames:

            if file.endswith(".pdf"):
                files.append(os.path.join(root, file))

    return files
