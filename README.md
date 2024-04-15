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
* **One or more targets**.

The following snippet illustrates the structure of the configuration YAML file.

```yaml
temp-dir: C:\\temp
destination-dir: D:\BACKUP
targets:
  - description: CV + related documents
    source-path: C:\Home\CV
    archive-name: CV
  - description: Financial Excel + related documents
    source-path: C:\Home\Financial
    archive-name: Financial-Documents
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

## How to Run the Application

```
python ...
```