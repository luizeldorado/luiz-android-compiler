import argparse
import os, subprocess, sys

parser = argparse.ArgumentParser(description='Signs a APK')
parser.add_argument('apk', help='apk file')
parser.add_argument('keystore', help='keystore file')
parser.add_argument('--sdk', help='android sdk path')
parser.add_argument('--buildtool', help='buildtool version')

def main(args):

	args = parser.parse_args(args)

	dir_apk = args.apk
	dir_keystore = args.keystore

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

	dir_apksigner = os.path.join(dir_sdk, R"""build-tools""", buildtool, R"""apksigner.bat""")

	print("Signing APK...")

	c = subprocess.call([dir_apksigner, "sign", "--ks", dir_keystore, dir_apk])
	if c != 0: exit()

	print("Done!")

if __name__ == "__main__":

	main(sys.argv)