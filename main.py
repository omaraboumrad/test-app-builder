import argparse

from gen import apps_builder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='target django directory')
    parser.add_argument('-a', '--apps', default=1, type=int)
    parser.add_argument('-m', '--models', default=1, type=int)

    args = parser.parse_args()

    apps = apps_builder(args.target, args.apps, args.models)


