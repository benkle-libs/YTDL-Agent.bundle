import os


def sum(iter):
    result = 0
    for item in iter:
        result += item
    return result

def Start():
    HTTP.CacheTime = CACHE_1MONTH
    HTTP.Headers[
        'User-Agent'] = 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.54'
    HTTP.Headers['Accept-Language'] = 'en-us'


def LoadAnyJSON(directory, filenames=[]):
    result = False
    if len(filenames) > 0:
        for filename in filenames:
            filename = os.path.join(directory, filename)
            if os.path.exists(filename):
                result = JSON.ObjectFromString(Core.storage.load(filename))
                break
    else:
        try:
            result = JSON.ObjectFromString(Core.storage.load(directory))
        except:
            pass
    return result


def any(hash, keys, default=''):
    for key in keys:
        if key in hash:
            return hash[key]
    return default


def ApplyInfoToMetadata(infoData, metadata):
    metadata.title = any(infoData, ['fulltitle', 'title', 'name'])
    if 'name' in dir(metadata):
        metadata.name = metadata.title
    if 'original_title' in dir(metadata):
        metadata.original_title = metadata.title
    if 'duration' in dir(metadata):
        metadata.duration = infoData['duration']
    metadata.summary = any(infoData, ['description', 'summary'])
    date = any(infoData, ['upload_date', 'date', 'year'])
    if date:
        date = Datetime.ParseDate(str(date))
        metadata.originally_available_at = date.date()
        if 'year' in dir(metadata):
            metadata.year = date.year
    metadata.rating = infoData['average_rating'] * 2 if 'average_rating' in infoData else 10.0
    metadata.content_rating = 0
    try:
        metadata.directors.clear()
        meta_director = metadata.directors.new()
        meta_director.name = infoData['uploader'] if 'uploader' in infoData else infoData['extractor']
    except:
        pass
    return metadata


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
        infoData = LoadAnyJSON(os.path.splitext(filename)[0] + '.info.json')
        if infoData:
            ytdl_id = 'movie-' + infoData['extractor'] + '-' + infoData['id']
            metadata = MetadataSearchResult(
                id=ytdl_id,
                name=media.name,
                year=int(infoData['upload_date'][:4]) if 'upload_date' in infoData else None,
                score=infoData['average_rating'] if 'average_rating' in infoData else 100,
                lang=lang
            )
            results.Append(metadata)

    def update(self, metadata, media, lang, force):
        filename = String.Unquote(media.items[0].parts[0].file)
        infoData = LoadAnyJSON(os.path.splitext(filename)[0] + '.info.json')
        if infoData:
            return ApplyInfoToMetadata(infoData, metadata)


class YoutubeDLSeriesAgent(Agent.TV_Shows):
    name = 'Youtube-DL Shows'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = [
        'com.plexapp.agents.localmedia',
        'com.plexapp.agents.opensubtitles',
        'com.plexapp.agents.plexthememusic'
    ]
    contributes_to = [
        'com.plexapp.agents.thetvdb'
    ]

    def search(self, results, media, lang):
        filename = String.Unquote(media.filename)
        directory = os.path.dirname(os.path.dirname(filename))
        title = os.path.basename(directory)
        infoData = LoadAnyJSON(directory, [title + '.info.json', 'show.info.json'])
        if infoData:
            infoData['name'] = infoData['name'] if 'name' in infoData else media.show
            infoData['id'] = infoData['id'] if 'id' in infoData else infoData['name'].replace(' ', '-').lower()
            infoData['year'] = infoData['year'] if 'year' in infoData else 1700
            infoData['score'] = infoData['score'] if 'score' in infoData else 100
            metadata = MetadataSearchResult(
                id=infoData['id'],
                name=infoData['name'],
                year=infoData['year'],
                score=infoData['score'],
                lang=lang
            )
            results.Append(metadata)

    def update(self, metadata, media, lang, force):
        showDirectory = ''
        showRatings = []
        for season in media.seasons:
            seasonDirectory = ''
            metadata.seasons[season].index = int(season)
            for episode in media.seasons[season].episodes:
                filename = media.seasons[season].episodes[episode].items[0].parts[0].file
                seasonDirectory = os.path.dirname(filename)
                showDirectory = os.path.dirname(seasonDirectory)
                infoData = LoadAnyJSON(os.path.splitext(filename)[0] + '.info.json')
                if infoData:
                    ApplyInfoToMetadata(infoData, metadata.seasons[season].episodes[episode])
                    showRatings += [metadata.seasons[season].episodes[episode].rating]
            infoData = LoadAnyJSON(seasonDirectory, [os.path.basename(seasonDirectory) + '.info.json', 'season.info.json'])
            if infoData:
                metadata.seasons[season].summary = infoData['summary'] if 'summary' in infoData else ''
        infoData = LoadAnyJSON(showDirectory, [os.path.basename(showDirectory) + '.info.json', 'show.info.json'])
        if infoData:
            if not set(dir(infoData)) & {'fulltitle', 'title', 'name'}:
                infoData['title'] = metadata.title
            Log.Debug(infoData)
            ApplyInfoToMetadata(infoData, metadata)
        metadata.rating = sum(showRatings) / len(showRatings)
        return metadata
