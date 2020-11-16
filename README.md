# kenwood_copy
This script will copy music from a source directory to a USB drive using a folder structure compatible with a Kenwood DNX691HD car stereo (other models will likely work too). This is helpful for large music libraries that would otherwise break compatibility due to the number of folders (especially) and files.

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
WARNING: All data in the target directory except exluded folders will be deleted, and everything from the source with matching extensions will be copied over.
```
------------- Kenwood Music File Copy Script -------------

Source Directory is: Z:/Music
Target Directory is: U:/

Please wait while the source directory is scanned for files...Done (584 found)

This will delete all data from the target directory (except excluded folders).
Are you sure you want to proceed? (Y/N):
Deleting all data from the target directory...Done
Copied 1/584 0.17%
        from: Z:/Music/Artist1/Album/01 - Song.flac
        to:   U:/1/01 - Song.flac
...
Copied 584/584 100.00%
        from: Z:/Music/Artist7/Album/15 - Song.flac
        to:   U:/3/15 - Song.flac
Done! Total time elapsed: 0:08:46.321000
```
The final folder structure will look like this:
!(example_folders.png?raw=true "Title")

While it's not good for manually browsing files, it doesn't matter because the Kenwood unit will read the tags from the files and organize using it's own UI.
