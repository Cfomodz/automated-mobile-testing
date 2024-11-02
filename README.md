# Automated Mobile Testing - English Translation of the repo from which this was forked


## Project Description
This project aims to automate mobile application tests using Python, Appium, and Vysor.



## Technologies Used
- **Python:** Main project language
- **Appium:** Mobile testing automation framework
- **Unittest:** Python unit testing framework
- **ADB (Android Debug Bridge):** Tool for Android device interaction
- **Selenium**

## Project Structure
The project follows this structure:

- **`app_utils.py`:** Utility class for application interactions
- **`test_suite_muambator.py`:** File containing test methods/functions
- **`requirements.txt`:** Project dependencies list

## Prerequisites
- Make sure you meet the following prerequisites before running the tests:

- Code editor (Visual Studio Code) or an IDE (Pycharm)
- Python 3.x installed
- Appium configured
- Android SDK installed or Android Studio to obtain ADB
- Connected Android device and Vysor or configured emulator
- ADB configured and accessible via terminal
- Python libraries installed (check requirements.txt file)

## Environment Setup and Execution Instructions

1. **Python and Dependencies:**
   - Install Python on your system
   - Install dependencies using the command:
     ```
     pip install -r requirements.txt
     ```
2. **Appium and Settings:**
   - Install Appium on your machine
   - Configure necessary capabilities in the Appium configuration file
   - Start the Appium Server

3. **ADB (Android Debug Bridge):**
   - Install Android SDK or Android Studio to obtain ADB
   - Ensure ADB is available in your PATH

## Test Execution
- Execute the tests using the following command:

     ```bash
     python test_suite.py
     ```
  

## References
- [Appium](http://appium.io/): Official Appium documentation
- [Vysor](https://www.vysor.io/): Vysor official page
- [ADB (Android Debug Bridge)](https://developer.android.com/studio/command-line/adb): Official ADB documentation
