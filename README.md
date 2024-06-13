
# Agribot

The agricultural robot simulator is a modified version or the CARLA simulator made to test the code meant to run on the physical robot in a virtual space. 
The code for this project should be contained in an SSD stored in the lab, though if it gets lost the below details how to recreate everything from scratch.

## How To Run
1. Navigate into *F:\carla\Unreal\CarlaUE4* and right-click the *CarlaUE4.uproject* file. Select "Switch Unreal Engine Version...".
2. A dialogue prompt should open up. Click on the three dots next to the dropdown menu, then select the folder *F:\UnrealEngine*.
3. Press "OK" and wait for the project files to finish being generated.
4. Double click the *CarlaUE4.uproject* file and Unreal Engine should open with the agricultural simulator scene already open.
5. Press the  "Play" button in the top right. Leave the scene playing for the time being.
6. Open a terminal and navigate to *F:\carla\PythonAPI\examples*
7. Run the command `python farm_robot.py`

## Preinstallations
The following details how to get the simulator set up from scratch in case the code in the SSD breaks, along with all potential errors that may come up during setup.
Follow the steps detailed below and avoid using the official documentation for Windows, as it is currently very outdated.
> **Note:** The following steps are meant for a **Windows** machine. If you are running **Linux** then the setup process is detailed in CARLA's own official documentation. https://carla.readthedocs.io/en/latest/build_linux/
> Differences between the Linux documentation and setting up this specific variant of it will be listed and the end.
### Potentially required:
If the project files for some reason do not work, then the following will be required to remake the project from scratch. It is recommended to download them regardless though just in case.

**CMake:** The most recent version will suffice. The minimum is 3.15
**Git**: This is for if you need to pull the project from the original CARLA repository. This shouldn't be neccessary however its still good to have as a backup.
**Make**: Same as the above, though if needed you **must** have version **3.81**.
**7zip**: Any version will suffice

### Required:
**Python**: **You must have Python x64 3.8.10.** No other version of python will work properly.
**Visual Studio:** The most recent of Visual Studio should work. Use the Community version of it as its free. You will need the addition elements selected when install Visual Studio:

 - Include the most recent version of the **Windows 10** SDK. 
 - Desktop development with C++
 - .NET desktop development

