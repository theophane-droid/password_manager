import hashlib
import argparse

def check_password(password, hash):
    """ 
    A function to check if password is correct
    password: str
    """
    hash_ = hashlib.sha3_512(bytes(password,"UTF-8")).hexdigest()
    return hash==hash_

def add_user(user_name, passwd):
    """
    A function to add a user to file
    param user_name: str; user_name sould not already exist in file
    param passwd: str
    """
    with open("passwd","r") as file:
        for line in file.readlines():
            if user_name==line.split(";")[0]:
                raise RuntimeError("Username already exists")

if __name__ == "__main__":
    """
    This main allow user to change password or to init one
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="describe the action to do : add or delete")
    parser.add_argument("username", help="describe the action to do : add or delete")
    args = parser.parse_args()
    if args.action not in ["add","delete"]:
        print("action option should be add or delete")
        exit(-1)
    

    password = bytes(input("please enter password (old one will be overwritted) : "), "UTF-8")
    hash_ = hashlib.sha3_512(password)
    with open("passwd","w") as file:
        file.write(hash_.hexdigest())
    print(check_password("coucou"))