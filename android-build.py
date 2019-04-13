import argparse, android

parser = argparse.ArgumentParser(description='Builds an APK from project')
parser.add_argument('project', help='path of project')
parser.add_argument('package', help='package name')
parser.add_argument('keystore', help='keystore')
parser.add_argument('--sdk', help='android sdk path')
parser.add_argument('--buildtool', help='buildtool version')
parser.add_argument('--platform', help='platform')

args = parser.parse_args()

android.build(android.Project(args.project, args.package, args.sdk, args.buildtool, args.platform, args.keystore))