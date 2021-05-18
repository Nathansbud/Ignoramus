from PyInquirer import prompt
from sys import argv
from os import getcwd, rename
from pathlib import Path
from shutil import copy

VALID_CHOICES = ["python", "default"]
TEMPLATE_PATH = Path(Path(__file__).parent).joinpath("templates")
questions = [
    {
        "type": "list",
        "name": "_language",
        "message": "Project Type?",
        "choices": [c.title() for c in VALID_CHOICES]
    }
]

def build_gitignore(_language):
    language = _language.lower()
    
    try:
        with open(TEMPLATE_PATH.joinpath(f"{language}.gitignore"), "r") as language_gitignore, \
            open(Path(getcwd()).joinpath(".gitignore"), "w+") as output_gitignore:

            contents = []
            if language != 'default':
                with open(TEMPLATE_PATH.joinpath("default.gitignore"), "r") as default_gitignore:
                    contents.extend(default_gitignore.readlines())

            contents.extend(["\n"] + language_gitignore.readlines())
            output_gitignore.writelines([c if c.endswith('\n') else f'{c}\n' for c in contents])
    except FileNotFoundError:
        print(f"'{language}' is as a valid option, but no corresponing .gitignore could be located for it. Did you remember to create one?")

if __name__ == "__main__":
    if len(argv) == 1:
        responses = prompt(questions)
        if responses.get('_language'):
            build_gitignore(**responses)
    else:
        user_choice = " ".join(argv[1:]).strip().lower()
        if user_choice in VALID_CHOICES:
            build_gitignore(user_choice)
        else:
            print(
                f"No .gitignore template exists for '{user_choice}'! Did you misspell something?\n",
                "Current options:",
                "".join(sorted([f"  • {p}\n" for p in TEMPLATE_PATH.rglob('*.gitignore')])),
                sep='\n'
            )
