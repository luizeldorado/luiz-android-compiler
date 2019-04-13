import argparse, android

parser = argparse.ArgumentParser(description='Builds, aligns, signs and launches a project')
parser.add_argument('project', help='path of project')
parser.add_argument('package', help='package name')
parser.add_argument('keystore', help='keystore file')
parser.add_argument('--sdk', help='android sdk path')
parser.add_argument('--buildtool', help='buildtool version')
parser.add_argument('--platform', help='platform')

args = parser.parse_args()

project = android.Project(args.project, args.package, args.sdk, args.buildtool, args.platform, args.keystore)

android.build(project)
android.launch(project)