package com.hyphenate.chatuidemo.cache;

import com.avos.avoscloud.AVClassName;
import com.avos.avoscloud.AVObject;

/**
 * Created by Martin on 2017/4/26.
 */
@AVClassName("UserWebInfo")
public class UserWebInfo extends AVObject {
    public String getOpenId() {
        return getString("openId");
    }
    public void setOpenId(String value) {
        put("openId", value);
    }

    public String getNickName() {
        return getString("nickName");
    }
    public void setNickName(String value) {
        put("nickName", value);
    }

    public String getAvatarUrl() {
        return getString("avatarUrl");
    }
    public void setAvatarUrl(String value) {
        put("avatarUrl", value);
    }
}
