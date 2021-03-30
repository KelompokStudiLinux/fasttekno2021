const fs = require("fs");
const express = require("express");

const port = 3000;
const app = express();

app.get("/", function (req, res) {
  if (req.query.album) {
    res.write(fs.readFileSync("./public/assets/" + req.query.album));
    return res.end();
  }

  res.write(fs.readFileSync("./public/index.html"));
  res.end();
});

app.listen(port, () => console.log("Listening " + port));
