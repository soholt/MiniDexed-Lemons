import express from 'express';
import { createServer } from 'https';
import { readFileSync } from 'fs';
import { WebSocketServer } from 'ws';

//import conf from 'lemons.json'

import { readFile } from 'fs/promises';
const conf = JSON.parse(
  await readFile(
    new URL('./lemons.json', import.meta.url)
  )
)['local'];
//console.log('conf',conf)


/**
 * MiniDexedLemons localServer.js
 * @TODO Net Midi && ble? jzz?
 * @TODO move ssl gen to node and automate? https://github.com/digitalbazaar/forge
 */

/**
 * UART
 */
import { SerialPort, ReadlineParser } from 'serialport';

/**
 * Called on UART RX
 * @param {*} dat 
 */
function RX_UART(dat) {
  if (conf.dev) console.log('--> RX_UART', dat)
  // Send it to Websocket
  //ws.send(dat)
}

if (conf.uart_midi) {
  const serial = new SerialPort({ path: conf.uart_port, baudRate: conf.uart_rate })
  //const { SerialPort, ReadlineParser } = require('serialport') //DelimiterParser, 
  
  //const { DelimiterParser } = require('@serialport/parser-delimiter')
  

  //const parser = serial.pipe(new DelimiterParser({ delimiter: 0xF7 }))

  const parser = new ReadlineParser()
  serial.pipe(parser)
  //parser.on('--> RX_UART', console.log)
  parser.on('--> RX_UART', RX_UART)
}

/**
 * Write to UART
 * @param {*} dat 
 */
function TX_UART(dat) {
  if (conf.dev) console.log('<-- TX_UART', dat)
  if (conf.uart_midi) serial.write(dat)
}

/**
 * Static web server and web socket
 */
const app = express()
app.use(express.static('www'))
app.use('/www/assets', express.static('assets'))
/*
app.get('*.js', function(req, res, next) {
  req.url = req.url + '.gz';
  res.set('Content-Encoding', 'gzip');
  res.set('Content-Type', 'text/javascript');
  next();
});
app.get('*.css', function(req, res, next) {
  req.url = req.url + '.gz';
  res.set('Content-Encoding', 'gzip');
  res.set('Content-Type', 'text/css');
  next();
});
app.get('*.html', function(req, res, next) {
  req.url = req.url + '.gz';
  res.set('Content-Encoding', 'gzip');
  res.set('Content-Type', 'text/html');
  next();
});
*/
const server = createServer({
  cert: readFileSync('minidexed.crt'),
  key: readFileSync('minidexed.key'),
  //port: conf.port
}, app);


/**
 * Called on web socket data
 * @param {*} dat 
 */
function RX_WS(dat) {
  if (conf.dev) console.log('----> RX_WS', dat)
  // Send it to UART
  if(conf.tx_uart) TX_UART(dat)
}
const wss = new WebSocketServer({ server, path: '/wss' });

wss.on('connection', function connection(ws) {
  ws.on('error', console.error);

  ws.on('message', function message(data) {
  //  //console.log('received: %s', data);
    RX_WS(data)
  });

  //ws.send('something');
});

server.listen(conf.www_port);


console.log(`--- MinidexedLemon ---`)
console.log(`https://localhost:${conf.www_port}`)
console.log(`Ctrl + c to exit..`)
