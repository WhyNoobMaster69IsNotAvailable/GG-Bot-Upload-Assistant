GG-BOT Auto ReUploader provides various commandline arguments that can be used to customize the auto uploaders process. These are mainly classified into 4 different groups.
- Commonly used arguments
- Less commonly used arguments
- Internal upload arguments

NOTE:
* If the **Value Needed** for any argument is **NO**, then only the argument flag needs to be provided in run command.
* If the **Value Needed** for any argument is **YES**, then the argument flag followed by the value for the argument also needs to be provided.

<br>

## Commonly Used Arguments
This category contains the list of arguments that are used commonly.

| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1 | **-t** or **--trackers** | Yes | Tracker(s) to upload to. Space-separates if multiple (no commas)| **-t BHD BHDTV NBL** |
| 2 | **-a** or **--all_trackers** | No | Select all trackers that can be uploaded to automatically | **--all_trackers** |
| 3 | **-anon** | No | Used to mark the upload to be anonymous. | **-anon** |

<br>

## Less Commonly Used Arguments
These are the list of arguments that can provide additional functionality to the upload assistant but on a day to day basis is almost never needed.
There are some rare cases where these arguments will come in use. Please see details below.
| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1 | **-disc** | No | If you are uploading a raw dvd/bluray disc you need to pass this arg | **-disc** |
| 2 | **-d or --debug** | No | Used for debugging. Writes debug lines to log file | **--debug** |
| 3 | **-mkt or --use_mktorrent** | No | Use mktorrent instead of torf (Latest git version only) | **--use_mktorrent** |
| 4 | **-fpm or --force_pymediainfo** | No | Force use PyMediaInfo to extract video codec over regex extraction from file name | **--force_pymediainfo** |
| 5 | **-ss or --skip_screenshots** | No | Override the configuration in config.env and proceed to upload without taking screenshots | **-ss** |
| 6 | **-let or --load_external_templates** | No | When enabled uploader will load external site templates from `./external/site_templates` location | **--load_external_templates** |
| 7 | **-tag or --tags** | Yes | Send custom tags to all trackers in addition to automatically resolved ones. | **--tags custom_tag_1 custom_tag_2** |

<br>

## Internal Upload Arguments
> These flags are applicable only if your account is already in a **Internal** class

| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1| **-internal** | No| Used to mark an upload as 'Internal' | **-internal** |
| 2| **-freeleech** | No| Used to give a new upload freeleech | **-freeleech** |
| 3| **-featured** | No| Mark the upload as featured | **-featured** |
| 4| **-doubleup** | No| Give a new upload 'double up' status | **-doubleup** |
| 5| **-tripleup** | No| Give a new upload 'triple up' status [XBTIT Exclusive] | **-tripleup** |
| 6| **-sticky** | No| Pin the new upload / Mark the upload as sticky | **-sticky** |

> Please note that the arguments `-doubleup` and `-tripleup` cannot be used together