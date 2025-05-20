// server.js
const express = require("express");
const jsf = require("json-schema-faker");
const bodyParser = require("body-parser");
const fs = require("fs");

const app = express();
app.use(bodyParser.json());

app.post("/generate", (req, res) => {
  try {
    const { schema, count } = req.body;
    const results = [];

    for (let i = 0; i < (count || 1); i++) {
      results.push(jsf.generate(schema));  // 여기서 터질 수 있음
    }

    res.json(results);
  } catch (err) {
    console.error("🔥 JSON generation 실패:", err.message);
    res.status(400).json({ error: err.message });
  }
});


app.listen(3000, () => {
    console.log("✅ JSON Schema Faker API running at http://localhost:3000");
});
