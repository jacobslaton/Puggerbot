const fs = require('fs');

let exit_code = null;
fs.readFile('exit_code.txt', 'utf8', (err, data) => {
	fs.unlink('exit_code.txt', err => {
		if (err) {
			console.log(err);
		}
	});
	if (err) {
		console.log(err);
		exit_code = 1;
		return;
	}
	exit_code = data;
	process.exit(exit_code);
});
