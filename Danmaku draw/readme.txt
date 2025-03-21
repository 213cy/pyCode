# https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/grpc_api/bilibili/community/service/dm/v1/dm.proto
# https://github.com/XavierJiezou/python-danmu-analysis/tree/master

key = (field_number << 3) | wire_type



syntax = "proto3";

package bilibili.community.service.dm.v1;

// 弹幕条目
message DanmakuElem {
    // 弹幕dmid
    int64 id = 1;
    // 弹幕出现位置(单位ms)
    int32 progress = 2;
    // 弹幕类型 1 2 3:普通弹幕 4:底部弹幕 5:顶部弹幕 6:逆向弹幕 7:高级弹幕 8:代码弹幕 9:BAS弹幕(pool必须为2)
    int32 mode = 3;
    // 弹幕字号
    int32 fontsize = 4;
    // 弹幕颜色
    uint32 color = 5;
    // 发送者mid hash
    string midHash = 6;
    // 弹幕正文
    string content = 7;
    // 发送时间
    int64 ctime = 8;
    // 权重 用于屏蔽等级 区间:[1,10]
    int32 weight = 9;
    // 动作
    string action = 10;
    // 弹幕池 0:普通池 1:字幕池 2:特殊池(代码/BAS弹幕)
    int32 pool = 11;
    // 弹幕dmid str
    string idStr = 12;
    // 弹幕属性位(bin求AND)
    // bit0:保护 bit1:直播 bit2:高赞
    int32 attr = 13;
    //
    string animation = 22;
    // 大会员专属颜色
    DmColorfulType colorful = 24;
}