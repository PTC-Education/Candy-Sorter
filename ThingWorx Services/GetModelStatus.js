// jobInfo: INFOTABLE dataShape: "AnalyticsJobInfo"
result = Things[me.AnalyticsServerString+"-AnalyticsServer_TrainingThing"].GetJobInfo({
	jobId: me.ModelURI /* STRING */
});