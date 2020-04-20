const cmd_util = require('./cmd_util.js');
const cmds = require('./cmds.js');
const config = require('./config');
const Discord = require('discord.js');
const error_text = require('./error_text');
const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

class DiscordBot {
	constructor() {
		this.exit_code = null;
		this.init();
		this.client = new Discord.Client();
		this.client.on('ready', () => {
			console.log(`${this.client.user.username} is online.`);
		});
		this.client.on('message', msg => { this.handle_cmd(msg); });
		this.client.on('disconnect', () => { this.shutdown(); });
	}
	init() {
		this.db_ref = null;
		try {
			fs.accessSync(path.join('SQL', 'reference.db'));
		} catch (err) {
			this.db_ref = new sqlite3.Database(path.join('SQL', 'reference.db'));
			const path_ref = path.join('SQL', 'Reference');
			const files_ref = fs.readdirSync(path_ref);
			for (let ii = 0; ii < files_ref.length; ++ii) {
				console.log(files_ref[ii]);
				this.db_ref.exec(fs.readFileSync(path.join(path_ref, files_ref[ii]), 'utf8'));
			}
			this.db_ref.close();
		}
		this.db_ref = new sqlite3.Database('SQL/reference.db', sqlite3.OPEN_READONLY);
		this.db_data = new sqlite3.Database('SQL/user_data.db');
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
				msg_cmds[ii].flags,
				this.db_ref,
				this.db_data
			);
			if (this.exit_code == 0 || this.exit_code == 2) {
				console.log(`${this.client.user.username} is offline.`);
				this.client.destroy();
				return;
			}
		}
	}
	shutdown() {
		this.db_data.close();
		this.db_ref.close();
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
