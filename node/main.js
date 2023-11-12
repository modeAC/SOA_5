var http = require('http');
var os = require('os');

var server = http.createServer(function (req, res) {

    if (req.url == '/') {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.write(`Node pod: ${process.env.POD_NAME}, Time: ${new Date().toISOString()}`);
            res.end();
    }
});

server.listen(5000);

console.log('Node.js server at port 5000 is running...')