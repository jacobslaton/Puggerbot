const config = require('./config');
const Discord = require('discord.js');
const error_text = require('./error_text');
const fs = require('fs');
const help_text = require('./help_text');
const path = require('path');

/////////////
// Utility //
/////////////

function is_owner(msg) {
	return msg.author.id == config.owner.id;
}
function is_admin(msg) {
	return is_owner(msg) || msg.member.hasPermission('ADMINISTRATOR');
}

//////////////
// Commands //
//////////////

const cmds = {
	'bark' : barkbork,
	'bork' : barkbork,
	'help' : help,
	'hype' : hype,
	'pet' : pet,
	'shutdown' : shutdown,
	'update' : update,
}

function barkbork(client, msg, args=[], batch=false) {
	let response = '';
	let subcontent = msg.content;
	const re_barkbork = /(b[ao]rk)/;
	let woof = re_barkbork.exec(subcontent);
	while (woof != null) {
		let sound = subcontent.slice(woof.index, woof.index+woof[0].length);
		if (sound == 'bark') {
			response += 'bork ';
		} else if (sound == 'bork'){
			response += 'bark ';
		} else {
			response += 'b?rk ';
		}
		subcontent = subcontent.slice(woof.index+woof[0].length);
		woof = re_barkbork.exec(subcontent);
	}
	response = response.charAt(0).toUpperCase()+response.slice(1, -1)+'!';
	msg.channel.send(response);
}
function help(client, msg, args=[], batch=false) {
	if (args.length == 0 || args[0] == 'help') {
		msg.channel.send(new Discord.RichEmbed()
			.setColor(config.embed_color)
			.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
			.setThumbnail('https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg')
			.setDescription('Version '+config.version)
			.addField('Command Specific Help', 'Type `>help [command_name]` for more information on a command.')
			.addField('More Information', 'For more information, visit [my github page](https://github.com/jacobslaton/Puggerbot).')
			.setTimestamp()
		);
		return;
	}
	msg.channel.send(new Discord.RichEmbed()
		.setColor(config.embed_color)
		.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
		.addField('Help Page for '+args[0], help_text[args[0]])
	);
}
async function hype(client, msg, args=[], batch=false) {
	await msg.react('🇭');
	await msg.react('🇾');
	await msg.react('🇵');
	await msg.react('🇪');
}
function pet(client, msg, args=[], batch=false) {
	const files = fs.readdirSync(path.join('Media', 'pet'));
	const file = files[Math.floor(Math.random()*files.length)];
	msg.channel.send({
		files : [{
			'attachment' : path.join('Media', 'pet', file),
			'name' : file,
		}]
	});
}
function shutdown(client, msg, args=[], batch=false) {
	if (!is_owner(msg)) {
		msg.channel.send(error_text.owner_only);
	} else {
		return 0;
	}
}
function update(client, msg, args=[], batch=false) {
	if (!is_owner(msg)) {
		msg.channel.send(error_text.owner_only);
	} else {
		return 2;
	}
}

module.exports = cmds;
