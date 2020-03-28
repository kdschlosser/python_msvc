# pyMSVC

A fairly stupid proof build environment setup for compiling c extensions using pythons distutils or setup tools.

I created this module because distutils does not do a good job at setting up a Windows build environment.
Distutils relies on static paths for the MSVC compiler It does not detect Visual Studio Build tools installations. And 
the largest problem with it is that it uses the vcvars*.bat files included with the compiler. It runs a subprocess 
takes a snapshot of the computers environment then runs vcvarsall and takes another snapshot of the environment. It 
then compares the before and after and stores the differences between the 2. Now this would be a fantastic approach if
Microsoft had made the vcvars*.bat files in a manner that would et up a correct build environment. There have been known issues
using these files in the past.

The single largest problem with the vcvars files is NONE of them check to see if any of the components actually exist.
We all know how good applications are when they get uninstalled. They do a very thorough job of removing all traces 
from the registry.. NOT. Microsoft is the biggest offender of this.

My system does not use the vcvars* files the information is obtained from the registry. The paths that are obtained are 
checked to ensure they exist.

Setuptools is an improvement over distutils but still relies on those vcvars* files.

`pyMSVC.Environment(strict_visual_c_version=None, minimum_visual_c_version=None)`

If both strict_visual_c_version and minimum_visual_c_version are None that the program runs as a free for all and 
whichever installation it finds first is the winner.

Both parameters accept either None or a float that is the version number fo the MSVC compiler that you want to use.

* 9.0 Visual Studio 2008
* 10.0 Visual Studio 2010
* 11.0 Visual Studio 2012
* 12.0 Visual Studio 2013
* 14.0 Visual Studio 2015
* 14.1x Visual Studio 2017
* 14.2x Visual Studio 2019

Python recommends that any extensions that are compiled on Windows should be compiled with the same MSVC version
that was used to compile Python. This is due to incompatibilities in the common runtime language between the 
compiler versions. You may or may not experience any issues if you do not use the ame compiler version. Your extension 
would have to use that portion of the CLR in order to have an issue. This is why it is a recommendation.


Python versions 3.5, 3.6, 3.7, 3.8 use any of the MSVC compiler versions beginning with 14.0
Python versions 3.3, 3.4 use MSVC compiler version 10.0
Python versions 2.6, 2.7, 3.0, 3.1, 3.2 use MSVC compiler version 9.0

If you would like to have the above done for you automatically and have the environment set up. Yuo can use 
`environment = pyMSVC.setup_environment()`. This will rise an exception if the msvc version that is needed based on the 
python version is not found. This will set up the environment for you as well without the need for any additional steps.

I added the minimum_visual_c_version argument so you can specify a minimum compiler version to use. You may have code 
that will compile using MSVC 10.0 but will fail if compiled using MSVC 9.0.

So to sum it up.
strict_visual_c_version you will use if only a specific compiler version is to be used to compile.
minimum_visual_c_version you will use if compiler versions that are the same or higher as the one specified are ok to use 

Here is an example of using pyMSVC to only set up the build environment.

    import os
    import pyMSVC

    environment = pyMSVC.Environment()
    print(environment)
    
    os.environ.update(environment)


You will want to set up the environment before you import distutils or setuptools.

Now onto some of the goodies. This module provides access to a bucket load of information. 
    
    
Here are the properties and attributes available


###### class ***Environment***
* ***machine_architecture***: Windows architecture x86 or x64
* ***platform***: x86 or x64, if running Windows x86 this will be x86. if running Windows x64 and Python x86 this will return x86.    
* ***build_environment***: returns a `dict` of the environment
* ***visual_c***: instance of VisualCInfo
* ***visual_studio***: instance of VisualStudioInfo 
* ***windows_sdk***: instance of WindowsSDKInfo
* ***dot_net***: instance of NETInfo
* ***python***: instance of PythonInfo


###### class ***NETInfo***
* ***version***: .NET version based on the platform architecture
* ***version_32***: 32bit .NET version
* ***version_64***: 64bit .NET version 
* ***directory***: directory to .NET based on preffered bitness
* ***directory_32***: 32bit .NET directory 
* ***directory_64***: 64bit .NET directory
* ***preferred_bitness***: .NET bitness
* ***netfx_sdk_directory***: .NET FX SDK path
* ***net_fx_tools_directory***: .NET FX tools path using preffered bitness
* ***net_tools***: .NET tools paths 
* ***executable_path_x64***: 64bit executable path
* ***executable_path_x86***: 32 bit execitable path
* ***lib***: library paths
   
    
###### class ***WindowsSDKInfo***
* ***extension_sdk_directory***: Extension SDK path
* ***ucrt_version***: UCRT version
* ***ucrt_sdk_directory***: Path to the UCRT libraries
* ***bin_path***: BIN path
* ***lib***: paths to the libraries.
* ***type_script_path***: path to TypeScript
* ***include***: include paths
* ***sdk_lib_path***: 
* ***windows_sdks***: Acceptable SDK versions based on compiler version
* ***version***: SDK version
* ***sdk_version***: Actual SDK version
* ***directory***: path to the Windows SDK


###### class ***VisualStudioInfo***
* ***install_directory***: installation directory
* ***dev_env_directory***: directory where devenv.exe is located
* ***common_tools***: path to tools
* ***common_version***: example - 2019 
* ***uncommon_version***: example - 16.4.5
* ***version***: VS major version


###### class ***VisualCInfo***
* ***f_sharp_path***: FSharp path
* ***ide_install_directory***: path to Visual C ide
* ***install_directory***: path to Visual C
* ***version***: Visual C version
* ***tools_version***: Visual C tool version
* ***toolset_version***: Visual C Toolset Version - v141, v140, v120 etc...
* ***msvc_dll_version***: MSVC dll version
* ***msvc_dll_path***: Location of the MSVC dll
* ***tools_redist_directory***: Visual C redist path
* ***tools_install_directory***: Visual C tools installation folder
* ***msbuild_version***: MSBuild version
* ***msbuild_path***: MSBuild path
* ***html_help_path***: HTML Help path
* ***atlmfc_lib_path***:  ATLMFC library path
* ***lib***: Visual C library path
* ***atlmfc_path***: ATLMFC path 
* ***atlmfc_include_path***: ATLMFC include path
* ***include***: Visual C include folders


###### class ***PythonInfo***
* ***architecture***: x86 or x64
* ***version***: Python version
* ***dependency***: library name.. Python27.lib
* ***includes***: include paths
* ***libraries***: library paths


Visual Studio 2019 has a whole new system for package installation. It no longer stores the information in the registry 
for installed packages. I will be writing a ctypes binder so I will be able to call the API functions needed in order 
to collect this information.