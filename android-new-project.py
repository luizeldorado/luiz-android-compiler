import argparse, android

parser = argparse.ArgumentParser(description='Creates new project on a folder name')
parser.add_argument('name', help='app name and folder')
parser.add_argument('package', help='package name')

args = parser.parse_args()

android.make_directory(android.Project(args.name, args.package, None, None, None, None))