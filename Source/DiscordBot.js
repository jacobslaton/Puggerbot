const cmd_util = require('./cmd_util.js');
const cmds = require('./cmds.js');
const config = require('./config');
const Discord = require('discord.js');
const error_text = require('./error_text');
const fs = require('fs');

class DiscordBot {
	constructor() {
		this.exit_code = null;
		this.client = new Discord.Client();
		this.client.on('ready', () => { this.init(); });
		this.client.on('message', msg => { this.handle_cmd(msg); });
		this.client.on('disconnect', () => { this.shutdown(); });
	}
	init() {
		console.log(`${this.client.user.username} is online.`);
	}
	async handle_cmd(msg) {
		if (msg.author.id === this.client.user.id) { return; }
		const errors = cmd_util.check_msg(msg.content);
		if (errors != '') {
			msg.channel.send(new Discord.RichEmbed()
				.setColor(config.embed_color)
				.setTitle(error_text.bad_command)
				.setDescription(errors)
			);
			return;
		}
		const msg_cmds = cmd_util.parse_cmds(msg.content);
		for (let ii = 0; ii < msg_cmds.length; ++ii) {
			if (!cmds.hasOwnProperty(msg_cmds[ii].cmd)) { continue; }
			this.exit_code = await cmds[msg_cmds[ii].cmd](
				this.client,
				msg,
				msg_cmds[ii].args,
				msg_cmds.length > 1
			);
			if (this.exit_code == 0 || this.exit_code == 2) {
				console.log(`${this.client.user.username} is offline.`);
				this.client.destroy();
				return;
			}
		}
	}
	shutdown() {
		fs.writeFile('exit_code.txt', this.exit_code, err => {
			if (err) {
				console.log(err);
			}
		});
	}
	run(token) {
		this.client.login(token).catch(console.error);
	}
}

module.exports = DiscordBot;
