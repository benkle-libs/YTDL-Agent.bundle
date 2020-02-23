# Youtube-DL Agent

This agents will load metadata for video downloaded from youtube. Unlike
[ZeroQI's better known plugin](https://github.com/ZeroQI/YouTube-Agent.bundle) however, they don't query youtube directly,
relying instead on the metadata files created by `youtube-dl --write-info-json`, thus allowing them to work for videos that
are not online anymore, or where actually downloaded from a different source (like vimeo).

You can even write the metadata files yourself, to override bad matches or really obscure movies! 

## Installation

Instructions for installing a 3rd party Plex agent can be found on the Plex support website:
[How do I manually install a plugin?](https://support.plex.tv/articles/201187656-how-do-i-manually-install-a-plugin/)

## Usage

You can either enable the agents as additional providers under _Settings ⇒ Agents_, or select the agent specifically when
correcting the match. It's called _Youtuble-DL Movies_ for movie entries and _Youtube-DL Shows_ for TV shows.

## Naming

Files for individual episodes and movies must lay side by side with the video files and share the basename with the
extension replaced by `info.json`, like this:

```
Requiem 2019 (2011)/
Requiem 2019 (2011)/Requiem 2019 (2011).mp4
Requiem 2019 (2011)/Requiem 2019 (2011).info.json
```

The TV show agent also support special files for shows and seasons. Season files should either be `Season##.info.json` or
simply `season.info.json` and lay within the seasons directory.
Show files must be either `SHOW_TITLE.info.json` or `show.info.json`.

```shell script
KaBlam!/
KaBlam!/KaBlam!.info.json # this will get preference
KaBlam!/show.info.json
KaBlam!/Season 01/
KaBlam!/Season 01/Season 01.info.json # this will get preference
KaBlam!/Season 01/season.info.json
```

## Faking it

These agents allow you to fake metadata. For that you'll need a JSON file with the following keys:

```json
{
    "title": "",
    "name": "",
    "original_title": "",
    "duration": 0,
    "summary": "",
    "originally_available_at": "20200101",
    "year": 2020,
    "extractor": "",
    "id": ""
}
```