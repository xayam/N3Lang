import math


def main():
    width = 32
    limit = 22
    passengers = range(1, width + 1)
    paths = dict()
    for departure in passengers:
        paths[departure] = []
        message = f"{departure}"
        destination = departure
        while True:
            destination = 4 * math.ceil(math.log2(destination)) + 2
            paths[departure].append(destination)
            if destination == limit:
                message += f" -> {limit}"
                break
            else:
                message += f" -> {destination}"
        print(message)


if __name__ == "__main__":
    main()
