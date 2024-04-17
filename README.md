# Rudimentary Backup

## Introduction
Rudimentary Backup is a Python console application meant as a simple, minimalistic solution for backup of personal data.

## Runtime Environment, Source Code Organization etc.
When implementing the project, I used Python 3.10, so this version or any higher version should work properly. Chances are older versions will work as well, but I have not tried. The application depends on these 3rd party modules:
* [pyaml](https://pypi.org/project/pyaml)
* [rich](https://pypi.org/project/rich)

## Configuration
The application is configured via a YAML file. The configuration defines the following settings:
* **Temporary working directory** is a directory where the backup process will create some temporary files. It is recommended to use a dedicated directory not used by other applications.
* **Destination directory** is a directory where the backup archives will be stored. Each backup will create a new subdirectory in this directory. The name of the subdirectory will be derived from the current date and time.
* **One or more targets**. Each target corresponds to a single source directory structure which will be archived to a single ZIP file. Each target can have an optional list of include or exclude patterns.  Include and exclude patterns are mutually exclusive - single target cannot have both include and exclude patterns. The patterns can be used to ensure that only a subset of files present in the source directory structure will be archived. The archive name is expected without file extension (.ZIP extension is automatically generated by the backup tool). At the end of the backup process, the created archive(s) will end up in a subdirectory of the specified destination directory. The name of the subdirectory will be dervied from the current date and time.

The following snippet illustrates the structure of the configuration YAML file.

```yaml
temp-dir: C:\\temp
destination-dir: D:\BACKUP
targets:
  - description: CV + related documents
    source-path: C:\Home\CV
    archive-name: CV
  - description: Keepass database
    source-path: C:\Home
    archive-name: Keepass
    include-patterns:
      - .+KeePassDB.kdbx$
  - description: Knowledge-Base
    source-path: C:\Home\Knowledge-Base
    archive-name: Knowledge-base
    exclude-patterns:
      - .+\.zip$
      - .+\.mp3$
```

The example above defines three targets:
* The first target will archive all files contained in the <code>C:\Home\CV</code> directory including subdirectories (the entire tree is archived recursively).
* The second target will archive all files containing in the <code>C:\Home</code> directory that match the specified include pattern. As for the first target, the entire tree is evaluated. However, only files matching the specified include pattern are archived in this case.
* The third target will archive all files containing in the <code>C:\Home\Knowledge-Base</code> directory that do not match the specified exclude pattern(s). As for the first target, the entire tree is evaluated. However, only files NOT matching any of the specified exclude patterns are archived in this case.

## How to Run the Application
If you start the application with the <code>-h</code> (or <code>--help</code>) switch, you will get the information about the usage (i.e. expected command line parameters). Example:
```
python -m backup.main --help
```

The following example illustrates how to start the application using a configuration file with the name <code>config.yml</code>:
```
python -m backup.main config.yml
```

The example above assumes you do not use the Python ZIP file. If you use the Python ZIP file, you can use the following command:
```
python rbackup.pyz config.yml
```
