python -m http.server 8001

===========================================

Video.js - HTML5 Video Player 
https://github.com/videojs/video.js
Video.js CDN
https://unpkg.com/browse/video.js@8.11.8/dist/
https://vjs.zencdn.net/8.3.0/video.min.js
files in Video.js distribution package
https://videojs.com/getting-started/#distributions

移动端的浏览器video标签原生支持 m3u8 直接播放
pc端需要 vhs 或是 hls 才能播放
所以pc端有几种方案播放 m3u8
1, videojs 7.0 以下版本 + vhs
<script src="video.core.min.js"></script>
<script src="videojs-http-streaming.min.js"></script>
2, videojs 7.0 以上版本
<link href="http://vjs.zencdn.net/7.0/video-js.min.css" rel="stylesheet">
<script src="http://vjs.zencdn.net/7.0/video.min.js"></script>
3, hls

videojs-http-streaming (VHS) Included in video.js 7 by default!
https://github.com/videojs/http-streaming
VHS from the CDN 
https://unpkg.com/browse/@videojs/http-streaming@3.10.0/

HLS
https://github.com/videojs/videojs-contrib-hls
videojs-contrib-hls will be deprecated and is succeeded by videojs-http-streaming(VHS).

===========================================

video.js simple-embed examples
https://unpkg.com/browse/video.js@8.11.8/dist/examples/simple-embed/index.html 