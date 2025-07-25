process.on('uncaughtException', (err) => {
  console.error('[ohio]', err);
});

process.on('unhandledRejection', (boxzzzzz) => {
  console.error('[ohio]', boxzzzzz);
});

import express from 'express';
import { createBot } from 'mineflayer';
import { SocksClient } from 'socks';
const app = express();
const port = 6969;

const botz = {}, statuz = {};

app.use(express.json());

function parseProxy(proxyUrl) {
  try {
    const url = new URL(proxyUrl);
    if (!url.protocol.startsWith('socks')) throw new Error('Unsupported proxy type');
    return {
      type: parseInt(url.protocol.replace('socks', '').replace(':', ''), 10),
      host: url.hostname,
      port: parseInt(url.port, 10),
      userId: url.username || undefined,
      password: url.password || undefined
    };
  } catch {
    throw new Error('Invalid proxy URL format');
  }
}

app.post('/connect', async (req, res) => {
  const { host, port = 25565, username, proxy } = req.body;
  const server = `${host}:${port}`;
  if (botz[server]?.[username]) return res.status(400).json({ error: 'Bot already connected.' });

  try {
    let customConnect;
    if (proxy) {
      const broxy = parseProxy(proxy);
      customConnect = async (client) => {
        const { socket } = await SocksClient.createConnection({
          proxy: {
            host: broxy.host,
            port: broxy.port,
            type: broxy.type,
            username: broxy.userId,
            password: broxy.password
          },
          command: 'connect',
          destination: { host: host.trim(), port: Number(port) }
        });
        console.log(`[Proxy] Connected through ${broxy.host}:${broxy.port}`);
        client.setSocket(socket);
        client.emit('connect');
      };
    }

    const bot = createBot({
      username,
      host,
      port: Number(port),
      auth: 'offline',
      connect: customConnect
    });

    bot.on('login', () => console.log(`[Bot] Logged in as ${username} on ${server}`));
    bot.on('spawn', () => statuz[server][username].connected = true);
    bot.on('error', err => console.error(`[Bot] ${err.message}`));

    botz[server] = botz[server] || {};
    statuz[server] = statuz[server] || {};
    botz[server][username] = bot;
    statuz[server][username] = { connected: false, username };

    res.json({ message: 'Bot connecting...', server, username, status: 'connecting' });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: `Connection failed: ${err.message}` });
  }
});


app.post('/send', (req, res) => {
  const { host, port = 25565, username, message } = req.body;
  const server = `${host}:${port}`;
  const bot = botz[server]?.[username];
  if (!bot) return res.status(400).json({ error: 'No bot with this username connected.' });
  
  bot.chat(message);
  res.json({ message: `Sent to ${server} by ${username}: ${message}` });
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
app.listen(port, () => console.log(`API listening on http://localhost:${port}`));