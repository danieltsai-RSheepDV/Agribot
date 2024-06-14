
# Agribot

The agricultural robot simulator is a modified version or the CARLA simulator made to test the code meant to run on the physical robot in a virtual space. 
The code for this project should be contained in an SSD stored in the lab, though if it gets lost the below details how to recreate everything from scratch.

# How To Run

## Prerequisites

**Python**: **You must have Python x64 3.8.10.** No other version of python will work properly. If you have other installations of python on your computer, it is highly reccomended you remove them. This includes variants of python, mamba, anacoda, etc. 

> **Note:** If you are able to create a new conda environment with Python 3.8.10 then uninstalling other python versions won't be neccessary. If you are however, ensure that all the following steps are run inside the conda environment. 

After installing python, run the following commands:

```
pip3 install --upgrade pip
pip3 install --user setuptools
pip3 install --user wheel
```

All these commands should run without error.

## Instructions

1. Navigate into *F:\carla\Unreal\CarlaUE4* and right-click the *CarlaUE4.uproject* file. Select "Switch Unreal Engine Version...".
2. A dialogue prompt should open up. Click on the three dots next to the dropdown menu, then select the folder *F:\UnrealEngine*.
3. Press "OK" and wait for the project files to finish being generated.
4. Double click the *CarlaUE4.uproject* file and Unreal Engine should open with the agricultural simulator scene already open.
5. Press the  "Play" button in the top right. Leave the scene playing for the time being.
6. Open a terminal and navigate to *F:\carla\PythonAPI\examples*
7. Run the command `python farm_robot.py`

This will open up a window showing to perspectives of cameras on the robot. Movement can be controlled via the WASD keys. This file will be where AgroNav will be run from, and the image data is obtained from the ```process_img`` function. The details on what the CARLA methods do and how to add cameras are detailed in the [CARLA documentation](https://carla.readthedocs.io/en/latest/).

Within Unreal Engine, the top right of the Scene View are two sliders. These two sliders affect the row gap size and density of the crops in the scene.

# Building From Sratch

The following details how to get the simulator set up from scratch in case the code in the SSD breaks, along with all potential errors that may come up during setup.
Follow the steps detailed below and avoid using the official documentation for Windows, as it is currently very outdated.

> **Note:** The following steps are meant for a **Windows** machine. If you are running **Linux** then the setup process is detailed in CARLA's own official documentation. https://carla.readthedocs.io/en/latest/build_linux/
> Differences between the Linux documentation and setting up this specific variant of it will be listed and the end.

## Prerequisites:

> **Note:** Make sure to run the prerequesites in the How To Run section before moving on.

**CMake:** The most recent version will suffice. The minimum is 3.15

**Git**: Any version will suffice.

**Make**: You **must** have version **3.81**, no other version will work

**7zip**: Any version will suffice.

**Visual Studio:** The most recent of Visual Studio *should* work. Use the Community version of it as its free. You will need the addition elements selected when install Visual Studio:
 - Include the most recent version of the **Windows 10** SDK. 
 - Desktop development with C++
 - .NET desktop development

## Building Carla's Unreal Engine

Carla uses its own, modified version of Unreal Engine 4. This may change in the future however the Agribot simulator will be using the current, UE4 version.

1. **Make sure you have an Unreal Account linked to your Github account.** If you do not have an Unreal account, then you will need to make one. If this step isn't done then you will not have permission to pull the Unreal Engine source code. Details on how to do so [are detailed here](https://www.unrealengine.com/en-US/ue-on-github).
2. Clone the Carla Unreal Engine repository \(https://github.com/CarlaUnreal/UnrealEngine.git\). The Carla documentation uses git commands to do so, though using Github Desktop also works.
3. Navigate into the repository in command prompt, then run the following commands
```
Setup.bat
GenerateProjectFiles.bat
```
4. Open the UE4.sln file in the UnrealEngine repository using Visual Studio.

5. In the top left corner in the Build Bar, there will be three dropdown menus. Set the first one to "Development Editor", the second one to "Win64", and the third one to "UnrealBuildTool".

6. Right click UE4 in the solution explorer and press on the Build option. If there are errors, attempt rebuilding the project by right clicking UE4, Clean, then scrolling down to UnrealLightmass, right clicking and pressing clean, then building UE4 again. If issues still persist, then it is best to delete the repository and restart from step 2. Building does take a while, be prepared for this to take a couple of tries.

7. Scroll down in the solution explorer and right click UnrealLightmass, then press Build.

8. Once Complete, test that the engine works properly by navigating to ```Engine\Binaries\Win64\UE4Editor.exe``` in the repository folder. 

9. Create and account for and install [Quixel bridge](https://quixel.com/). By linking your Unreal Account to your Quixel account, you will be able to access the software for free.

10. Open the Bridge program, click on edit, export settings. Set the export target to **Unreal Engine**, the version to **4.26**, the plugin location to ```/Engine/Plugins``` inside the UnrealEngine repository, and Defualt project to ```Unreal/CarlaUE4``` in the carla repository. Finally, press install.

> **Note**: Install Quixel bridge may require rebuilding Unreal Engine. Simply clean, then build the engine again.

## Building Carla Simulator

A majority of the steps will be indentical to setting up the CARLA simulator, however extra files will need to be inserted into the project for the Agricultural Robot simulator.

1. Clone the Carla Unreal Engine repository \(https://github.com/carla-simulator/carla\). The Carla documentation uses git commands to do so, though using Github Desktop also works.

2. Open an **x64 Native Tools Command Prompt for VS 2022**. This is findable by searching via the windows search bar (clicking the windows button in the bottom left then typing the name of the program)

3. Navigate to the CARLA repository, then run the following command
```
Update.bat
```
4. Set an environment variable with the name ```UE4_ROOT``` and set the path to it to the Unreal Engine respository root folder.

5. Run the following commands. 
```
make PythonAPI
make launch
```

6. Navigate in file explorer from within the CARLA repository to ```\Unreal\CarlaUE4\Content\Carla\Maps```. Copy and paste the contents of the UEAssets folder in this respository, to there.

7. Navigate in file explorer from within root CARLA repository folder to ```\PythonAPI\examples```. Copy and paste the contents of the pythonAPI folder in this repository to there.

8. From the Bridge app seperate from Unreal Engine, install the Castor Oil Plant and potting soil assets. Resolve any dependencies in the ```\Unreal\CarlaUE4\Content\Carla\Maps\FarmSim``` folder using the downloaded assets.