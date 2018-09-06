# python_msvc
Python Visual C build helper.

This module is designed to take the complexity out of building C
extensions in Python. I personally found the setuptools.msvc module
to complex for my liking, and it also has quite a few shortfalls.

Support list:
Visual C >= 9.0,
Visual Studio >= 2008,
Python >= 2.6 (x86 or x64)

Requirements:
setuptools >= 40.2.0


OK so here is how to use this module.

if building a standalone solution

    import os
    from subprocess import Popen, PIPE
    from python_msvc import Environment

    solution_src_path = r'C:\some_solution_source_path'
    solution_dst_path = r'C:\some_solution_destination_path'

    env = Environment()

    for key, value in env.items():
        os.environ[key] = value

    solution, build = env.update_solution(
        solution_src_path,
        solution_dst_path
    )

    build_command = env.get_build_command(solution)

    proc = Popen(build_command, stdout=PIPE, stderr=PIPE)

    if env.py_version[0] == '3':
        dummy_return = b''
    else:
        dummy_return = ''

    while proc.poll() is None:
        for line in iter(proc.stdout.readline, dummy_return):
            if line:
                print(line)


if building a C extension using distutils or setuptools

    import os
    from setuptools import setup, Extension
    from python_msvc import Environment
    env = Environment()

    for key, value in env.items():
        os.environ[key] = value

    extension = Extension(
        name='example',
        sources=['path_to_sources_files'],
        include_dirs=env.py_includes,
        define_macros=[],
        libraries=env.py_libraries,
        extra_objects=[env.py_dependency],
        extra_compile_args=[],
        extra_link_args=[],
        language='c++'
    )

    setup(
        script_args=['build_ext'],
        version='0.0.0',
        name='example',
        description='example',
        verbose=1,
        ext_modules=[extension],
    )

it's as simple as that. I really don't think It could be any easier.
It even handles updating the solution and project files for you. and
gives you the commands that can be passed directly to subprocess.Popen.

There are 2 constructor parameters so you can adjust the build environment

Environment(strict_compiler_version=False, dll_build=False)

I have found that not all projects require you to build using the same
compiler that python was built with. but in the event you do have
issues because of this setting  strict_compiler_version to True will
make sure the compiler versions match.  if they don't a runtime error
gets raised.

dll_build is used with standalone builds of a solution. it changes the
build configuration. there are 4 build configurations in a solution

* Release
* ReleaseDLL
* Debug
* DebugDLL

I test the python executable to see if it has _d at the end of the
filename, if it does it will use Debug or DebugDLL otherwise
Release or ReleaseDLL.

if you want to print out the build environment

    from python_msvc import Environment
    print(Environment())


## Properties

  * msvc_dll_version
  * msvc_dll_path
  * machine_architecture
  * architecture
  * platform
  * platform_toolset
  * py_architecture
  * py_version
  * py_dependency
  * py_includes
  * py_libraries
  * target_framework
  * framework_dir_32
  * framework_dir_64
  * framework_version_32
  * framework_version_64
  * configuration
  * min_visual_c_version
  * visual_c_version
  * msbuild_version
  * tools_install_path
  * build_environment
  * windows_sdks
  * target_platform
  * windows_sdk_version
  * target_platform_path
  * tools_version
  * visual_c_path
  * msbuild_path


## Methods

  * get_clean_command(self, solution)
  * get_build_command(self, solution)
  * update_solution(self, src, dst)





