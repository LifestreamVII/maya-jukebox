const axios = require('axios');
require('dotenv').config();

const getSpotifyToken = async () => {
    try {
        const response = await axios.post(
            'https://accounts.spotify.com/api/token',
            'grant_type=client_credentials',
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic ' + Buffer.from(
                        process.env.SPOTIFY_CLIENT_ID + ':' + process.env.SPOTIFY_CLIENT_SECRET
                    ).toString('base64')
                }
            }
        );
        return response.data.access_token;
    } catch (error) {
        console.error('Error fetching Spotify token:', error.message);
        throw new Error('Unable to fetch Spotify token');
    }
};

const getCoverArt = async (title, artist) => {
    let token;
    try {
        token = await getSpotifyToken();
    } catch (error) {
        throw new Error('Failed to authenticate with Spotify');
    }

    try {
        const response = await axios.get(
            'https://api.spotify.com/v1/search',
            {
                params: {
                    query: `album:"${title}" artist:"${artist}"`,
                    type: 'album',
                    limit: 1
                },
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        if (response.data.albums.items.length > 0) {
            return {coverUrl: response.data.albums.items[0].images[0].url, spotUrl: response.data.albums.items[0].external_urls.spotify};
        } else {
            throw new Error('No album found for the given title and artist');
        }
    } catch (error) {
        console.error('Error fetching cover art from Spotify:', error.message);
        throw new Error('Failed to fetch cover art from Spotify');
    }
};

module.exports = {
    getCoverArt
};
