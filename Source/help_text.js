const config = require('./config');

const help_text = {
	'bark' : 'Bork!',
	'bible' : 'Lookup verses from the Bible. Choose your version by passing it in the "v" flag and indicate which passage by passing it in the "p" flag.',
	'bork' : 'Bark!',
	'hype' : 'Got something exciting to share? Get Puggerbot 🇭 🇾 🇵 🇪 d up!',
	'pet' : 'Give Puggerbot a pet! He\'ll respond with a cute pug gif.',
	'shutdown' : `Shuts down Puggerbot. Can only be used by ${config.owner.username}.`,
	'update' : `Restarts Puggerbot to pull from his git repository. Can only be used by ${config.owner.username}.`,
	'votd' : 'Posts the verse of the day from the KJV.',
}

module.exports = help_text;
