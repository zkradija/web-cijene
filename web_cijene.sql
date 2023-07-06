use master
go

create database WebCijene collate SQL_Croatian_CP1250_CI_AS
go

use WebCijene
go

create table Valuta (
ValutaId smallint primary key identity (1,1),
Naziv varchar(40) not null,
Naziv2 varchar(40) not null,
IsoAlpha3 char(3) not null,
Oznaka char (3) not null
)


create table Drzava (
DrzavaId smallint primary key identity (1,1),
Naziv varchar(60) not null,
NazivEng varchar(60) not null,
IsoAlpha2 char(2) not null,
IsoAlpha3 char(3) not null,
Oznaka char(3) not null,
ValutaId smallint,
IndEU bit default 0,
constraint FK_ValutaId foreign key (ValutaId) references Valuta(ValutaId)
)

create table Trgovina (
TrgovinaId smallint primary key identity (1,1),
Naziv varchar (50),
DrzavaId smallint not null,
IndA tinyint default 1,
constraint FK_DrzavaId foreign key (DrzavaId) references Drzava(DrzavaId)
)


create table Cijene (
	CijeneId int identity (1,1) primary key,
	TrgovinaId smallint not null,
	Datum date not null,
	Poveznica varchar(512),
	Kategorija varchar (10) not null,
	Sifra varchar(100),
	Naziv varchar (256) not null,
	Cijena decimal (10,2)
	constraint FK_WebMjestoId foreign key (WebMjestoId) references WebMjesto(WebMjestoId),
	constraint FK_TrgovinaId foreign key (TrgovinaId) references Trgovina(TrgovinaId)
)


create table GrupaMat (
GrupaMatId int primary key identity (1,1),
Sifra char(6) not null,
Naziv varchar (100) not null
)


create table Proizvodi (
ProizvodiId int primary key identity (1,1),
Sifra char(20),
Naziv varchar (256) not null,
EanKom varchar (13),
Status char (2),
GrupaMatId int
constraint FK_GrupaMatId foreign key (GrupaMatId) references GrupaMat(GrupaMatId)
)

create table WebProizvodi (
WebProizvodiId int primary key identity (1,1),
Sifra char(20),
Naziv varchar (256) not null,
ProizvodiId int,
GrupaMatId int,
constraint FK_Proizvodi_WebProizvodi foreign key (ProizvodiId) references Proizvodi(ProizvodiId)
constraint FK_GrupaMatId foreign key (GrupaMatId) references GrupaMat(GrupaMatId)
)




