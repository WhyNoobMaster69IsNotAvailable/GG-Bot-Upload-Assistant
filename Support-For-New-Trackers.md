1. Create a new Feature Request Issue and mention the tracker details.
2. Create the site template and raise a pull request.
3. Use templates externally with the uploader.

## 1. Create Issue
Create a new [Issue](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/issues/new) with template as `Feature Request`.

## 2. Raise PR
- Clone this repo
- Create the template and validate that uploader is working as expected
- Raise a PR

### What all should you change to add support for new tracker?

To support a new tracker the following files and contents needs to be updated
1. README.md => Add the newly supported details to the supported trackers table
2. samples/assistant/config.env => Add the environment variable entry for the new tracker. This will help users get the latest config.env and uplaoder also uses to validate the active environment variable.
3. samples/reuploader/reupload.config.env => Same as above but for the Auto Reuploader
4. parameters/tracker/acronyms.json => Add an entry to this json with the acryonym and expansion.
5. parameters/tracker/api_keys.json => Add an entry to this json with the api key format.
6. site_templates/new_tracker.json => Create this file and fill the details.

> Notes:
> In acronym you'll specify a 3 letter `acronym` => `tracker_name`. The template file created in `site_templates` should be `tracker_name.json`
> The entry added to api_keys.json should be `<acronym>_api_key`. The same value should be present in both config.env files with all caps

Consider you want to add support for a new tracker named Seedpool. The contents of the config files should be as follows.
- New template in `site_templates` with the name `seedpool.json`
- An entry in `api_keys.json` with the following value: `spl_api_key`
- Entry in `acronyms.json` as follows => `"spl": "seedpool"`
- Entries in config.env as follows
> SPL_API_KEY=# Fill Api Key
> SPL_ANNOUNCE_URL=https://seedpool.org/announce/<TRACKER_PASS_KEY>

## 3. Use Templates Externally
> :warning: **There will be no support provided for externally loaded templates** :warning:

Another way to add support for external trackers is to create the template and load them to gg-bot uploaders as external templates.
Starting from `v3.0.4`, ggbot uploaders have a new argument `-let` or `--load_external_templates` which can be provided at runtime to instruct the uploaders to load external templates.
> The templates created should be valid. Invalid templates will be ignored by the uploaders.

### Steps in loading templates as external templates
 - Create the template file for the tracker that you want to support.

 > Note that this MUST be a valid template and must conform to the [schema/site_template_schema.json](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/blob/master/schema/site_template_schema.json).

 - You must also create a `tracker_to_acronym.json` file, which contains the mapping for the tracker and its acronym

 > Refer to the acronyms parameter file [parameters/tracker/acronym.json](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/blob/master/parameters/tracker/acronyms.json). The `tracker_to_acronym.json` mapping should be the exact opposite of this file.

<details><summary>tracker_to_acronym.json sample</summary>
if you have two tracker templates
- external.json
- randomsite.json

Then the `tracker_to_acronym.json` should look something like this
```{
    "external": "extn",
    "randomsite": "rds"
}
```
Here
- `external` is the name of the tracker, and `extn` is its acronym.
- `randomsite` is the name of the tracker, and `rds` is its acronym.
</details>

- Once the template and acronym mapping files have been created, create a new folder named `external` in the root of the project.
> When using docker setup, then folder needs to be created in the folder where you have the `config.env` / `reupload.config.env`
- Folder structure for `external`
    - external
        - site_templates
            - external.json
            - randomsite.json
        - tracker
            - tracker_to_acronym.json
 - Run the uploader as usual, but this time add an extra argument `-let` or `--load_external_templates` to the run command.
 - When using the docker setup, once the folder `external` has been created, it needs to be mapped inside the container. The below run command shows an example for mapping the `external` directory and providing the argument
```
docker run --rm -it
    -v {YOUR_MEDIA_LOCATION}:/data
    -v external/:/app/external
    --env-file config.env
    noobmaster669/gg-bot-3.0.4 -t TSP-p "/data/YOUR_FILE_OR_FOLDER" <ADDITIONAL_ARGUMENTS> --load_external_templates
```