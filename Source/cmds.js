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
	'bible' : bible,
	'bork' : barkbork,
	'help' : help,
	'hype' : hype,
	'pet' : pet,
	'shutdown' : shutdown,
	'update' : update,
}

function barkbork(client, msg, args=[], flags={}, db_ref, db_data) {
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
function bible(client, msg, args=[], flags={}, db_ref, db_data) {
	// Get passage
	const re_passage = /((?:[0-9] )?(?:[A-z]| )*) ([0-9]+)(?::([0-9]+(?:-[0-9]+)?))?/;
	const match = re_passage.exec(flags['p']);
	if (!match) {
		msg.channel.send(new Discord.RichEmbed()
			.setColor(config.embed_color)
			.setTitle(error_text.bad_command)
			.setDescription(error_text['bad_args'])
		);
		return;
	}
	const book = match[1];
	const chapter = Number(match[2]);
	let verse_start = match[3];
	let verse_end = match[3];
	if (match[3].indexOf('-') > -1) {
		verse_start = match[3].slice(0, match[3].indexOf('-'));
		verse_end = match[3].slice(match[3].indexOf('-')+1);
		verse_end = verse_end < verse_start ? verse_start : verse_end;
	}
	verse_start = Number(verse_start);
	verse_end = Number(verse_end);
	// Select verses
	db_ref.get('select book_id from books where title = ?', [book], function (err, row) {
		if (!row) {
			const empty_query = error_text['empty_query'][Math.floor(Math.random()*error_text['empty_query'].length)];
			msg.channel.send(new Discord.RichEmbed()
				.setColor(config.embed_color)
				.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
				.addField(empty_query, error_text['bible_no_book'].replace('<book>', book))
			);
			return;
		}
		db_ref.all(
			'select verse_num, text from bible_esv where book_id = ? and chapter = ? and verse_num between ? and ?',
			[row.book_id, chapter, verse_start, verse_end],
			function (err, rows) {
				let passage = [''];
				rows.forEach(function (row) {
					let verse = ' **['+row.verse_num+']** '+row.text;
					if (passage[passage.length-1].length+verse.length > 1024) {
						passage.push('');
					}
					passage[passage.length-1] += verse;
				});
				console.log(passage);
				if (passage.length == 1 && passage[0] == '') {
					const empty_query = error_text['empty_query'][Math.floor(Math.random()*error_text['empty_query'].length)];
					msg.channel.send(new Discord.RichEmbed()
						.setColor(config.embed_color)
						.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
						.addField(empty_query, error_text['bible_no_passage'])
					);
					return;
				}
				console.log(passage);
				if (passage.join('').length > 6000) {
					const empty_query = error_text['empty_query'][Math.floor(Math.random()*error_text['empty_query'].length)];
					msg.channel.send(new Discord.RichEmbed()
						.setColor(config.embed_color)
						.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
						.addField(empty_query, error_text['bible_long_passage'])
					);
					return;
				}
				let embed = new Discord.RichEmbed()
					.setColor(config.embed_color)
					.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
					.setDescription('**'+flags['p']+'**');
				for (let ii = 0; ii < passage.length; ++ii) {
					embed.addField('-', passage[ii].slice(1));
				}
				msg.channel.send(embed);
			}
		);
	});
}
function help(client, msg, args=[], flags={}, db_ref, db_data) {
	if (args.length == 0 || args[0] == 'help') {
		msg.channel.send(new Discord.RichEmbed()
			.setColor(config.embed_color)
			.setAuthor(client.user.username, 'https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg', '')
			.setThumbnail('https://cdn.pixabay.com/photo/2016/07/07/15/35/puppy-1502565_960_720.jpg')
			.setDescription('Version '+config.version)
			.addField('Flags', 'Some commands require information to be passed through flags. A flag is a hyphen followed by a character or word. The value of the flag can be assigned with `=` or passed as a string using `"`. Ex: `>bible -v=esv -p"Genesis 1:1"`')
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
async function hype(client, msg, args=[], flags={}, db_ref, db_data) {
	await msg.react('🇭');
	await msg.react('🇾');
	await msg.react('🇵');
	await msg.react('🇪');
}
function pet(client, msg, args=[], flags={}, db_ref, db_data) {
	const files = fs.readdirSync(path.join('Media', 'pet'));
	const file = files[Math.floor(Math.random()*files.length)];
	msg.channel.send({
		files : [{
			'attachment' : path.join('Media', 'pet', file),
			'name' : file,
		}]
	});
}
function shutdown(client, msg, args=[], flags={}, db_ref, db_data) {
	if (!is_owner(msg)) {
		msg.channel.send(error_text.owner_only);
	} else {
		return 0;
	}
}
function update(client, msg, args=[], flags={}, db_ref, db_data) {
	if (!is_owner(msg)) {
		msg.channel.send(error_text.owner_only);
	} else {
		return 2;
	}
}

module.exports = cmds;
