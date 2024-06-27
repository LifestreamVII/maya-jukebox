const express = require('express');
const app = express();
const spotifyRouter = require('./routes/spotify');

app.use(express.json());
app.use('/spotify', spotifyRouter);

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
