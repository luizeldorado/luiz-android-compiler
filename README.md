# Luiz's Android Compiler

Bunch of scripts written in Python that help you develop Android applications. You can make, compile, and run Android apps without needing a heavy program like Eclipse or Android Studio.

## Installing

You must install these programs:

- Windows, probably.
- Python 3: https://www.python.org/downloads/
- Java Development Kit: https://www.oracle.com/technetwork/java/javase/downloads/index.html
- Android SDK command line tools: https://developer.android.com/studio/#command-tools

### Installing Android SDK

Android gets more and more complicated with time. Google fucked up the structure of their files. So, here's how to make it work, at least currently (2021-01-03).

1. Create a folder somewhere that will be the root of the Android SDK. Make a enviroment variable called "ANDROID_SDK_ROOT" and set it to that directory.
2. Create a folder called "cmdline-tools", and inside of it another folder called "latest".
3. The zip file you downloaded from the link above will contain a folder called "cmdline-tools". Move its contents (not the folder itself) to inside the "latest" folder you created.

Now the `sdkmanager.bat` file is in "%ANDROID_SDK_ROOT%\cmdline-tools\latest\bin\sdkmanager.bat". You can put this folder in your %PATH% if you want.

### Installing SDK manager packages

There's no way to just install the latest versions of some packages, so you must list them and find which is the latest version, and then install them:

`sdkmanager --list`
`sdkmanager "build-tools;<version>" "platform-tools" "platforms;android-<version>"`

The packages will be in their folders in %ANDROID_SDK_ROOT%.

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

`sdk` is the location of the Android SDK. If omitted, it will look in the ANDROID_SDK_ROOT environment variable by default.

`buildtool` is the build tools version to be used. If omitted, it will select the most recent one.

`platform` is the platform version to be used. If omitted, it will select the most recent one.

## The point of this

Who needs Android Studio anyway?

The point is for people to be able to make their apps in an open environment, allowing them to see and change any part of the process as they please. It's a midpoint between doing everything manually and using an IDE for everything. Come on, Eclipse is like 1 GB in size!

The build process of an Android app is complicated, but here I've simplified it. You can still look into the scripts to see what's going on, I tried to make it as neat as possible.

I don't wanna make an IDE with a GUI, but just simple tools that can help you out, not do literally everything for you. So this could be expanded by allowing automatic creation of layouts and activities, code linting, keystore creation, and much more. That's the plan, bro. Also I should probably be using AAPT2.