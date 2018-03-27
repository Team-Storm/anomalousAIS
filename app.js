//const fs =  require('fs');
//var obj = require('./hello.csv');
//var hello = require()
//obj.from.path('hello.csv');
/* 1)var data = fs.open('hello.csv', 'r', (err, fd) => {
  if (err) throw err;
  else{
  	var file = JSON.stringify(data);
  }
});*/

/* 2) const csvFilePath='hello.csv';
const csv=require('csvtojson');
var file = csv()
.fromFile(csvFilePath)
.on('json',(jsonObj)=>{
    // combine csv header row and csv line to a json object
    // jsonObj.a ==> 1 or 4
})
.on('done',(error)=>{
    console.log('end')
})
*/
var zerorpc = require("zerorpc");
var fs = require('fs');
var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");
var file = fs.readFile( __dirname + '/iris.csv', function (err, data) {
  if (err) {
    throw err; 
  }
  //                    converting csv to string!
  client.invoke("hello",data.toString(), function(error, res, more) {
    console.log(res);
});
});
