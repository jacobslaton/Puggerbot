create table if not exists bible_books (
	book_id		integer not null primary key autoincrement,
	title		char(15) not null,
	abbr		varchar(85) not null
);

insert into bible_books (book_id, title, abbr) values(0, 'Genesis', 'Gen,Ge,Gn');
insert into bible_books (title, abbr) values('Exodus', 'Ex,Exod,Exo');
insert into bible_books (title, abbr) values('Leviticus', 'Lev,Le,Lv');
insert into bible_books (title, abbr) values('Numbers', 'Num,Nu,Nm,Nb');
insert into bible_books (title, abbr) values('Deuteronomy', 'Deut,De,Dt');
insert into bible_books (title, abbr) values('Joshua', 'Josh,Jos,Jsh');
insert into bible_books (title, abbr) values('Judges', 'Judg,Jdg,Jg,Jdgs');
insert into bible_books (title, abbr) values('Ruth', 'Rth,Ru');
insert into bible_books (title, abbr) values('1 Samuel', '1 Sam,1 Sm,1 Sa');
insert into bible_books (title, abbr) values('2 Samuel', '2 Sam,2 Sm,2 Sa');
insert into bible_books (title, abbr) values('1 Kings', '1 Kgs,1 Ki');
insert into bible_books (title, abbr) values('2 Kings', '2 Kgs,2 Ki');
insert into bible_books (title, abbr) values('1 Chronicles', '1 Chron,1 Chr,1 Ch');
insert into bible_books (title, abbr) values('2 Chronicles', '2 Chron,2 Chr,2 Ch');
insert into bible_books (title, abbr) values('Ezra', 'Ezr,Ez');
insert into bible_books (title, abbr) values('Nehemiah', 'Neh,Ne');
insert into bible_books (title, abbr) values('Esther', 'Est,Esth,Es');
insert into bible_books (title, abbr) values('Job', 'Jb');
insert into bible_books (title, abbr) values('Psalms', 'Ps,Psalm,Pslm,Psa,Psm,Pss');
insert into bible_books (title, abbr) values('Proverbs', 'Prov,Pro,Prv,Pr');
insert into bible_books (title, abbr) values('Ecclesiastes', 'Eccles,Eccle,Ecc,Ec,Qoh');
insert into bible_books (title, abbr) values('Song of Solomon', 'Song,Song of Songs,SOS,So');
insert into bible_books (title, abbr) values('Isaiah', 'Isa,Is');
insert into bible_books (title, abbr) values('Jeremiah', 'Jer,Je,Jr');
insert into bible_books (title, abbr) values('Lamentations', 'Lam,La');
insert into bible_books (title, abbr) values('Ezekiel', 'Ezek,Eze,Ezk');
insert into bible_books (title, abbr) values('Daniel', 'Dan,Da,Dn');
insert into bible_books (title, abbr) values('Hosea', 'Hos,Ho');
insert into bible_books (title, abbr) values('Joel', 'Jl');
insert into bible_books (title, abbr) values('Amos', 'Am');
insert into bible_books (title, abbr) values('Obadiah', 'Obad,Ob');
insert into bible_books (title, abbr) values('Jonah', 'Jnh,Jon');
insert into bible_books (title, abbr) values('Micah', 'Mic,Mc');
insert into bible_books (title, abbr) values('Nahum', 'Nah,Na');
insert into bible_books (title, abbr) values('Habakkuk', 'Hab,Hb');
insert into bible_books (title, abbr) values('Zephaniah', 'Zeph,Zep,Zp');
insert into bible_books (title, abbr) values('Haggai', 'Hag,Hg');
insert into bible_books (title, abbr) values('Zechariah', 'Zech,Zec,Zc');
insert into bible_books (title, abbr) values('Malachi', 'Mal,Ml');
insert into bible_books (title, abbr) values('Matthew', 'Matt,Mt');
insert into bible_books (title, abbr) values('Mark', 'Mrk,Mar,Mk,Mr');
insert into bible_books (title, abbr) values('Luke', 'Luk,Lk');
insert into bible_books (title, abbr) values('John', 'Joh,Jhn,Jn');
insert into bible_books (title, abbr) values('Acts', 'Act,Ac');
insert into bible_books (title, abbr) values('Romans', 'Rom,Ro,Rm');
insert into bible_books (title, abbr) values('1 Corinthians', '1 Cor,1 Co');
insert into bible_books (title, abbr) values('2 Corinthians', '2 Cor,2 Co');
insert into bible_books (title, abbr) values('Galatians', 'Gal,Ga');
insert into bible_books (title, abbr) values('Ephesians', 'Eph,Ephes');
insert into bible_books (title, abbr) values('Philippians', 'Phil,Php,Pp');
insert into bible_books (title, abbr) values('Colossians', 'Col,Co');
insert into bible_books (title, abbr) values('1 Thessalonians', '1 Thess,1 Thes,1 Th');
insert into bible_books (title, abbr) values('2 Thessalonians', '2 Thess,2 Thes,2 Th');
insert into bible_books (title, abbr) values('1 Timothy', '1 Tim,1 Ti');
insert into bible_books (title, abbr) values('2 Timothy', '2 Tim,2 Ti');
insert into bible_books (title, abbr) values('Titus', 'Tit,Ti');
insert into bible_books (title, abbr) values('Philemon', 'Philem,Phm,Pm');
insert into bible_books (title, abbr) values('Hebrews', 'Heb');
insert into bible_books (title, abbr) values('James', 'James,Jas,Jm');
insert into bible_books (title, abbr) values('1 Peter', '1 Pet,1 Pe,1 Pt,1 P');
insert into bible_books (title, abbr) values('2 Peter', '2 Pet,2 Pe,2 Pt,2 P');
insert into bible_books (title, abbr) values('1 John', '1 Jhn,1 Jn,1 J');
insert into bible_books (title, abbr) values('2 John', '2 Jhn,2 Jn,2 J');
insert into bible_books (title, abbr) values('3 John', '3 Jhn,3 Jn,3 J');
insert into bible_books (title, abbr) values('Jude', 'Jud,Jd');
insert into bible_books (title, abbr) values('Revelation', 'Rev,Re');
