import sys

def query_yes_no(question):
    valid = {
        "yes": True, "y": True, "ye": True,
        "no": False, "n": False
    }
    prompt = " [Y/n] "

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '':
            return valid["yes"]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
