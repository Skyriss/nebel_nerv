#!/usr/bin/env python3
"""
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import hashlib

correct_key = "25ba2423dfad0f5c837cbd75aacc07f0"
melchior_uri = "http://melchior.farstone.ru:9876/rescue_key"

grant_page = """
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>MAGI 3.0 NERV contol centre</title>
    <style>
    .letters {

}

.letters ul {
  list-style:none;
  position:absolute;
  left: 50%;
  top:50%;

}
.letters ul li{
  display:inline-block;
  color:red;
font-size: 50px;
}

.letters ul li:nth-child(4),
.letters ul li:nth-child(5){
  color: red;
  transform: translateX(130%);
  
}

.letters svg{
  position:absolute;
  top:50%;
  left:50%;
  display:inline-block;
  transform: translateX(40%) 
translateY(10px);}

body {
  background-color:black;
}
    </style>
</head>
<body>
<div class='letters'>
    <svg width='120' height='120'>
  <path d="
M 30 0 115 110 Q120 70 
100 50 Q100 35 120 35 
120 25 95 5 
105 0 105 0 90 0 
95 5 95 5 105 0
105 0 90 0 " stroke="red" stroke-width="2" fill="none" />
    </svg>
 <ul>
   <li>N</li>
   <li>E</li>
   <br>
   <li>R</li>
   <li>V</li>
  </ul> 
 </div>
</body>
"""

balthazar_failure_page = """
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>MAGI 3.0 NERV contol centre</title>
    <style>
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 200;
  src: url(https://fonts.gstatic.com/s/sourcesanspro/v14/6xKydSBYKcSV-LCoeQqfX1RYOo3i94_wlxdr.ttf) format('truetype');
}
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 400;
  src: url(https://fonts.gstatic.com/s/sourcesanspro/v14/6xK3dSBYKcSV-LCoeQqfX1RYOo3qOK7g.ttf) format('truetype');
}
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 700;
  src: url(https://fonts.gstatic.com/s/sourcesanspro/v14/6xKydSBYKcSV-LCoeQqfX1RYOo3ig4vwlxdr.ttf) format('truetype');
}
body {
  background: #000;
  padding: 0;
  margin: 0;
  overflow: hidden;
  font-family: 'Source Sans Pro', arial, sans-serif;
}
.magi {
  position: absolute;
  z-index: -1;
  overflow: hidden;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  text-align: center;
}
.magi-wrapper {
  position: absolute;
  width: 2640px;
  left: 50%;
  margin-left: -1743px;
  right: 0;
  top: -75px;
  bottom: 0;
  padding: 0 14px;
}
.magi-message {
  width: 150px;
  height: 145px;
  display: inline-block;
  position: relative;
  perspective: 150px;
  margin: 6px -7px;
  color: #F00;
  text-align: center;
}
.magi-message:nth-child(even) {
  top: 81px;
}
.magi-message::before {
  content: '\\2B22';
  position: absolute;
  left: 0;
  right: 0;
  top: -12px;
  bottom: 12px;
  color: #000;
  z-index: -1;
  font-size: 240px;
  line-height: 125px;
  transform: rotate(90deg);
  text-shadow: 0 5px 0 #000, 4px -3px 0 #000, -4px -3px 0 #000, -4px 3px 0 #000, 4px 3px 0 #000, 0 -5px 0 #000, /* segundo nivel: rojo */ 0 8px 0 #F00, 7px -4px 0 #F00, -7px -4px 0 #F00, -7px 4px 0 #F00, 7px 4px 0 #F00, 0 -8px 0 #F00, /* tercer nivel: negro */ 0 12px 0 #000, 10px -6px 0 #000, -10px -6px 0 #000, -10px 6px 0 #000, 10px 6px 0 #000, 0 -12px 0 #000, /* cuarto nivel: rojo */ 0 15px 0 #F00, 13px -7px 0 #F00, -13px -7px 0 #F00, -13px 7px 0 #F00, 13px 7px 0 #F00, 0 -15px 0 #F00, /* quinto nivel: negro */ 0 17px 0 #000, 15px -9px 0 #000, -15px -9px 0 #000, -15px 9px 0 #000, 15px 9px 0 #000, 0 -17px 0 #000;
}
.magi-message-content {
  position: absolute;
  left: -19px;
  right: 0;
  top: 0;
  bottom: 0;
}
.magi-message-content span,
.magi-message-content strong {
  font-size: 16px;
  display: block;
  position: absolute;
  left: 0;
  right: 0;
}
.magi-message-content .top {
  top: 5px;
  line-height: 70px;
  letter-spacing: 8px;
}
.magi-message-content .center {
  top: 48px;
  font-size: 33px;
  line-height: 34px;
  height: 34px;
}
.magi-message-content .bottom {
  bottom: 45px;
}
.magi-message-content .triangle {
  opacity: 0;
  letter-spacing: 2px;
  left: 55px;
  font-size: 8px;
  line-height: 70px;
  oveflow: visible;
  width: 1px;
  height: 1px;
  border-bottom: 28px solid red;
  border-left: 30px solid transparent;
  border-right: 30px solid transparent;
  white-space: nowrap;
  text-indent: -18px;
}
.magi-message-content .triangle:before,
.magi-message-content .triangle:after {
  content: attr(title);
  display: block;
  position: absolute;
  line-height: 8px;
  top: 5px;
  text-indent: 0;
}
.magi-message-content .triangle:before {
  transform: rotate(-42deg);
  left: -39px;
}
.magi-message-content .triangle:after {
  top: 8px;
  transform: rotate(42deg);
  left: 3px;
}
.magi-message-content .triangle.bottom {
  transform: rotate(180deg);
  bottom: 20px;
}
.magi-error {
  color: #000;
}
.magi-error::before {
  color: #F00;
}
.magi-warning .magi-message-content .triangle {
  opacity: 1;
}

    </style>
