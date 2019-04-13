# Luiz's Android Compiler

Bunch of scripts written in Python that help you develop Android applications. You can make, compile, and run Android apps without needing a heavy program like Eclipse or Android Studio.

## Requeriments

- Windows, probably.
- Python 3: https://www.python.org/downloads/
- Java Development Kit: https://www.oracle.com/technetwork/java/javase/downloads/index.html
- Android SDK command line tools: https://developer.android.com/studio/#command-tools
	- Android SDK Build Tools ("build-tools;[version]")
	- Android SDK Platform Tools ("platform-tools")
	- Android SDK Platform ("platforms;android-[version]")

## Scripts

`android-new-project.py name package`

Creates a new Android project folder.

`android-build.py project package keystore [--sdk SDK] [--buildtool BUILDTOOL] [--platform PLATFORM]`

Build the project into an APK.

`android-launch.py project package [--sdk SDK]`

Installs and launches the project on the default ADB device.

`android-build-and-launch.py project package keystore [--sdk SDK] [--buildtool BUILDTOOL] [--platform PLATFORM]`

Does these two things.

`android.py` is used by the other scripts, containing the main functionality.

### Common arguments

`name` or `project` is a directory path where an Android project is located.

`package` is a qualified Android package name (e.g. *com.example.hellothere*).

`keystore` is a keystore file path.

`sdk` is the location of the Android SDK. If ommited, it will look in the ANDROID_SDK_ROOT enviroment variable by default.

`buildtool` is the build tools version to be used. If ommited, it will select the most recent one.

`platform` is the platform version to be used. If ommited, it will select the most recent one.

# The point of this

Who needs Android Studio anyway?

The point is for people to be able to make their apps in an open enviroment, allowing them to see and change any part of the process as they please. It's a mid point between doing everything manually and using an IDE for everything. Come on, Eclipse is like 1 GB in size!

The build process of an Android app is complicated, but here I've simplified it. You can still look into the scripts to see what's going on, I tried to make it as neat as possible.

I don't wanna make a IDE with a GUI, but just simple tools that can help you out, not do literally everything for you. So this could be expanded by allowing automatic creation of layouts and activities, code linting, keystore creation, and much more. That the plan, bro. 