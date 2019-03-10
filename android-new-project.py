import argparse
import os, sys

parser = argparse.ArgumentParser(description='Creates new project on a folder name')
parser.add_argument('name', help='app name and folder')
parser.add_argument('package', help='package name')

def main(args):

	args = parser.parse_args(args)

	if os.path.exists(args.name):
		exit()

	package_dir = args.package.replace(".", "\\")

	print('Making directories...')

	os.makedirs(args.name)

	os.makedirs(args.name+R"""\src\\"""+package_dir)
	os.makedirs(args.name+R"""\obj""")
	os.makedirs(args.name+R"""\bin""")
	os.makedirs(args.name+R"""\res\layout""")
	os.makedirs(args.name+R"""\res\values""")
	os.makedirs(args.name+R"""\res\drawable""")
	os.makedirs(args.name+R"""\libs""")

	print('Making '+R"""src\\"""+package_dir+R"""\MainActivity.java...""")

	with open(args.name+R"""\src\\"""+package_dir+R"""\MainActivity.java""", 'w') as f:
		f.write(R"""package """+ args.package +R""";

	import android.app.Activity;
	import android.os.Bundle;

	public class MainActivity extends Activity {
		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			setContentView(R.layout.activity_main);
		}
	}""")

	print('Making '+R"""res\values\strings.xml...""")

	with open(args.name+R"""\res\values\strings.xml""", 'w') as f:
		f.write(R"""<resources>
		<string name="app_name">"""+ args.name +R"""</string>
		<string name="hello_world">Hello, world!</string>
	</resources>""")

	print('Making '+R"""res\layout\activity_main.xml""")

	with open(args.name+R"""\res\layout\activity_main.xml""", 'w') as f:
		f.write(R"""<RelativeLayout
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

	print('Making AndroidManifest.xml...')

	with open(args.name+R"""\AndroidManifest.xml""", 'w') as f:
		f.write(R"""<?xml version='1.0'?>

	<manifest
		xmlns:a='http://schemas.android.com/apk/res/android'
		package='"""+ args.package +R"""'
		a:versionCode='1'
		a:versionName='1'
		>
		<application a:label='"""+ args.name +R"""'>
			<activity a:name='"""+ args.package +R""".MainActivity'>
				<intent-filter>
					<category a:name='android.intent.category.LAUNCHER'/>
					<action a:name='android.intent.action.MAIN'/>
				</intent-filter>
			</activity>
		</application>

	</manifest>""")

	print('Done.')

if __name__ == "__main__":

	main(sys.argv)