</head>
<body>
<div class='magi'>
  <div class='magi-wrapper'>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>PRESENSE</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 2'>LEVEL 2</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 2'>LEVEL 2</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>ANGEL</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>BALTHAZAR FAILURE</span>
      </div>
    </div>
  </div>
</div>
</body>

"""

melchior_failure_page = """
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>MAGI 3.0 NERV contol centre</title>
    <style>
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 200;
  src: url(https://fonts.gstatic.com/s/sourcesanspro/v14/6xKydSBYKcSV-LCoeQqfX1RYOo3i94_wlxdr.ttf) format('truetype');
}
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 400;
  src: url(https://fonts.gstatic.com/s/sourcesanspro/v14/6xK3dSBYKcSV-LCoeQqfX1RYOo3qOK7g.ttf) format('truetype');
}
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 700;
  src: url(https://fonts.gstatic.com/s/sourcesanspro/v14/6xKydSBYKcSV-LCoeQqfX1RYOo3ig4vwlxdr.ttf) format('truetype');
}
body {
  background: #000;
  padding: 0;
  margin: 0;
  overflow: hidden;
  font-family: 'Source Sans Pro', arial, sans-serif;
}
.magi {
  position: absolute;
  z-index: -1;
  overflow: hidden;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  text-align: center;
}
.magi-wrapper {
  position: absolute;
  width: 2640px;
  left: 50%;
  margin-left: -1743px;
  right: 0;
  top: -75px;
  bottom: 0;
  padding: 0 14px;
}
.magi-message {
  width: 150px;
  height: 145px;
  display: inline-block;
  position: relative;
  perspective: 150px;
  margin: 6px -7px;
  color: #F00;
  text-align: center;
}
.magi-message:nth-child(even) {
  top: 81px;
}
.magi-message::before {
  content: '\\2B22';
  position: absolute;
  left: 0;
  right: 0;
  top: -12px;
  bottom: 12px;
  color: #000;
  z-index: -1;
  font-size: 240px;
  line-height: 125px;
  transform: rotate(90deg);
  text-shadow: 0 5px 0 #000, 4px -3px 0 #000, -4px -3px 0 #000, -4px 3px 0 #000, 4px 3px 0 #000, 0 -5px 0 #000, /* segundo nivel: rojo */ 0 8px 0 #F00, 7px -4px 0 #F00, -7px -4px 0 #F00, -7px 4px 0 #F00, 7px 4px 0 #F00, 0 -8px 0 #F00, /* tercer nivel: negro */ 0 12px 0 #000, 10px -6px 0 #000, -10px -6px 0 #000, -10px 6px 0 #000, 10px 6px 0 #000, 0 -12px 0 #000, /* cuarto nivel: rojo */ 0 15px 0 #F00, 13px -7px 0 #F00, -13px -7px 0 #F00, -13px 7px 0 #F00, 13px 7px 0 #F00, 0 -15px 0 #F00, /* quinto nivel: negro */ 0 17px 0 #000, 15px -9px 0 #000, -15px -9px 0 #000, -15px 9px 0 #000, 15px 9px 0 #000, 0 -17px 0 #000;
}
.magi-message-content {
  position: absolute;
  left: -19px;
  right: 0;
  top: 0;
  bottom: 0;
}
.magi-message-content span,
.magi-message-content strong {
  font-size: 16px;
  display: block;
  position: absolute;
  left: 0;
  right: 0;
}
.magi-message-content .top {
  top: 5px;
  line-height: 70px;
  letter-spacing: 8px;
}
.magi-message-content .center {
  top: 48px;
  font-size: 33px;
  line-height: 34px;
  height: 34px;
}
.magi-message-content .bottom {
  bottom: 45px;
}
.magi-message-content .triangle {
  opacity: 0;
  letter-spacing: 2px;
  left: 55px;
  font-size: 8px;
  line-height: 70px;
  oveflow: visible;
  width: 1px;
  height: 1px;
  border-bottom: 28px solid red;
  border-left: 30px solid transparent;
  border-right: 30px solid transparent;
  white-space: nowrap;
  text-indent: -18px;
}
.magi-message-content .triangle:before,
.magi-message-content .triangle:after {
  content: attr(title);
  display: block;
  position: absolute;
  line-height: 8px;
  top: 5px;
  text-indent: 0;
}
.magi-message-content .triangle:before {
  transform: rotate(-42deg);
  left: -39px;
}
.magi-message-content .triangle:after {
  top: 8px;
  transform: rotate(42deg);
  left: 3px;
}
.magi-message-content .triangle.bottom {
  transform: rotate(180deg);
  bottom: 20px;
}
.magi-error {
  color: #000;
}
.magi-error::before {
  color: #F00;
}
.magi-warning .magi-message-content .triangle {
  opacity: 1;
}

    </style>
