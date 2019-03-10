import argparse, importlib, os

parser = argparse.ArgumentParser(description='Builds, aligns, signs and launches a project')
parser.add_argument('project', help='path of project')
parser.add_argument('package', help='package name')
parser.add_argument('keystore', help='keystore file')

args = parser.parse_args()

apk_name = os.path.join(args.project, 'bin', os.path.basename(args.project) + '.apk')

android_build = importlib.import_module('android-build-apk')
android_align = importlib.import_module('android-align-apk')
android_sign = importlib.import_module('android-sign-apk')
android_launch = importlib.import_module('android-launch')

android_build.main([args.project, args.package])
android_align.main([apk_name])
android_sign.main([apk_name + '-aligned.apk', args.keystore])
android_launch.main([apk_name + '-aligned.apk', args.package])