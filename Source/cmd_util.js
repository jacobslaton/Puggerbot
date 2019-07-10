const error_text = require('./error_text');

function check_msg(content) {
	let err = '';
	// Double Quotes
	const content_escaped = content.replace('\\"', '');
	if ((content_escaped.split('"').length - 1) % 2 == 1) {
		err += error_text.odd__double_quotes+'\n';
	}
	// Semicolons
	const re_bad = />([A-z_]+)(?:( +"(?:[^\\"]|\\.)*")|(?: +[^ ">;\n]+))* *>/;
	let subcontent = content.replace(/<@[0-9]+>/g, '');
	let invalid = re_bad.exec(subcontent);
	while (invalid != null) {
		console.log(subcontent);
		subcontent = subcontent.slice(invalid.index+invalid[0].length);
		err += error_text.missing_semicolon.replace('{}', invalid[1])+'\n';
		invalid = re_bad.exec(subcontent);
	}
	return err;
}
function parse_args(arg_str) {
	const re_args = /(?:"(?:[^\\"]|\\.)*")|(?:[^ ;\n]+)/;
	let args = [];
	let arg_found = re_args.exec(arg_str);
	while (arg_found != null) {
		arg_str = arg_str.slice(arg_found.index+arg_found[0].length);
		args.push(arg_found[0]);
		arg_found = re_args.exec(arg_str);
	}
	return args;
}
function parse_cmds(content) {
	const re_cmd = />([A-z_]+)((?:( +"(?:[^\\"]|\\.)*")|(?: +[^ ">;\n]+))*)/;
	let cmds = [];
	let subcontent = content;
	let cmd_match = re_cmd.exec(subcontent);
	while (cmd_match != null) {
		subcontent = subcontent.slice(cmd_match.index+cmd_match[0].length);
		cmds.push({
			'cmd' : cmd_match[1],
			'args' : parse_args(cmd_match[2])
		});
		cmd_match = re_cmd.exec(subcontent);
	}
	return cmds;
}

module.exports = {
	'check_msg' : check_msg,
	'parse_args' : parse_args,
	'parse_cmds' : parse_cmds
};