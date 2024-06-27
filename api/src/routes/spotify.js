const express = require('express');
const router = express.Router();
const spotifyService = require('../services/spotifyService');

router.get('/cover', async (req, res) => {
    const { title, artist } = req.query;

    if (!title || !artist) {
        return res.status(400).json({ error: 'Title and artist are required' });
    }

    try {
        const coverUrl = await spotifyService.getCoverArt(title, artist);
        res.json(coverUrl);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;

