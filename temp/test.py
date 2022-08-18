from utils import array


def main():
    print(array.get_real_val({'a': {'b': {}}}, 'a|b|c'))
    print(array.get_real_val({'a': {'b': {}}}, 'a'))
    print(array.get_real_lst({'a': {'b': {}}}, 'a'))

    pass


if __name__ == "__main__":
    main()
