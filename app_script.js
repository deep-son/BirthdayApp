function submitToLambda() {
  const formResponse = FormApp.getActiveForm().getResponses().pop();
  const formData = formResponse.getItemResponses().reduce((obj, itemResponse) => {
    obj[itemResponse.getItem().getTitle()] = itemResponse.getResponse();
    return obj;
  }, {});
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(formData)
  };
  
  console.log(formData)
  
  var response = UrlFetchApp.fetch('api_gateway_url', options);
  
  Logger.log(response.getContentText());

}