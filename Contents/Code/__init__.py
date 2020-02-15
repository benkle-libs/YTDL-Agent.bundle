import os


def Start():
    HTTP.CacheTime = CACHE_1MONTH
    HTTP.Headers[
        'User-Agent'] = 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.54'
    HTTP.Headers['Accept-Language'] = 'en-us'


class YoutubeDLMovieAgent(Agent.Movies):
    name = 'Youtube-DL Movies'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = [
        'com.plexapp.agents.localmedia',
        'com.plexapp.agents.opensubtitles',
        'com.plexapp.agents.plexthememusic'
    ]
    contributes_to = [
        'com.plexapp.agents.themoviedb',
        'com.plexapp.agents.imdb',
        'com.plexapp.agents.none'
    ]

    def search(self, results, media, lang, manual):
        filename = String.Unquote(media.filename)
        infoFilename = os.path.splitext(filename)[0] + '.info.json'
        if os.path.exists(infoFilename):
            infoData = JSON.ObjectFromString(Core.storage.load(infoFilename))
            ytdl_id = infoData['extractor'] + '-' + infoData['id']
            metadata = MetadataSearchResult(
                id=ytdl_id,
                name=media.name,
                year=int(infoData['upload_date'][:4]) if 'upload_date' in infoData else None,
                score=infoData['average_rating'] if 'average_rating' in infoData else 99,
                lang=lang
            )
            Log.Debug(dir(metadata))
            results.Append(metadata)

    def update(self, metadata, media, lang, force):
        Log.Debug('Updating %s' % metadata.id)
        filename = String.Unquote(media.items[0].parts[0].file)
        infoFilename = os.path.splitext(filename)[0] + '.info.json'
        try:
            infoData = JSON.ObjectFromString(Core.storage.load(infoFilename))
        except:
            Log('Could not retrieve data from YouTube for: %s' % metadata.id)
            infoData = None
        if infoData:
            metadata.title = infoData['fulltitle']
            metadata.original_title = infoData['fulltitle']
            metadata.duration = infoData['duration']
            metadata.summary = infoData['description']
            date = Datetime.ParseDate(infoData['upload_date'])
            metadata.originally_available_at = date.date()
            metadata.year = date.year
            metadata.rating = infoData['average_rating']*2 if 'average_rating' in infoData else 10
            metadata.directors.clear()
            try:
                meta_director = metadata.directors.new()
                meta_director.name = infoData['uploader'] if 'uploader' in infoData else infoData['extractor']
            except:
                pass
            return metadata
