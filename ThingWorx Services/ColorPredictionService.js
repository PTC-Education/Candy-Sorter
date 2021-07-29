me.Red = Rin;
me.Green = Gin;
me.Blue = Bin;
me.Lux = Lin;
me.Temperature = Tin;

// create Infotable containing the features (properties) used for prediction
var modelFeatures = Resources["InfoTableFunctions"].CreateInfoTable({
	infoTableName: "modelFeatures" /* STRING */
});
// create the fields with the corresponding feature (property) name and description
modelFeatures.AddField({name:"name", baseType:"STRING"}); 
modelFeatures.AddField({name:"description", baseType:"STRING"});
// add a row for each feature (property)
modelFeatures.AddRow({name:"Red", description:""});
modelFeatures.AddRow({name:"Green", description:""});
modelFeatures.AddRow({name:"Blue", description:""});
modelFeatures.AddRow({name:"Lux", description:""});
modelFeatures.AddRow({name:"Temperature", description:""});

/*  
 *  datasetref InfoTable containing the features (properties) with their current values -> 
 *  based on theses values the prediction will be executed
 */ 
var datasetref = Resources["InfoTableFunctions"].CreateInfoTableFromDataShape({
	infoTableName: "datasetref" /* STRING */,
	dataShapeName: "AnalyticsDatasetRef" /* DATASHAPENAME */
});
// get all the property values from the properties specified in the modelFeatures Infotable
var data = me.GetNamedPropertyValues({
	propertyNames: modelFeatures /* INFOTABLE */
});
// write the properties with their values in the datasetref Infotable
datasetref.AddRow({data:data});

/*
 *  execute the prediction with the AnalyticsServer_PredictionThing RealtimeScore service
 *  predictiveScores: INFOTABLE; dataShape: "AnalyticsPredictionScores"
 */
var predictiveScores =  Things[me.AnalyticsServerString+"-AnalyticsServer_PredictionThing"].RealtimeScore({
	goalField: "Color" /* STRING */, 
	modelUri: "results:/models/"+me.ModelURI /* STRING */,  // change me!!
	datasetRef: datasetref /* INFOTABLE */,
});
// write the predicted goal to the me.Goal property
me.ColorPrediction = predictiveScores.rows[0].Color;
// return a Infotable containing the results of the prediction for the user
result = predictiveScores.rows[0].Color;