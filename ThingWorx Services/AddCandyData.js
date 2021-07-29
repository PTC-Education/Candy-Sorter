me.R = inR;
me.G = inG;
me.B = inB;
me.T = inT;
me.L = inL;
me.ColorTag = inColor;
me.CandyNum = me.CandyNum + 1;
    
// tags:TAGS
let tags = new Array();

// values:INFOTABLE(Datashape: ColorTrainingData)
let values = Things[me.name].CreateValues();
values.Red = inR; // INTEGER
values.Temperature = inT; // NUMBER
values.Blue = inB; // INTEGER
values.CandyNumber = me.CandyNum; // INTEGER [Primary Key]
values.Color = inColor; // STRING [Primary Key]
values.Green = inG; // INTEGER
values.Lux = inL; // NUMBER

// location:LOCATION
let location = {
    latitude: 0,
    longitude: 0,
    elevation: 0,
    units: "WGS84"
};

let params = {
	tags: tags,
	source: me.name,
	values: values,
	location: location
};

// AddOrUpdateDataTableEntry(tags:TAGS, source:STRING("me.name"), values:INFOTABLE(SkittleTraining1), location:LOCATION):STRING
let id = Things[me.name].AddOrUpdateDataTableEntry(params);

