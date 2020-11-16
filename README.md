# kenwood_copy
This script will copy music from a source directory to a USB drive using a folder structure compatible with a Kendwood DNX691HD car stereo. This is helpful for large music libraries that would otherwise break compatibility due to the number of folders and files.

Per the [specifications](https://www.kenwood.com/cs/ce/audiofile/index.php?model=DNX691HD&lang=english):

| Limitation of structure for files and folders| USB |
| ----------- | ----------- |
| <b>Type</b> | <b>Limit</b> |
| Maximum number of folder layers | 8 |
| Maximum number of folders (per device) | 255 |
| Maximum number of files (per folder) | 255 |
| Maximum number of files (per device) | 65025 |
| Maximum number of files per playlist | 7000 |

Usage is simple, just set the source_dir, target_dir, and music_extensions as desired:
```
source_dir = "SOURCE_DIR"
target_dir = "TARGET_DIR"
music_extensions = [".flac"] # List of allowed extensions
```
All data in the target directory will be deleted and everything from the source directory with matching extensions will be copied over.

Final folder structure will look like this:

Not good for manually browsing, but ok for the stereo since it reads the ID3 tags and organizes the music by itself.
