import inference


if __name__ == '__main__':
    user_clue = input()
    response = inference.pipe(user_clue)
    print(response)