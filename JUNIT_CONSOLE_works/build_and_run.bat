del Home\Egor\TestRunner2.class Home\Egor\TestAssertions.class Test.jar

javac -cp junit-4.10.jar;C:\JUNIT_WORKSPACE\Home\Egor Home\Egor\TestRunner2.java Home\Egor\TestAssertions.java || pause && exit \b

::java -cp junit-4.10.jar;. Home.Egor.TestRunner2

jar cvfm Test.jar Manifest.mf Home\Egor\TestAssertions.class Home\Egor\TestRunner2.class || pause && exit \b
java -jar Test.jar

::YOUR_CMD || pause && exit \b
pause