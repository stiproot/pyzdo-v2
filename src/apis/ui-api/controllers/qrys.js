// const { get, post } = require("../http-client.js");
require("dotenv").config();

const HttpClient = require("../http-client.js");

// const BASE_URL = "http://0.0.0.0:8000/";
const STORE_API_BASE_URL = process.env.STORE_API_BASE_URL;
console.log("STORE_API_BASE_URL", STORE_API_BASE_URL);

const client = new HttpClient(STORE_API_BASE_URL);

const processResp = (resp) => {
  const refined = resp["result"];
  return refined;
};

const processQry = async (req, res) => {
  try {
    const reqBody = req.body;
    const data = await client.post("store/qry", reqBody);
    const processedResp = processResp(data);
    res.json(processedResp);
  } catch (error) {
    console.error("Process qry request error:", error);
    res.status(500).json({ error: "Error processing query." });
  }
};

module.exports = { processQry };
