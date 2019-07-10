const config = require('./config');
const DiscordBot = require('./DiscordBot.js');
const process = require('process');

puggerbot = new DiscordBot();
if (process.argv[2] === "-d" || process.argv[2] === "--debug") {
	puggerbot.run(config.token_debug);
} else {
	puggerbot.run(config.token);
}
