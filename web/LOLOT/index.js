const fs = require("fs");
const express = require("express");

const port = 3000;
const app = express();

app.get("/", function (req, res) {
  if (req.query.album) {
    const q = req.query.album.replace(/\.\.\//g, '');
    res.write(fs.readFileSync("./public/assets/" + q));
    return res.end();
  }

  res.write(fs.readFileSync("./public/index.html"));
  res.end();
});

app.listen(port);