insert into Valuta (Naziv,Naziv2,IsoAlpha3,Oznaka) values 
	('afgan','Afghani','AFN','971'),
	('lek','Lek','ALL','008'),
	('al�irski dinar','Algerian Dinar','DZD','012'),
	('ameri�ki dolar','US Dollar','USD','840'),
	('euro','Euro','EUR','978'),
	('kvanza','Kwanza','AOA','973'),
	('isto�nokaripski dolar','East Caribbean Dollar','XCD','951'),
	('argentinski pezo','Argentine Peso','ARS','032'),
	('armenski dram','Armenian Dram','AMD','051'),
	('arupski florin','Aruban Florin','AWG','533'),
	('australski dolar','Australian Dollar','AUD','036'),
	('azerbajd�anski manat','Azerbaijan Manat','AZN','944'),
	('bahamski dolar','Bahamian Dollar','BSD','044'),
	('bahreinski dinar','Bahraini Dinar','BHD','048'),
	('taka','Taka','BDT','050'),
	('barbadoski dolar','Barbados Dollar','BBD','052'),
	('belizeanski dolar','Belize Dollar','BZD','084'),
	('CFA franak BCEAO','CFA Franc BCEAO','XOF','952'),
	('bermudski dolar','Bermudian Dollar','BMD','060'),
	('bjeloruski rubalj','Belarusian Ruble','BYN','933'),
	('pula','Pula','BWP','072'),
	('bolivijano','Boliviano','BOB','068'),
	('konvertibilna marka','Convertible Mark','BAM','977'),
	('brazilski real','Brazilian Real','BRL','986'),
	('brunejski dolar','Brunei Dollar','BND','096'),
	('bugarski lev','Bulgarian Lev','BGN','975'),
	('burundski franak','Burundi Franc','BIF','108'),
	('ngultrum','Ngultrum','BTN','064'),
	('nizozemskoantilski gulden','Netherlands Antillean Guilder','ANG','532'),
	('CFA franak BEAC','CFA Franc BEAC','XAF','950'),
	('�e�ka kruna','Czech Koruna','CZK','203'),
	('�ileanski pezo','Chilean Peso','CLP','152'),
	('danska kruna','Danish Krone','DKK','208'),
	('dominikanski pezo','Dominican Peso','DOP','214'),
	('d�ibutski franak','Djibouti Franc','DJF','262'),
	('egipatska funta','Egyptian Pound','EGP','818'),
	('nakfa','Nakfa','ERN','232'),
	('lilangeni','Lilangeni','SZL','748'),
	('etiopski bir','Ethiopian Birr','ETB','230'),
	('falklandska funta','Falkland Islands Pound','FKP','238'),
	('fid�ijski dolar','Fiji Dollar','FJD','242'),
	('filipinski pezo','Philippine Peso','PHP','608'),
	('CFP franak','CFP Franc','XPF','953'),
	('dalasi','Dalasi','GMD','270'),
	('ganski cedi','Ghana Cedi','GHS','936'),
	('gibraltarska funta','Gibraltar Pound','GIP','292'),
	('lari','Lari','GEL','981'),
	('funta sterlinga','Pound Sterling','GBP','826'),
	('gvajanski dolar','Guyana Dollar','GYD','328'),
	('kvecal','Quetzal','GTQ','320'),
	('gvinejski franak','Guinean Franc','GNF','324'),
	('gourd','Gourde','HTG','332'),
	('lempira','Lempira','HNL','340'),
	('hongkon�ki dolar','Hong Kong Dollar','HKD','344'),
	('indijska rupija','Indian Rupee','INR','356'),
	('rupija','Rupiah','IDR','360'),
	('ira�ki dinar','Iraqi Dinar','IQD','368'),
	('iranski rijal','Iranian Rial','IRR','364'),
	('islandska kruna','Iceland Krona','ISK','352'),
	('novi izraelski �ekel','New Israeli Sheqel','ILS','376'),
	('jamaj�anski dolar','Jamaican Dollar','JMD','388'),
	('jen','Yen','JPY','392'),
	('jemenski rijal','Yemeni Rial','YER','886'),
	('jordanski dinar','Jordanian Dinar','JOD','400'),
	('ju�nosudanska funta','South Sudanese Pound','SSP','728'),
	('rand','Rand','ZAR','710'),
	('kajmanski dolar','Cayman Islands Dollar','KYD','136'),
	('rijal','Riel','KHR','116'),
	('kanadski dolar','Canadian Dollar','CAD','124'),
	('katarski rijal','Qatari Rial','QAR','634'),
	('tenge','Tenge','KZT','398'),
	('kenijski �iling','Kenyan Shilling','KES','404'),
	('juan renminbi','Yuan Renminbi','CNY','156'),
	('som','Som','KGS','417'),
	('kolumbijski pezo','Colombian Peso','COP','170'),
	('komorski franak','Comorian Franc','KMF','174'),
	('kongoanski franak','Congolese Franc','CDF','976'),
	('sjevernokorejski von','North Korean Won','KPW','408'),
	('von','Won','KRW','410'),
	('kostarikanski kolon','Costa Rican Colon','CRC','188'),
	('kubanski pezo','Cuban Peso','CUP','192'),
	('novozelandski dolar','New Zealand Dollar','NZD','554'),
	('kuvajtski dinar','Kuwaiti Dinar','KWD','414'),
	('lao kip','Lao Kip','LAK','418'),
	('loti','Loti','LSL','426'),
	('libanonska funta','Lebanese Pound','LBP','422'),
	('liberijski dolar','Liberian Dollar','LRD','430'),
	('libijski dinar','Libyan Dinar','LYD','434'),
	('�vicarski franak','Swiss Franc','CHF','756'),
	('malga�ki arijari','Malagasy Ariary','MGA','969'),
	('forinta','Forint','HUF','348'),
	('pataka','Pataca','MOP','446'),
	('malavi kva�a','Malawi Kwacha','MWK','454'),
	('rufija','Rufiyaa','MVR','462'),
	('malezijski ringit','Malaysian Ringgit','MYR','458'),
	('marokanski dirham','Moroccan Dirham','MAD','504'),
	('mauricijska rupija','Mauritius Rupee','MUR','480'),
	('ouguja','Ouguiya','MRU','929'),
	('meksi�ki pezo','Mexican Peso','MXN','484'),
	('kjat','Kyat','MMK','104'),
	('moldavski lej','Moldovan Leu','MDL','498'),
	('tugrik','Tugrik','MNT','496'),
	('mozambijski metikal','Mozambique Metical','MZN','943'),
	('nepalska rupija','Nepalese Rupee','NPR','524'),
	('naira','Naira','NGN','566'),
	('kordoba oro','C�rdoba Oro','NIO','558'),
	('norve�ka kruna','Norwegian Krone','NOK','578'),
	('omanski rijal','Rial Omani','OMR','512'),
	('pakistanska rupija','Pakistan Rupee','PKR','586'),
	('balboa','Balboa','PAB','590'),
	('kina','Kina','PGK','598'),
	('gvarani','Guarani','PYG','600'),
	('sol','Sol','PEN','604'),
	('zloti','Zloty','PLN','985'),
	('ruandski franak','Rwanda Franc','RWF','646'),
	('rumunjski leu','Romanian Leu','RON','946'),
	('ruski rubalj','Russian Ruble','RUB','643'),
	('salvadorski kolon ','El Salvador Colon','SVC','222'),
	('tala','Tala','WST','882'),
	('saudijski rijal','Saudy Riyal','SAR','682'),
	('sej�elska rupija','Seychelles Rupee','SCR','690'),
	('leone','Leone','SLE','925'),
	('singapurski dolar','Singapore Dollar','SGD','702'),
	('sirijska funta','Syrian Pound','SYP','760'),
	('sjeverno-makedonski denar','North Macedonia Denar','MKD','807'),
	('solomonskooto�ni dolar','Solomon Islands Dollar','SBD','090'),
	('somalijski �iling','Somali Shilling','SOS','706'),
	('srpski dinar','Serbian Dinar','RSD','941'),
	('sudanska funta','Sudanese Pound','SDG','938'),
	('surinamski dolar','Surinam Dollar','SRD','968'),
	('svetohelenska funta','St. Helena Pound','SHP','654'),
	('dobra','Dobra','STN','930'),
	('�rilanska rupija','Sri Lanka Rupee','LKR','144'),
	('�vedska kruna','Swedish Krona','SEK','752'),
	('somoni','Somoni','TJS','972'),
	('baht','Baht','THB','764'),
	('novotajvanski dolar','New Taiwan Dollar','TWD','901'),
	('tanzanijski �iling','Tanzanian Shilling','TZS','834'),
	('paanga','Paanga','TOP','776'),
	('trinidadtoba�ki dolar','Trinidad and Tobago Dollar','TTD','780'),
	('tuniski dinar','Tunisian Dinar','TND','788'),
	('turkmenistanski novi manat','Turkmenistan New Manat','TMT','934'),
	('turska lira','Turkish Lira','TRY','949'),
	('ugandski �iling','Uganda Shilling','UGX','800'),
	('UAE dirham','UAE Dirham','AED','784'),
	('hrivnja','Hryvnia','UAH','980'),
	('urugvajski pezo','Peso Uruguayo','UYU','858'),
	('uzbekistanski sum ','Uzbekistan Sum','UZS','860'),
	('vatu','Vatu','VUV','548'),
	('bolivarijanski soberano','Bolivar Soberano','VES','928'),
	('dong','Dong','VND','704'),
	('zambijska kva�a','Zambian Kwacha','ZMW','967'),
	('zelenortski eskudo','Cabo Verde Escudo ','CVE','132'),
	('zimbabveanski dolar','Zimbabwe Dollar','ZWL','932')


