const config = require('./config');

const error_text = {
	'admin_only' : 'Grrr, bark! (You\'re not my supervisor! Only admins can use that command.)',
	'owner_only' : `Grrr, bark! (You're not my supervisor! Only ${config.owner.username} can use that command.)`,
	'purge' : ':warning: An admin has requested to purge more than 50 messages. To confirm, purge again. :warning:',
	'no_permission' : 'Bork? (I do not have the proper permissions to use that command.)',
	'empty_query' : [
		'*Rolls a natural 1.*',
		'All out of szechuan sauce.',
		'Geeettttttt dunked on!!!',
		'Just Monika.',
		'I\'m sorry Dave, I\'m afraid I can\'t do that.',
		'Your query has been counterspelled!',
		'Your query has been exiled!',
		'Your query has been sent to the Shadow Realm!',
		'Your query has entered the *danger zone*.'
	],
	'odd__double_quotes' : 'Error: this message has an odd number of unescaped double quotes',
	'missing_semicolon' : 'Error: {} command is a missing trailing semicolon',
	'bad_command' : 'Bork? (I had some trouble unsterstanding your commands.)',
	'no_help' : 'Bork? (I couldn\'t find a help page for that command.)'
}

module.exports = error_text;
