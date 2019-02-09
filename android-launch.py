import argparse
import os, subprocess

parser = argparse.ArgumentParser(description='Launch an app on a device')
parser.add_argument('apk', help='apk file')
parser.add_argument('--sdk', help='android sdk path')
parser.add_argument('--buildtool', help='buildtool version')

args = parser.parse_args()

dir_apk = args.apk

if args.sdk == None:
	dir_sdk = os.getenv('ANDROID_SDK_HOME','')
	if dir_sdk == "":
		print('Could not get Android SDK path because ANDROID_SDK_HOME envs are missing.')
		exit()
else:
	dir_sdk = args.sdk

if args.buildtool == None:
	buildtool = '28.0.2' # TODO: find most recent one
else:
	buildtool = args.buildtool

dir_adb = os.join(dir_sdk, R"""build-tools""", buildtool, R"""adb.exe""")

print("Launching...")

subprocess.call([dir_adb, "install", "-r", dir_apk],
	cwd = dir_project)

# wtf is this
# subprocess.call([dir_adb, "shell", "am", "start", "-n", dir_packaging_android + R"""/.MainActivity"""],
# 	cwd = dir_project)

print("Done!")