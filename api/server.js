import express from 'express'
import { createBot } from 'mineflayer'

const app = express()
const port = 6969
let bot = null, latestMessage = null, botStatus = { connected: false, username: null }

app.use(express.json())

app.post('/connect', ({ body: { host, port, username } }, res) => {
  if (bot) return res.status(400).json({ error: 'Bot already connected.' })
  if (host.includes(':')) [host, port] = host.split(':')
  bot = createBot({ host, port: port || 25565, username })
  
  bot.on('login', () => { console.log(`[Bot] Logged in as ${username}`); botStatus = { connected: true, username } })
  bot.on('end', () => { console.log('[Bot] Disconnected.'); botStatus = { connected: false, username: null }; bot = null })
  bot.on('spawn', () => { console.log('[Bot] Spawned in server.'); botStatus.connected = true })
  bot.on('messagestr', (message) => latestMessage = message)

  res.json({ message: `Bot ${username} connected to ${host}:${port || 25565}` })
})

app.post('/send', ({ body: { message } }, res) => {
  if (!bot) return res.status(400).json({ error: 'No bot connected.' })
  bot.chat(message)
  res.json({ message: `Sent: ${message}` })
})

app.post('/disconnect', (req, res) => {
  if (!bot) return res.status(400).json({ error: 'No bot connected.' })
  bot.quit()
  bot = null
  botStatus = { connected: false, username: null }
  res.json({ message: 'Bot disconnected.' })
})

app.get('/status', (req, res) => res.json(botStatus))
app.get('/latest', (req, res) => latestMessage ? res.json({ latestMessage }) : res.status(400).json({ error: 'No messages received yet.' }))

app.listen(port, () => console.log(`API listening on http://localhost:${port}`))
