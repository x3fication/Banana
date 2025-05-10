process.on('uncaughtException', (err) => {
  console.error('[ohio]', err);
});

process.on('unhandledRejection', (boxzzzzz) => {
  console.error('[ohio]', boxzzzzz);
});

import express from 'express';
import { createBot } from 'mineflayer';

const app = express();
const port = 6969;

const botz = {}, statuz = {};

app.use(express.json());

app.post('/connect', (req, res) => {
  const { host, port = 25565, username } = req.body;
  const server = `${host}:${port}`;
  
  if (botz[server]?.[username]) return res.status(400).json({ error: 'Bot already connected.' });

  let bot;
  try {
    bot = createBot({ host, port, username });
  } catch (err) {
    return res.status(500).json({ error: `Failed to create bot: ${err.message}` });
  }

  botz[server] = botz[server] || {};
  statuz[server] = statuz[server] || {};
  botz[server][username] = bot;
  statuz[server][username] = { connected: false, username };

  bot.on('login', () => console.log(`[Bot] Logged in as ${username} on ${server}`));
  bot.on('spawn', () => {
    console.log(`[Bot] Spawned on ${server}`);
    statuz[server][username].connected = true;
  });
  bot.on('end', () => {
    console.log(`[Bot] Disconnected from ${server}`);
    delete botz[server][username];
    delete statuz[server][username];
    if (!Object.keys(botz[server]).length) delete botz[server];
    if (!Object.keys(statuz[server]).length) delete statuz[server];
  });
  bot.on('error', err => console.log(`[Bot] ${username} @ ${server}: ${err.message}`));

  res.json({ message: 'Bot is connecting...', server, username, status: 'connecting' });
});

app.post('/send', (req, res) => {
  const { host, port = 25565, username, message } = req.body;
  const server = `${host}:${port}`;
  const bot = botz[server]?.[username];
  if (!bot) return res.status(400).json({ error: 'No bot with this username connected.' });
  
  bot.chat(message);
  res.json({ message: `Sent to ${server} by ${username}: ${message}` });
  res.status(200).send('received')
});

app.post('/disconnect', (req, res) => {
  const { host, port = 25565, username } = req.body;
  const server = `${host}:${port}`;
  const bot = botz[server]?.[username];
  const status = statuz[server]?.[username];

  if (!bot || !status) return res.status(400).json({ error: 'No bot connected.' });

  bot.quit();
  delete botz[server][username];
  delete statuz[server][username];
  if (!Object.keys(botz[server]).length) delete botz[server];
  if (!Object.keys(statuz[server]).length) delete statuz[server];

  res.json({ message: `Bot ${username} disconnected from ${server}` });
});

app.get('/status', (req, res) => res.json(Object.keys(statuz).length ? statuz : { connected: false }));
app.listen(port, () => console.log(`API listening on http://localhost:${port}`))