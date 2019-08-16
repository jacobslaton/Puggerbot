const config = require('./config');
const crypto = require('crypto');
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
function empty_query() {
	return error_text['empty_query'][Math.floor(Math.random()*error_text['empty_query'].length)];
}
function send_error(msg, title, text) {
	msg.channel.send(new Discord.RichEmbed()
		.setColor(config.embed_color)
		.setAuthor(client.user.username, config.profile_image, '')
		.addField(title, text)
	);
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
	'votd' : votd,
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
function make_passage_embed(client, msg, passage, version, rows) {
	let fields = [''];
	rows.forEach(function (row) {
		let verse = ' **['+row.verse_num+']** '+row.text;
		if (fields[fields.length-1].length+verse.length > 1024) {
			fields.push('');
		}
		fields[fields.length-1] += verse;
	});
	if (fields.length == 1 && fields[0] == '') {
		send_error(msg, empty_query(), error_text['bible_no_passage']);
		return;
	}
	if (fields.join('').length > 6000) {
		send_error(msg, empty_query(), error_text['bible_long_passage']);
		return;
	}
	let embed = new Discord.RichEmbed()
		.setColor(config.embed_color)
		.setAuthor(client.user.username, config.profile_image, '')
		.setDescription('**'+passage+' ('+version.toUpperCase()+')**');
	for (let ii = 0; ii < fields.length; ++ii) {
		embed.addField('-', fields[ii].slice(1));
	}
	return embed;
}
function bible(client, msg, args=[], flags={}, db_ref, db_data) {
	// Get passage
	const re_passage = /((?:[0-9] )?(?:[A-z]| )*) ([0-9]+)(?::([0-9]+(?:-[0-9]+)?))?/;
	const match = re_passage.exec(flags['p']);
	if (!match) {
		send_error(msg, error_text.bad_command, error_text['bad_args']);
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
	// Get version
	let version = flags['v'];
	if (!version) {
		version = 'kjv';
	} else {
		version = version.toLowerCase();
	}
	db_ref.get('select name from sqlite_master where type=\'table\' and name=?', ['bible_'+version], function (err, row) {
		if (!row) {
			send_error(msg, error_text.bad_command, error_text['bad_args']);
			return;
		}
		// Select verses
		db_ref.get('select book_id from bible_books where title = ?', [book], function (err, row) {
			if (!row) {
				send_error(msg, empty_query(), error_text['bible_no_book'].replace('<book>', book));
				return;
			}
			db_ref.all(
				'select verse_num, text from bible_'+version+' where book_id = ? and chapter = ? and verse_num between ? and ?',
				[row.book_id, chapter, verse_start, verse_end],
				function (err, rows) {
					msg.channel.send(make_passage_embed(client, msg, flags['p'], version, rows));
				}
			);
		});
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
function votd(client, msg, args=[], flags={}, db_ref, db_data) {
	db_ref.all('select verse_id from bible_kjv', [], function (err, rows) {
		const date = new Date().toISOString().replace('T', '').substr(0, 10);
		const hash = crypto.createHash('md5').update(date).digest('hex');
		const id = parseInt(hash, 16)%rows.length;
		db_ref.get('select * from bible_kjv where verse_id = ?', [id], function (err, verse) {
			db_ref.get('select title from bible_books where book_id = ?', [verse.book_id], function (err, book) {
				let embed = new Discord.RichEmbed()
					.setColor(config.embed_color)
					.setAuthor(client.user.username, config.profile_image, '')
					.setDescription('**'+book.title+' '+verse.chapter+':'+verse.verse_num+' (KJV)**')
					.addField('-', '**['+verse.verse_num+']** '+verse.text)
					.setTimestamp();
				msg.channel.send(embed);
			});
		});
	});
}

module.exports = cmds;
