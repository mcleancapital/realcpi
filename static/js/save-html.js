// save-html.js
const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
app.use(express.json({ limit: '5mb' }));

app.post('/save-html', (req, res) => {
  const { filename, html } = req.body;
  const filePath = path.join(__dirname, 'stocks', filename);

  fs.writeFile(filePath, html, err => {
    if (err) {
      console.error("Error saving file:", err);
      return res.status(500).send("Error saving file");
    }
    res.send("Saved");
  });
});

app.listen(3000, () => console.log("Server running on port 3000"));
