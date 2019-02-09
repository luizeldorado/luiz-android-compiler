# Python Android Compiler Scripts

Some scripts written in Python to help you compile Android projects into APKs. **They are not finished**, please look into the code before executing any of them, change it as needed.

You'll need to download the Android SDK in https://developer.android.com/studio/#command-tools. In the "Command line tools only" you'll find the download for your operating system. You will also need some other tools that can be downloaded using the [*sdkmanager*](https://developer.android.com/studio/command-line/sdkmanager) that comes with the SDK.

# How to use them

## Avaliable scripts

**android-build-apk** project package [--sdk SDK] [--buildtool BUILDTOOL] [--platform PLATFORM]

Builds an APK for the project, placing it in the /bin folder of the project.

**android-new-project** name package

Creats folder called name, with a project with the *package* folder structure.

**android-align-apk** apk [--sdk SDK] [--buildtool BUILDTOOL]

Aligns an APK, making it smaller.

**android-sign-apk** apk keystore [--sdk SDK] [--buildtool BUILDTOOL]

Signs an APK with the keystore file.

**android-launch** apk [--sdk SDK] [--buildtool BUILDTOOL]

Installs and launches an APK to an ADB connected device.

## Argument explanation

**project**: Folder where the whole project is on. Must follow a specific format, like the one created by using android-new-project.

**package**: Currently, it only supports one package per project. Use the dot separated format, e.g. *com.example.hellothere*.

**apk**: APK file location.

**--sdk SDK**: By default, the scripts will use the ANDROID_SDK_HOME enviroment variable for the location of the Android SDK. Using --sdk, you can manually select the location.

**--buildtool BUILDTOOL**: Folder inside the 'build-tools' directory with the version you want to use. The name is generally the version, e.g. "28.0.3".

**--platform PLATFORM**: Folder inside the 'platforms' directory with the API level you want to use. The name is generally 'android-' plus the API level number, e.g. "android-28".

# Objective

Who needs Android Studio anyway?

The point is for people to be able to make their apps in an open enviroment, allowing them to see and change any part of the process as they please. It's a mid point between doing everything manually and using an IDE for everything. Come on, Eclipse is like 1 GB in size!