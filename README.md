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