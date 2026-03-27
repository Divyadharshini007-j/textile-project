import os

def replace_in_files(directory, old_str, new_str):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jsx', '.js', '.html')):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if old_str in content:
                    print(f"Replacing in {path}")
                    new_content = content.replace(old_str, new_str)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    replace_in_files('c:/Users/divya/Downloads/textile_ai_project/frontend/src', 'localhost:8000', '127.0.0.1:8000')
