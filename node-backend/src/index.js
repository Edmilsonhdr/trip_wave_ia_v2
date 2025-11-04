import express from "express";
import fetch from "node-fetch";
const app = express()

app.use(express.json());

const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.post('/api/tripwave/parse', async (req, res) => {
  const response = await fetch("http://localhost:8000/parse", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  });
  const data = await response.json();
  res.json(data);
});

app.post("/api/tripwave/generate-plan", async (req, res) => {
  const response = await fetch("http://localhost:8000/generate-plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  });
  const data = await response.json();
  res.json(data);
});

app.listen(port, () => {
  console.log("Node backend rodando em http://localhost:3000")
})
