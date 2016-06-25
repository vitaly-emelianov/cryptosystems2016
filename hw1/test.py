from sha48 import sha48


if __name__ == '__main__':
    with open("user.txt", 'r') as f:
        user_data = f.read()
    with open("attacker.txt", 'r') as f:
        attacker_data = f.read()
    print (user_data)
    print (attacker_data)

    print (sha48(user_data))
    print (sha48(attacker_data))
