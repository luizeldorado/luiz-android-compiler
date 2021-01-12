import os, subprocess, shutil

class Project:
	def __init__(self, dir_project, package, dir_sdk, ver_buildtool, ver_platform, dir_keystore):
		self.dir_project = dir_project
		self.package = package
		self.dir_sdk = get_default_sdk(dir_sdk)
		self.ver_buildtool = get_default_buildtool(self.dir_sdk, ver_buildtool)
		self.ver_platform = get_default_platform(self.dir_sdk, ver_platform)
		self.dir_keystore = dir_keystore

def make_directory(project):

	# # new structure
	# "build"
	# "libs"
	# "src/main/java/com/example/package"
	# "src/main/gen"
	# "src/main/res"
	# "src/main/assets"
	# "src/main/java/AndroidManifest.xml"

	print("Making directories and files...")

	# generate a folder with a default project structure
	os.makedirs(get_dir_src_package(project))
	os.makedirs(get_dir_obj(project))
	os.makedirs(get_dir_bin(project))

	os.makedirs(os.path.join(get_dir_res(project), "layout"))
	os.makedirs(os.path.join(get_dir_res(project), "values"))
	os.makedirs(os.path.join(get_dir_res(project), "drawable"))

	make_mainactivity_java(project)
	make_string_xml(project)
	make_activity_main_xml(project)
	make_androidmanifest_xml(project)

	print("Finished.")

def build(project):
	# builds a project (makes final apk)
	
	# make r.java
	print("Making R.java...")
	make_r_java(project)

	# compile .java files into .class files
	print("Compiling Java code...")
	make_classes(project)

	# compile .class files into classes.dex
	print("Compiling into Dalvik code...")
	make_dex(project)

	# compile into apk
	print("Making APK file...")
	make_apk(project)

	# apk alignment
	print("Aligning APK...")
	apk_align(project)

	# apk signing
	print("Signing APK...")
	apk_sign(project)

	print("Finished.")

def launch(project):

	print("Installing APK...")

	# install apk
	adb_install(project)

	print("Launching...")

	# launch application
	adb_launch(project)

	print("Finished.")

## internal

def get_default_sdk(sdk):
	if sdk == None:
		sdk = os.getenv('ANDROID_SDK_ROOT')
		if sdk == None:
			raise Exception("ANDROID_SDK_ROOT env var missing!")
	return sdk

def get_default_buildtool(sdk, buildtool):
	if buildtool == None:
		list_buildtools = sorted(os.listdir( os.path.join(sdk, "build-tools") ))
	return list_buildtools[-1]

def get_default_platform(sdk, platform):
	if platform == None:
		list_platforms = sorted(os.listdir( os.path.join(sdk, "platforms") ))
	return list_platforms[-1]

def make_mainactivity_java(project):

	with open(os.path.join(get_dir_src_package(project), "MainActivity.java"), "w") as file:
		file.write(R"""package """+ project.package +R""";

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}
}""")

def make_string_xml(project):

	with open(os.path.join(get_dir_res(project), "values", "strings.xml"), "w") as file:
		file.write(R"""<?xml version="1.0" encoding="utf-8"?>

<resources>
	<string name="app_name">"""+ get_name(project) +R"""</string>
	<string name="hello_world">Hello, world!</string>
</resources>""")

def make_activity_main_xml(project):

	with open(os.path.join(get_dir_res(project), "layout", "activity_main.xml"), "w") as file:
		file.write(R"""<?xml version="1.0" encoding="utf-8"?>

<RelativeLayout
	xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools"
	android:layout_width="match_parent"
	android:layout_height="match_parent"
	>
	
	<TextView
		android:layout_width="wrap_content"
		android:layout_height="wrap_content"
		android:layout_centerHorizontal="true"
		android:layout_centerVertical="true"
		android:text="@string/hello_world"
		tools:context=".MainActivity"
		/>

</RelativeLayout>""")

def make_androidmanifest_xml(project):

	with open(get_dir_android_manifest(project), "w") as file:
		file.write(R"""<?xml version="1.0" encoding="utf-8"?>

<manifest
	xmlns:a='http://schemas.android.com/apk/res/android'
	package='"""+ project.package +R"""'
	a:versionCode='1'
	a:versionName='1'
	>
	<application a:label='"""+ get_name(project) +R"""'>
		<activity a:name='"""+ project.package +R""".MainActivity'>
			<intent-filter>
				<category a:name='android.intent.category.LAUNCHER'/>
				<action a:name='android.intent.action.MAIN'/>
			</intent-filter>
		</activity>
	</application>

</manifest>""")

def make_r_java(project):

	# os.remove(os.path.join(get_dir_src_package(project), "R.java"))

	subprocess.check_call(
		[
			get_dir_aapt(project), "package", "-f", "-m",
			"-J", get_dir_src(project),
			"-M", get_dir_android_manifest(project),
			"-S", get_dir_res(project),
			"-I", get_dir_android_jar(project)
		]
	)

