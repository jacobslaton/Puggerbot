const config = require('./config');

const help_text = {
	'bark' : 'Bork!',
	'bork' : 'Bark!',
	'hype' : 'Got something exciting to share? Let Puggerbot show his 🇭 🇾 🇵 🇪',
	'pet' : 'Give Puggerbot a pet! He\'ll respond with a cute pug gif.',
	'shutdown' : `Shuts down Puggerbot. Can only be used by ${config.owner.username}.`,
	'update' : `Restarts Puggerbot to pull from his git repository. Can only be used by ${config.owner.username}.`,
}

module.exports = help_text;
