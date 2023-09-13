import matplotlib.pyplot as plt


def test(add):
    plt.savefig(f"date{add}")

def main():
    test(3)


if __name__ == '__main__':
    main()