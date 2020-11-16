# kenwood_copy
This script will copy music from a source directory to a USB drive using a folder structure compatible with a Kendwood DNX691HD car stereo (other models will likely work too). This is helpful for large music libraries that would otherwise break compatibility due to the number of folders and files.

Per the [specifications](https://www.kenwood.com/cs/ce/audiofile/index.php?model=DNX691HD&lang=english):

| Limitation of structure for files and folders| USB |
| :--- | ---: |
| <b>Type</b> | <b>Limit</b> |
| Maximum number of folder layers | 8 |
| Maximum number of folders (per device) | 255 |
| Maximum number of files (per folder) | 255 |
| Maximum number of files (per device) | 65025 |
| Maximum number of files per playlist | 7000 |

Usage is simple, just set these variables as required:
```
source_dir = "SOURCE_DIR"
target_dir = "TARGET_DIR"
music_extensions = [".flac"] # List of allowed extensions
del_exclude_dirs = ["Video"] # List of directories in the TARGET folder to exclude from deletion

# Leave empty to copy everything from the source_dir, otherwise, specify a list of artists sub-folders to copy
# Note: Larger libraries will choke the Kenwood scan process and may take a long time to resume playback.
artists = ["Artist1", "Artist2"]
```
Then run with:
```
python kenwood.py
```
All data in the target directory except exluded folders will be deleted, and everything from the source with matching extensions will be copied over.

The final folder structure will look like this:

While it's not good for manually browsing files, it doesn't matter because the Kenwood unit will read the tags from the files and organize using it's own UI.
