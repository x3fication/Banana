arguments = ["name"]
usage = "hello <name>\nSays hello to the specified name."

def run(args):
    print(f"Hello {args['name']}!")