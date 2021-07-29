var learners = Resources["InfoTableFunctions"].CreateInfoTableFromDataShape( {infoTableName : "learners", dataShapeName : "AnalyticsTrainingLearner"});
learners.AddRow({learningTechnique: "NEURAL_NET"});
learners.AddRow({learningTechnique: "GRADIENT_BOOST"});
learners.AddRow({learningTechnique: "LINEAR_REGRESSION"});
learners.AddRow({learningTechnique: "DECISION_TREE"});

var datasetref = Resources["InfoTableFunctions"].CreateInfoTableFromDataShape({
	infoTableName: "datasetref" /* STRING */,
	dataShapeName: "AnalyticsDatasetRef" /* DATASHAPENAME */
});
datasetref.data = trainingData;
datasetref.metadata = metadataInput;

me.ModelURI =  Things[me.AnalyticsServerString+"-AnalyticsServer_TrainingThing"].CreateJob({
	jobName: "Training job started from Generic_Analytics_Thing" /* STRING */,
	learners: learners /* INFOTABLE */,
	goalField: goal /* STRING */,
	datasetRef: datasetref /* INFOTABLE */,
    confidenceLevel: undefined /* NUMBER */,
	maxAllowedFields: undefined /* INTEGER */,
	description: undefined /* STRING */,
	ensembleTechnique: "ELITE_AVERAGE" /* STRING */,
	useRedundancyFilter: undefined /* BOOLEAN */,
	anomalyDetectionParams: undefined /* INFOTABLE */,
	tags: undefined /* INFOTABLE */,
	validationHoldoutPercentage: undefined /* NUMBER */,
	lookahead: undefined /* INTEGER */,
	comparisonMetric: "RMSE" /* STRING */,
	samplingParams: undefined /* INFOTABLE */,
	createConfidenceModel: false /* BOOLEAN */,
	virtualSensor: false /* BOOLEAN */,
	lookbackSize: undefined /* INTEGER */
});

result = me.ModelURI;