</head>
<body>
<div class='magi'>
  <div class='magi-wrapper'>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>BREACH</strong>
        <span class='bottom'>DETECTED</span>
      </div>
    </div>
    <div class='magi-message magi-warning'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>WARNING</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
    <div class='magi-message'>
      <div class='magi-message-content'>
        <span class='top triangle' title='LEVEL 1'>LEVEL 1</span>
        <strong class='center'>&nbsp;</strong>
        <span class='bottom triangle' title='LEVEL 1'>LEVEL 1</span>
      </div>
    </div>
    <div class='magi-message magi-error'>
      <div class='magi-message-content'>
        <span class='top'>SECURITY</span>
        <strong class='center'>REFUSAL</strong>
        <span class='bottom'>MELCHIOR FAILURE</span>
      </div>
    </div>
  </div>
</div>
</body>

"""

def make_request(uri):
    raw_data = Req().make_request(url=uri, method="GET")
    logging.info("Got response from %s: %s", uri, raw_data) 
    try:

        return json.loads(raw_data)
    except (json.JSONDecodeError, KeyError) as err:
        logging.error("Got error while parsing json: %s", err)
        return

def is_access_granted():
    result = make_request(melchior_uri)
    if result and result.get("key"):
        if hashlib.md5(result["key"].encode("utf8")).hexdigest() == correct_key:
            logging.info("Recieved key mistmatch: {} {} {}".format(result["key"], hashlib.md5(result["key"].encode("utf8")).hexdigest(), correct_key))
            return True
    return False


def is_melchior_alive():
    result = make_request(melchior_uri)
    if result:
        return True
    return False

class Req:
    conn_timeout = 5
    retries = 0
    bad_statuses = [400, 409, 422, 500, 502, 503, 504]
    response_timeout = None
    allowed_methods = {'GET', 'DELETE', 'HEAD', 'PUT', 'OPTIONS', 'TRACE'}

    def _make_session(self):
        sess = requests.Session()
        retries = Retry(total=self.retries,
                        backoff_factor=self.conn_timeout,
                        status_forcelist=self.bad_statuses)
        retries.allowed_methods = self.allowed_methods
        sess.mount('http://', HTTPAdapter(max_retries=retries))
        sess.mount('https://', HTTPAdapter(max_retries=retries))
        return sess

    def make_request(self, url, method="GET", headers=None, data=None, params=None):
        if not headers:
            headers = {"Content-Type": "application/json"}

        session = self._make_session()
        try:
            req = session.request(url=url, method=method, timeout=self.response_timeout,
                                  data=data, params=params, headers=headers)
        except requests.RequestException as err:
            logging.warning("%s", err)
            return ""
        if req.status_code not in [200, 201, 204]:
            header_logs = headers.copy()
            header_logs["Authorization"] = "<token masked>"
            logging.warning("I've got %s  HTTP Code for %s with data: %s, params: %s, headers: %s, text %s",
                            req.status_code,
                            url,
                            data,
                            params,
                            header_logs,
                            req.text)
        return req.text

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        if is_access_granted():
            self.wfile.write(grant_page.encode('utf-8'))
            return
        if is_melchior_alive():
            self.wfile.write(balthazar_failure_page.encode('utf-8'))
            return
        self.wfile.write(melchior_failure_page.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
