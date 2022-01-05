from changes_finder import CF


def main():
    print(CF(b"hello", b"world").encoded_changes)


if __name__ == '__main__':
    main()
