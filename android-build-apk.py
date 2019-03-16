import argparse
import os, subprocess, sys, shutil, pprint

parser = argparse.ArgumentParser(description='Builds an APK from project')
parser.add_argument('project', help='path of project')
parser.add_argument('package', help='package name')
parser.add_argument('--sdk', help='android sdk path')
parser.add_argument('--buildtool', help='buildtool version')
parser.add_argument('--platform', help='platform')

def main(args):

	args = parser.parse_args(args)

	dir_project = args.project

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

	if args.platform == None:
		platform = 'android-21' # TODO: find best one
	else:
		platform = args.platform

	dir_aapt = os.path.join(dir_sdk, R"""build-tools""", buildtool, R"""aapt.exe""")
	dir_platform = os.path.join(dir_sdk, R"""platforms""", platform, R"""android.jar""")

	dir_javac = "javac";
	dir_packaging = os.path.join("src", args.package.replace(".", "\\"))

	dir_dx = os.path.join(dir_sdk, R"""build-tools""", buildtool, R"""dx.bat""")

	dir_apk = os.path.join("bin", args.project + ".apk")

	print("Generating R.java file...")

	c = subprocess.call([dir_aapt, "package", "-f", "-m", "-J", "src", "-M", "AndroidManifest.xml", "-S", "res", "-I", dir_platform],
		cwd = dir_project)
	if c != 0: exit()

	print("Compiling...")

	# TODO: loop through all files
	c = subprocess.call([dir_javac, "-d", "obj", "-classpath", "src", "-bootclasspath", dir_platform,
		dir_packaging + R"""\MainActivity.java""",
		],
		cwd = dir_project)
	if c != 0: exit()

	c = subprocess.call([dir_javac, "-d", "obj", "-classpath", "src", "-bootclasspath", dir_platform, dir_packaging + R"""\R.java"""],
		cwd = dir_project)
	if c != 0: exit()

	print("Translating in Dalvik bytecode...")

	c = subprocess.call([dir_dx, "--dex", "--output=classes.dex", "obj"],
		cwd = dir_project)
	if c != 0: exit()

	print("Making APK...")

	c = subprocess.call([dir_aapt, "package", "-f", "-m", "-F", dir_apk, "-M", "AndroidManifest.xml", "-S", "res", "-I", dir_platform],
		cwd = dir_project)
	if c != 0: exit()
	
	c = subprocess.call([dir_aapt, "add", dir_apk, "classes.dex"],
		cwd = dir_project)
	if c != 0: exit()

	print("Done!")

if __name__ == "__main__":

	main(sys.argv[1:])