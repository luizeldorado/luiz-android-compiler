import argparse
import os, subprocess, sys

parser = argparse.ArgumentParser(description='Launch an app on a device')
parser.add_argument('apk', help='apk file')
parser.add_argument('package', help='package name')
parser.add_argument('--sdk', help='android sdk path')

def main(args):

	args = parser.parse_args(args)
	
	dir_apk = args.apk

	if args.sdk == None:
		dir_sdk = os.getenv('ANDROID_SDK_HOME','')
		if dir_sdk == "":
			print('Could not get Android SDK path because ANDROID_SDK_HOME envs are missing.')
			exit()
	else:
		dir_sdk = args.sdk

	dir_adb = os.path.join(dir_sdk, R"""platform-tools""", R"""adb.exe""")

	print("Installing...")

	c = subprocess.call([dir_adb, "install", "-r", dir_apk])
	if c != 0: exit()

	print("Launching...")

	# adb shell monkey -p app.package.name -c android.intent.category.LAUNCHER 1
	c = subprocess.call([dir_adb, "shell", "monkey", "-p", args.package, "-c", "android.intent.category.LAUNCHER", "1"])
	if c != 0: exit()

	print("Done!")

if __name__ == "__main__":

	main(sys.argv)