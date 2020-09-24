import requests
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

from new_releases.models.artist import ArtistModel
from new_releases.models.artists_refresh import ArtistsRefreshModel
from new_releases.models.image import ImageModel
from new_releases.models.genre import GenreModel


class SpotifyBrowseAPIService():
    BROWSE_URL = "https://api.spotify.com/v1/browse/new-releases"

    def __init__(self):
        self.session = FuturesSession()

    def retrieve_new_artists(self, token):
        ArtistModel.objects.all().hard_delete()
        albums = self._retrieve_new_albums_releases(token)
        artists = [
            artist for album in albums
            for artist in album.get('artists') if album.get('artists')
        ]
        artist_models = self._save_artists_details(token, artists)
        ArtistsRefreshModel().save()
        return artist_models

    def _retrieve_new_albums_releases(self, token):
        response = requests.get(
            self.BROWSE_URL,
            headers={'Authorization': f"Bearer {token}"}
        )
        raw_json = response.json()
        response.raise_for_status()

        if "albums" not in raw_json:
            return None

        raw_json_albums = raw_json.get("albums")
        if "items" not in raw_json_albums:
            return None

        return raw_json_albums.get("items")

    def _save_artists_details(self, token, artists):
        artist_detail_hrefs = [
            artist.get('href') for artist in artists
        ]
        artist_detail_requests = [
            self.session.get(
                href,
                headers={'Authorization': f"Bearer {token}"}
            ) for href in artist_detail_hrefs
        ]
        artist_models = []
        for future in as_completed(artist_detail_requests):
            resp = future.result()
            if "error" in resp:
                continue

            artist_model = self._save_artist_details(resp.json())
            artist_models.append(artist_model)
        return artist_models

    def _save_artist_details(self, raw_artist):
        artist_model = ArtistModel.objects.create(
            spotify_id=raw_artist.get('id'),
            name=raw_artist.get('name'),
            followers=raw_artist.get('followers').get('total'),
            popularity=raw_artist.get('popularity'),
        )

        genre_models = []
        for genre in raw_artist.get('genres'):
            genre_model, created = GenreModel.objects.get_or_create(name=genre)
            genre_models.append(genre_model)
        artist_model.genres.set(genre_models)

        image_models = []
        for image in raw_artist.get('images'):
            image_models.append(
                ImageModel(
                    artist=artist_model,
                    url=image.get('url'),
                    height=image.get('height'),
                    width=image.get('width')
                )
            )
        ImageModel.objects.bulk_create(image_models)
        return artist_model
