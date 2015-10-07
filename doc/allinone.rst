##################
CO2MPAS All-In-One
##################
A pre-populated folder with WinPython + CO2MPAS + Consoles for Windows.

Console Help
============

- You may freely move & copy this folder around.
  But prefer NOT TO HAVE SPACES IN THE PATH LEADING TO IT.

- To view & edit textual files, such as ``.txt``, ``.bat``, configuration-files
  starting with dot(``.``), you may use the "ancient" Window *notepad* editor,
  or better download and install **notepad++** from:
  http://portableapps.com/apps/development/notepadpp_portable
  (no admin-rights needed)

  Even better if you get accustomed to the "gem" file-manager of the '90s,
  **TotalCommander**, at http://www.ghisler.com/ (no admin-rights needed).
  Use the ``F3`` key-shortcut to view files.

- The Cygwin environment and its accompanying bash-shell is a much more
  powerful command-interpreter.  There are MANY tutorials and crash-courses
  for the fundamental bash-commands (`ls`, `pwd`, `cd`, etc), such as:
  http://www.ks.uiuc.edu/Training/Tutorials/Reference/unixprimer.html

  A more detailed guide is the following (just ignore the Linux-specific part):
  http://linuxcommand.org/lc3_lts0020.php



1st steps
=========

1. Start up the console of your choice using the appropriate bat-file:

    - Execute the ``cmd-console.bat`` to open a console with the **command-prompt**
      (`cmd.exe`) shell.
      Command-examples starting with the ``>`` character are for this shell.

    - Execute the ``bash-console.bat`` if you prefer the UNIX-like **bash-shell**
      environment.
      Command-examples starting with the ``$`` character are for this shell.

    - WHEN COPY-PASTING COMMANDS from the examples in the documents,
      DO NOT INCLUDE THE ``>`` OR ``$`` CHARACTERS.


2. Your *HOME* folder is ``CO2MPAS``.  You may run all example code inside
   this folder.

        - To move to your HOME folder when in *command-prompt*, type:

          .. code-block:: console

            > cd %HOME%

        - To move to your HOME folder when in *bash*, type:

          .. code-block:: console

            $ cd ~          ## The '~' char expands to home-folder.


3. View the files contained in your HOME folder, and read their description,
   provided in the next section:

        - In *command-prompt*, type:

          .. code-block:: console

            > dir
            07/10/2015  18:59    <DIR>          .
            07/10/2015  18:59    <DIR>          ..
            07/10/2015  17:35             6,066 .bashrc
            07/10/2015  18:58             2,889 .bash_history
            06/10/2015  18:09             1,494 .bash_profile
            10/09/2014  20:32               113 .inputrc
            06/10/2015  21:59    <DIR>          .ipython
            07/10/2015  17:27    <DIR>          .jupyter
            07/10/2015  18:25    <DIR>          .matplotlib
            06/10/2015  18:09             1,236 .profile
            06/10/2015  22:15                13 .python_history
            07/10/2015  00:33               688 README.txt
            07/10/2015  00:27    <DIR>          tutorial
                           7 File(s)         12,499 bytes
                           6 Dir(s)  319,382,626,304 bytes free

        - In *bash*, type:

          .. code-block:: console

            $ ls -l
            -r--rwxr--+ 1 user Domain Users 688 Oct  7 00:33 README.txt
            dr--rwxr--+ 1 user Domain Users   0 Oct  7 00:27 tutorial


3. To check everything is ok, run the following 2 commands and see if their
   output is quasi-similar:

        - In *command-prompt*, type:

          .. code-block:: console

            REM The python-interpreter that comes 1st is what we care about.
            > where python
            D:\co2mpas_ALLINONE-XXbit-v1.0.2\Apps\WinPython-XXbit-3.4.3.5\python-3.4.3\python.exe
            D:\co2mpas_ALLINONE-XXbit-v1.0.2\Apps\Cygwin\bin\python

            > co2mpas --version
            co2mpas-1.0.2 at D:\co2mpas_ALLINONE-XXbit-v1.0.2\Apps\WinPython-XXbit-3.4.3.5\python-3.4.3\lib\site-packages\co2mpas

        - In *bash*, type:

          .. code-block:: console

            > which python
            /cygdrive/d/co2mpas_ALLINONE-XXbit-v1.0.2/Apps/WinPython-XXbit-3.4.3.5/python-3.4.3/python

            > co2mpas --version
            co2mpas-1.0.2 at D:\co2mpas_ALLINONE-XXbit-v1.0.2\Apps\WinPython-XXbit-3.4.3.5\python-3.4.3\lib\site-packages\co2mpas

   In case of problems, the output from the above commands are valuable.


4. Follow the *Usage* instructions; they are locally installed at
   ``CO2MPAS/vX.X.X/co2mpas-doc-X.X.X/index.html`` or on the CO2MPAS-site:
   http://docs.co2mpas.io/  Just select the correct version.

   Demo files have been pre-generated for you, so certain commands might report
   that they cannot overwrite existing files.  Ignore the messages or use
   the `--force` option to overwrite them.

5. When a new CO2MPAS version is out, you may *upgrade* to it, and avoid
   re-downloading the *all-in-one* archive.  Read the respective sub-section
   of the *Installation* section from the documents.



File Contents
=============
::

    bash-console.bat                        ## Open a python+cygwin enabled `bash` console.
    cmd-console.bat                         ## Open a python+cygwin enabled `cmd.exe` console.
    co2mpas-Batch                           ## Run CO2MPAS in batch-mode, asking for Input/Output folders.
    co2mpas-env.bat                         ## Base script that sets environment variables for python+cygwin.

    CO2MPAS/                                ## User's HOME directory containing release-files and tutorial-folders.
    CO2MPAS/tutorial/input/                 ## Pre-generated input demo-files.
    CO2MPAS/tutorial/output/                ## Directory to store the results.
    CO2MPAS/tutorial/ipynbs/                ## IPython notebook(s); start with ``ipython notebook %HOME%\tutorial\ipynbs``.
    CO2MPAS/.*                              ## Configuration-files auto-generated by various programs, starting with dot(.).

    CO2MPAS/vX.X.X/co2mpas-doc-*/           ## CO2MPAS Reference Documentation (open ``index.html``).
    CO2MPAS/vX.X.X/co2mpas-src-*/           ## CO2MPAS sources.
    CO2MPAS/vX.X.X/co2mpas-*.whl            ## CO2MPAS wheel archive, to be installed with `pip` cmd.
    CO2MPAS/vX.X.X/pandalone-*.whl          ## Dependency of CO2MPAS, install it with `pip` cmd BEFORE co2mpas-wheel.
    CO2MPAS/vX.X.X/co2mpas_RelNotes-*.pdf   ## CO2MPAS Release notes.

    Apps/Cygwin/                            ## Unix-folders for *Cygwin* environment (i.e. bash).
    Apps/WinPython-XXbit-X.X.X.x/           ## Python environment (co2mpas is pre-installed inside it).
    Apps/Console2/                          ## A versatile console-window supporting decent copy-paste.
    Apps/graphviz-2.38/                     ## Graph-plotting library (needed to generate model-plots).

    README.txt                              ## This file, with instructions on this pre-populated folder.