def make_classes(project):

	shutil.rmtree(get_dir_obj(project))
	os.makedirs(get_dir_obj(project))

	# -bootclasspath is deprecated, I'm not sure how to replace it properly, just putting it in the classpath now.
	# I'm having to use Java 11, d8 doesn't work with anything higher, don't know why.

	subprocess.check_call(
		[
			get_dir_javac(project),
			"-d", get_dir_obj(project),
			"-classpath", ";".join([get_dir_android_jar(project), get_dir_src(project)]),
			# "-classpath", get_dir_src(project),
			# "-bootclasspath", get_dir_android_jar(project),
			"-source", "11",
			"-target", "11",
			os.path.join(get_dir_src_package(project), "*.java"),
			os.path.join(get_dir_src_package(project), "R.java"),
		],
	)

def make_dex(project):

	# os.remove(get_dir_classes_dex(project))

	# Aparently d8.bat and dx.bat are bugged and require manual adjustments to work. Because of that I'm directly calling the jar file from here.

	#'''
	buildlib = os.path.join(project.dir_sdk, "build-tools", project.ver_buildtool, "lib")
	d8jar = os.path.join(buildlib, "d8.jar")

	subprocess.check_call(
		[
			"java",
			"-classpath", ";".join([buildlib, d8jar]),
			"com.android.tools.r8.D8",
			os.path.join(get_dir_obj(project), project.package.replace(".", os.sep), "*.class"),
			"--release",
			"--output", project.dir_project,
			"--lib", get_dir_android_jar(project),
			"--classpath", get_dir_src(project),
		]
	)
	#'''

	'''
	subprocess.check_call(
		[
			get_dir_d8(project),
			os.path.join(get_dir_obj(project), project.package.replace(".", os.sep), "*.class"),
			"--release",
			"--output", project.dir_project,
			"--lib", get_dir_android_jar(project),
			# "--classpath", get_dir_src(project),
		]
	)
	'''

	'''
	subprocess.check_call(
		[
			get_dir_dx(project), "--dex",
			"--output", get_dir_classes_dex(project),
			get_dir_obj(project)
		]
	)
	'''

def make_apk(project):

	# os.remove(get_dir_apk(project))

	subprocess.check_call(
		[
			get_dir_aapt(project), "package", "-f", "-m",
			"-F", get_dir_apk(project),
			"-M", get_dir_android_manifest(project),
			"-S", get_dir_res(project),
			"-I", get_dir_android_jar(project)
		]
	)
	
	subprocess.check_call(
		[
			get_dir_aapt(project), "add", "-k",
			get_dir_apk(project),
			get_dir_classes_dex(project)
		]
	)

def apk_align(project):

	subprocess.check_call(
		[
			get_dir_zipalign(project), "-f", "4",
			get_dir_apk(project), get_dir_apk(project) + '.temp'
		]
	)

	os.replace(get_dir_apk(project) + '.temp', get_dir_apk(project))

def apk_sign(project):

	subprocess.check_call(
		[
			get_dir_apksigner(project), "sign",
			"--ks", get_dir_keystore(project), get_dir_apk(project)
		]
	)

def adb_install(project):

	subprocess.check_call(
		[
			get_dir_adb(project), "install", "-r", get_dir_apk(project)
		]
	)

def adb_launch(project):

	# adb shell monkey -p app.package.name -c android.intent.category.LAUNCHER 1
	subprocess.check_call(
		[
			get_dir_adb(project), "shell", "monkey",
			"-p", project.package,
			"-c", "android.intent.category.LAUNCHER", "1"
		]
	)

## getting stuff

def get_dir_aapt(project):
	return os.path.join(project.dir_sdk, "build-tools", project.ver_buildtool, "aapt")

def get_dir_javac(project):
	return "javac"

def get_dir_dx(project):
	return os.path.join(project.dir_sdk, "build-tools", project.ver_buildtool, "dx.bat")

def get_dir_d8(project):
	return os.path.join(project.dir_sdk, "build-tools", project.ver_buildtool, "d8.bat")

def get_dir_zipalign(project):
	return os.path.join(project.dir_sdk, "build-tools", project.ver_buildtool, "zipalign")

def get_dir_apksigner(project):
	return os.path.join(project.dir_sdk, "build-tools", project.ver_buildtool, "apksigner.bat")

def get_dir_adb(project):
	return os.path.join(project.dir_sdk, "platform-tools", "adb")


def get_dir_src(project):
	return os.path.join(project.dir_project, "src")

def get_dir_src_package(project):
	return os.path.join(project.dir_project, "src", project.package.replace(".", os.sep))

def get_dir_res(project):
	return os.path.join(project.dir_project, "res")

def get_dir_obj(project):
	return os.path.join(project.dir_project, "obj")

def get_dir_bin(project):
	return os.path.join(project.dir_project, "bin")

def get_dir_apk(project):
	return os.path.join(project.dir_project, "bin", get_name(project) + ".apk")


def get_dir_android_manifest(project):
	return os.path.join(project.dir_project, "AndroidManifest.xml")

def get_dir_classes_dex(project):
	return os.path.join(project.dir_project, "classes.dex")

def get_dir_keystore(project):
	return os.path.join(project.dir_keystore)


def get_dir_android_jar(project):
	return os.path.join(project.dir_sdk, "platforms", project.ver_platform, "android.jar")

def get_name(project):
	return os.path.basename(project.dir_project)
