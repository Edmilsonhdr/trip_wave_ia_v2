import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

const port = 3000;

app.get("/", (req, res) => {
  res.send("Node backend rodando!");
});

app.post("/api/tripwave/parse", async (req, res) => {
  try {
    // Valida se o body tem a propriedade mensagem
    if (!req.body || !req.body.mensagem) {
      return res.status(400).json({
        error: "O campo 'mensagem' é obrigatório no body da requisição",
      });
    }

    const response = await fetch("http://localhost:8000/parse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error("Erro ao processar requisição /parse:", error);
    res.status(500).json({
      error: "Erro interno do servidor",
      message: error.message,
    });
  }
});

app.post("/api/tripwave/generate-plan", async (req, res) => {
  try {
    // Valida se os campos obrigatórios estão presentes
    if (!req.body || !req.body.destino || !req.body.data_inicio || !req.body.data_fim) {
      return res.status(400).json({
        error: "Os campos 'destino', 'data_inicio' e 'data_fim' são obrigatórios",
      });
    }

    const response = await fetch("http://localhost:8000/generate-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error("Erro ao processar requisição /generate-plan:", error);
    res.status(500).json({
      error: "Erro interno do servidor",
      message: error.message,
    });
  }
});

app.post("/api/tripwave/roteiro/pdf", async (req, res) => {
  try {
    // Valida se o body tem roteiro e travel_data
    if (!req.body || !req.body.roteiro || !req.body.travel_data) {
      return res.status(400).json({
        error: "Os campos 'roteiro' e 'travel_data' são obrigatórios",
      });
    }

    const response = await fetch("http://localhost:8000/roteiro/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    // Verifica se é PDF (content-type)
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/pdf")) {
      // Retorna o PDF como buffer
      const buffer = await response.arrayBuffer();
      res.setHeader("Content-Type", "application/pdf");
      res.setHeader(
        "Content-Disposition",
        response.headers.get("content-disposition") || 'attachment; filename="roteiro.pdf"'
      );
      res.send(Buffer.from(buffer));
    } else {
      // Se não for PDF, retorna como JSON (erro)
      const data = await response.json();
      res.status(response.status).json(data);
    }
  } catch (error) {
    console.error("Erro ao processar requisição /roteiro/pdf:", error);
    res.status(500).json({
      error: "Erro interno do servidor",
      message: error.message,
    });
  }
});

app.post("/api/tripwave/roteiro/preview", async (req, res) => {
  try {
    // Valida se o body tem roteiro e travel_data
    if (!req.body || !req.body.roteiro || !req.body.travel_data) {
      return res.status(400).json({
        error: "Os campos 'roteiro' e 'travel_data' são obrigatórios",
      });
    }

    const response = await fetch("http://localhost:8000/roteiro/preview", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    // Verifica se é HTML
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("text/html")) {
      // Retorna o HTML
      const html = await response.text();
      res.setHeader("Content-Type", "text/html");
      res.send(html);
    } else {
      // Se não for HTML, retorna como JSON (erro)
      const data = await response.json();
      res.status(response.status).json(data);
    }
  } catch (error) {
    console.error("Erro ao processar requisição /roteiro/preview:", error);
    res.status(500).json({
      error: "Erro interno do servidor",
      message: error.message,
    });
  }
});

app.listen(port, () => {
  console.log("Node backend rodando em http://localhost:3000");
});
