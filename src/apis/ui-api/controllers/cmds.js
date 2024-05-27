require("dotenv").config();

const HttpClient = require("../http-client.js");

const KAFKA_API_BASE_URL = process.env.KAFKA_API_BASE_URL;
console.log("KAFKA_API_BASE_URL", KAFKA_API_BASE_URL);

const PERSIST_TOPIC = "PROJECTM_CMD_PERSIST";
const GATHER_TOPIC = "PROJECTM_CMD_GATHER";
const STRUCTURE_TOPIC = "PROJECTM_CMD_STRUCTURE";
const AZDO_PROXY_TOPIC = "PROJECTM_CMD_AZDO_PROXY";

const client = new HttpClient(KAFKA_API_BASE_URL);

const buildPersistCmd = (req) => {
  const cmd = {
    topic: PERSIST_TOPIC,
    key: "1",
    payload: req,
  };
  return cmd;
};

const buildGatherCmd = (req) => {
  const cmd = {
    topic: GATHER_TOPIC,
    key: "1",
    payload: req,
  };
  return cmd;
};

const buildStructureCmd = (req) => {
  const cmd = {
    topic: STRUCTURE_TOPIC,
    key: "1",
    payload: req,
  };
  return cmd;
};

const buildAzdoProxyCmd = (req) => {
  const cmd = {
    topic: AZDO_PROXY_TOPIC,
    key: "1",
    payload: req,
  };
  return cmd;
};

const processCmd = async (req, res, cmdBuilder) => {
  try {
    const reqBody = req.body;
    const cmd = cmdBuilder(reqBody);
    const data = await client.post("kafka/topic/publish", cmd);
    res.json(data);
  } catch (error) {
    debugger;
    console.error("GET request error:", error);
    res.status(500).json({ error: "Error processing command." });
  }
};

const processPersistCmd = async (req, res) => {
  await processCmd(req, res, buildPersistCmd);
};

const processGatherCmd = async (req, res) => {
  await processCmd(req, res, buildGatherCmd);
};

const processStructureCmd = async (req, res) => {
  await processCmd(req, res, buildStructureCmd);
};

const processAzdoProxyCmd = async (req, res) => {
  await processCmd(req, res, buildAzdoProxyCmd);
};

module.exports = {
  processCmd,
  processPersistCmd,
  processGatherCmd,
  processStructureCmd,
  processAzdoProxyCmd,
  buildPersistCmd,
  buildGatherCmd,
  buildStructureCmd,
  buildAzdoProxyCmd,
};
