/*
    https://tool.qianduange.cn/bili_danmu
	Modified By shaffer
*/
/*
https://github.com/MoePus/bilibili_danmaku_AntiAnonym/blob/master/crcRevEng.js
https://github.com/esterTion/BiliBili_crc2mid/blob/master/crc32.htm
https://github.com/cwuom/GetDanmuSender/blob/main/main.py
*/

var BiliBili_midcrc = function() {
    'use strict';
    const CRCPOLYNOMIAL = 0xEDB88320;
    var startTime = new Date().getTime()
      , crctable = new Array(256)
      , create_table = function() {
        var crcreg, i, j;
        for (i = 0; i < 256; ++i) {
            crcreg = i;
            for (j = 0; j < 8; ++j) {
                if ((crcreg & 1) != 0) {
                    crcreg = CRCPOLYNOMIAL ^ (crcreg >>> 1);
                } else {
                    crcreg >>>= 1;
                }
            }
            crctable[i] = crcreg;
        }
    }
      , crc32 = function(input) {
        if (typeof (input) != 'string')
            input = input.toString();
        var crcstart = 0xFFFFFFFF, len = input.length, index;
        for (var i = 0; i < len; ++i) {
            index = (crcstart ^ input.charCodeAt(i)) & 0xff;
            crcstart = (crcstart >>> 8) ^ crctable[index];
        }
        return crcstart;
    }
      , crc32lastindex = function(input) {
        if (typeof (input) != 'string')
            input = input.toString();
        var crcstart = 0xFFFFFFFF, len = input.length, index;
        for (var i = 0; i < len; ++i) {
            index = (crcstart ^ input.charCodeAt(i)) & 0xff;
            crcstart = (crcstart >>> 8) ^ crctable[index];
        }
        return index;
    }
      , getcrcindex = function(t) {
        //if(t>0)
        //t-=256;
        for (var i = 0; i < 256; i++) {
            if (crctable[i] >>> 24 == t)
                return i;
        }
        return -1;
    }
      , deepCheck = function(i, index) {
        var tc = 0x00
          , str = ''
          , hash = crc32(i);
        tc = hash & 0xff ^ index[2];
        if (!(tc <= 57 && tc >= 48))
            return [0];
        str += tc - 48;
        hash = crctable[index[2]] ^ (hash >>> 8);
        tc = hash & 0xff ^ index[1];
        if (!(tc <= 57 && tc >= 48))
            return [0];
        str += tc - 48;
        hash = crctable[index[1]] ^ (hash >>> 8);
        tc = hash & 0xff ^ index[0];
        if (!(tc <= 57 && tc >= 48))
            return [0];
        str += tc - 48;
        hash = crctable[index[0]] ^ (hash >>> 8);
        return [1, str];
    };
    create_table();
    var index = new Array(4);
    console.log('初始化耗时：' + (new Date().getTime() - startTime) + 'ms');
    return function(input) {
        var ht = parseInt('0x' + input) ^ 0xffffffff, snum, i, lastindex, deepCheckData;
        for (i = 3; i >= 0; i--) {
            index[3 - i] = getcrcindex(ht >>> (i * 8));
            snum = crctable[index[3 - i]];
            ht ^= snum >>> ((3 - i) * 8);
        }
        for (i = 0; i < 100000000; i++) {
            lastindex = crc32lastindex(i);
            if (lastindex == index[3]) {
                deepCheckData = deepCheck(i, index)
                if (deepCheckData[0])
                    break;
            }
        }

        if (i == 100000000)
            return -1;
        console.log('总耗时：' + (new Date().getTime() - startTime) + 'ms');
        return i + '' + deepCheckData[1];
    }
}
console.log(0xefb3f424 ^ 0xEDB88320)
getuid = BiliBili_midcrc()
startTime = new Date().getTime()
a = getuid('efb3f424')
console.log(a);
//efb3f424 1647605377
console.log('==========================');
// =========================================
