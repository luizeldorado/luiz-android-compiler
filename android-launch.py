import argparse, android

parser = argparse.ArgumentParser(description='Launch an app on a device')
parser.add_argument('project', help='path of project')
parser.add_argument('package', help='package name')
parser.add_argument('--sdk', help='android sdk path')

args = parser.parse_args()

android.launch(android.Project(args.project, args.package, args.sdk, None, None, None))