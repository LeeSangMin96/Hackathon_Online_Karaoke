var express = require('express'),
    http=require('http'),
    path=require('path');

var static = require('serve-static');

var cors = require('cors');

//const http = require('http');
const os = require('os');
const socketIO = require('socket.io');

var bodyParser = require('body-parser');

const PORT = process.env.PORT || 3000;

var app = express();

app.set("port", PORT);

app.use('/', static(path.join(__dirname, 'public')));

app.use(bodyParser.urlencoded({ extends: true }));
app.use(bodyParser.json());

var router = express.Router();

app.use(cors());

app.get("/", function(req, res){ 
    res.header("Access-Control-Allow-Origin", "*");
    res.sendFile(path.join(__dirname, '/public/rtc.html'));
});

app.get("/home", function(req, res){ 
    res.sendFile(path.join(__dirname, '/public/THIS_IS_FINAL/home.html'));
});

app.post("/get_url", function(req, res){
    console.log('babo');
    console.log(req.body.title+', '+req.body.singer);
    var spawn = require('child_process').spawn,
    py = spawn('python', ['mytube.py']),
    data = [req.body.title+' '+req.body.demo_singer+' karaoke'],
    dataString = '';

    py.stdout.on('data', function(data){ // py 쪽으로부터 data가 오면 callback
        dataString += data.toString();
    });
    py.stdout.on('end', function(){ // py 쪽으로부터 end가 오면 callback
        console.log('Sum of numbers=',dataString);
        return res.send({result:dataString});
    });
    py.stdin.write(JSON.stringify(data));// paramter를 data로 하여 python 모듈을 호출함
    py.stdin.end();
    
});

//app.get("/alone", function(req, res){ 
//    console.log(__dirname);
//    res.sendFile(path.join(__dirname, '/public/THIS_IS_FINAL/alone.html'));
//    
//});

var server = http.createServer(app);

var io = socketIO.listen(server);

io.sockets.on('connection',socket=>{
    function log() {
        let array = ['Message from server:'];
        array.push.apply(array,arguments);
        socket.emit('log',array);
    }

    socket.on('message',message=>{
        log('Client said : ' ,message);
        socket.broadcast.emit('message',message);
    });

    socket.on('create or join',room=>{
        let clientsInRoom = io.sockets.adapter.rooms[room];
        let numClients = clientsInRoom ? Object.keys(clientsInRoom.sockets).length : 0;
        log('Room ' + room + ' now has ' + numClients + ' client(s)');
        
        if(numClients === 0){
            console.log('create room!');
            socket.join(room);
            log('Client ID ' + socket.id + ' created room ' + room);
            socket.emit('created',room,socket.id);
        }
        else if(numClients===1){
            console.log('join room!');
            log('Client Id' + socket.id + 'joined room' + room);
            io.sockets.in(room).emit('join',room);
            socket.join(room);
            socket.emit('joined',room,socket.id);
            io.sockets.in(room).emit('ready');
        }else{
            socket.emit('full',room);
        }
    });


});

server.listen(app.get('port'),function(){
    console.log('익스프레스 서버를 시작했습니다. : '+app.get('port'));
});