insert into Drzava (Naziv,NazivEng,IsoAlpha2,IsoAlpha3,Oznaka,ValutaId,IndEu) values
	('Austrija','Austria','AT','AUT','040',5,1),
	('Belgija','Belgium','BE','BEL','056',5,1),
	('Bosna i Hercegovina','Bosnia and Herzegovina','BA','BIH','070',23,0),
	('Cipar','Cyprus','CY','CYP','196',5,1),
	('Crna Gora','Montenegro       ','ME','MNE','499',5,0),
	('�e�ka','Czechia','CZ','CZE','203',31,1),
	('Danska','Denmark','DK','DNK','208',33,1),
	('Estonija','Estonia','EE','EST','233',5,1),
	('Finska','Finland','FI','FIN','246',5,1),
	('Francuska','France','FR','FRA','250',5,1),
	('Gr�ka','Greece','GR','GRC','300',5,1),
	('Hrvatska','Croatia','HR','HRV','191',5,1),
	('Irska','Ireland','IE','IRL','372',5,1),
	('Italija','Italy','IT','ITA','380',5,1),
	('Latvija','Latvia','LV','LVA','428',5,1),
	('Litva','Lithuania','LT','LTU','440',5,1),
	('Luksemburg','Luxembourg','LU','LUX','442',5,1),
	('Ma�arska','Hungary','HU','HUN','348',91,1),
	('Malta','Malta','MT','MLT','470',5,1),
	('Nizozemska','Netherlands','NL','NLD','528',5,1),
	('Njema�ka','Germany','DE','DEU','276',5,1),
	('Poljska','Poland','PL','POL','616',114,1),
	('Portugal','Portugal','PT','PRT','620',5,1),
	('Rumunjska','Romania','RO','ROU','642',116,1),
	('Sjeverna Makedonija','North Macedonia','MK','MKD','807',125,0),
	('Slova�ka','Slovakia','SK','SVK','703',5,1),
	('Slovenija','Slovenia','SI','SVN','705',5,1),
	('Srbija ','Serbia ','RS','SRB','688',128,0),
	('�panjolska','Spain','ES','ESP','724',5,1),
	('�vedska','Sweden','SE','SWE','752',134,1)


insert into Trgovina (Naziv,DrzavaId) values 
	('Konzum',12),
	('Mercator',27),
	('IDEA',28),
	('Maxi',28),
	('Univerexport',28),
	('Tempo',28),
	('DIS Rakovica',28),
	('Roda',28),
	('Lidl',28),
	('Boso',12),
	('Interspar',12),
	('Kaufland',12),
	('Lidl',12),
	('NTL',12),
	('Plodine',12),
	('SPAR',12),
	('Studenac',12),
	('Spar',27),
	('Tu�',27),
	('VOLI trade',5),
	('Konzum',3),
	('Reptil DOOEL',25)

if not exists (select * from sys.server_principals where type_desc='SQL_LOGIN' and name = N'webcijene')
create login webcijene with password = 'webcijene123!'
go

drop user if exists webcijene
go

create user webcijene for login webcijene
alter role db_datawriter add member webcijene
alter role db_datareader add member webcijene