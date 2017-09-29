package com.hyphenate.chatuidemo.cache;

import android.util.Log;

import com.google.gson.Gson;
import com.hyphenate.chat.EMClient;
import com.hyphenate.chat.EMMessage;
import com.hyphenate.easeui.domain.EaseUser;
import com.j256.ormlite.dao.Dao;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 用户缓存管理类
 * Created by Martin on 2017/4/24.
 */
public class UserCacheManager {

    /**
     * 消息扩展属性
     */
    private static final String kChatUserId = "ChatUserId";// 环信ID
    private static final String kChatUserNick = "ChatUserNick";// 昵称
    private static final String kChatUserPic = "ChatUserPic";// 头像Url

    /**
     * 获取所有用户信息
     * @return
     */
    public static List<UserCacheInfo> getAll(){
        Dao<UserCacheInfo, Integer> dao = SqliteHelper.getInstance().getUserDao();
        try {
            List<UserCacheInfo> list = dao.queryForAll();
            return list;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    /**
     * 获取用户信息
     * @param userId 用户环信ID
     * @return
     */
    public static UserCacheInfo get(final String userId){
        UserCacheInfo info = null;

        // 如果本地缓存不存在或者过期，则从存储服务器获取
        if (notExistedOrExpired(userId)){
            UserWebManager.getUserInfoAync(userId, new UserWebManager.UserCallback() {
                @Override
                public void onCompleted(UserWebInfo info) {
                    if(info == null) return;

                    // 缓存到本地
                    // info.getOpenId() 为该用户的【环信ID】
                    save(info.getOpenId(), info.getNickName(),info.getAvatarUrl());
                }
            });
        }

        // 从本地缓存中获取用户数据
        info = getFromCache(userId);

        return info;
    }

    /**
     * 获取用户信息
     * @param userId 用户环信ID
     * @return
     */
    public static UserCacheInfo getFromCache(String userId){

        try {
            Dao<UserCacheInfo, Integer> dao = SqliteHelper.getInstance().getUserDao();
            UserCacheInfo model = dao.queryBuilder().where().eq("userId", userId).queryForFirst();
            return model;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    /**
     * 获取用户信息
     * @param userId
     * @return
     */
    public static EaseUser getEaseUser(String userId){

        UserCacheInfo user = get(userId);
        if (user == null) return null;

        EaseUser easeUser = new EaseUser(userId);
        easeUser.setAvatar(user.getAvatarUrl());
        easeUser.setNickname(user.getNickName());

        return easeUser;
    }

    /**
     * 用户是否存在
     * @param userId 用户环信ID
     * @return
     */
    public static boolean isExisted(String userId){
        Dao<UserCacheInfo, Integer> dao = SqliteHelper.getInstance().getUserDao();
        try {
            long count = dao.queryBuilder().where().eq("userId", userId).countOf();
            return count > 0;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return false;
    }

    /**
     * 用户不存在或已过期
     * @param userId 用户环信ID
     * @return
     */
    public static boolean notExistedOrExpired(String userId){
        Dao<UserCacheInfo, Integer> dao = SqliteHelper.getInstance().getUserDao();
        try {
            long count = dao.queryBuilder().where()
                    .eq("userId", userId).and()
                    .gt("expiredDate",new Date().getTime())
                    .countOf();
            return count <= 0;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return true;
    }

    /**
     * 缓存用户信息
     * @param userId 用户环信ID
     * @param avatarUrl 头像Url
     * @param nickName 昵称
     * @return
     */
    public static boolean save(String userId, String nickName, String avatarUrl){
        try {
            Dao<UserCacheInfo, Integer> dao = SqliteHelper.getInstance().getUserDao();

            UserCacheInfo user = getFromCache(userId);

            // 新增
            if (user == null){
                user = new UserCacheInfo();
            }

            user.setUserId(userId);
            user.setAvatarUrl(avatarUrl);
            user.setNickName(nickName);
            user.setExpiredDate(new Date().getTime() + 24*60*60*1000);// 一天过期，单位：毫秒

            Dao.CreateOrUpdateStatus status = dao.createOrUpdate(user);

            if(status.getNumLinesChanged() > 0){
                Log.i("UserCacheManager", "操作成功~");
                return true;
            }
        } catch (Exception e) {
            e.printStackTrace();
            Log.e("UserCacheManager", "操作异常~");
        }

        return false;
    }

    /**
     * 更新当前用户的昵称
     * @param nickName 昵称
     */
    public static void updateMyNick(String nickName){
        UserCacheInfo user = getMyInfo();
        if (user == null)  return;

        save(user.getUserId(), nickName, user.getAvatarUrl());
    }


    /**
     * 更新当前用户的头像
     * @param avatarUrl 头像Url（完成路径）
     */
    public static void updateMyAvatar(String avatarUrl){
        UserCacheInfo user = getMyInfo();
        if (user == null)  return;

        save(user.getUserId(), user.getNickName(), avatarUrl);
    }

    /**
     * 缓存用户信息
     * @param model 用户信息
     * @return
     */
    public static boolean save(UserCacheInfo model){

        if(model == null) return false;

        return save(model.getUserId(),model.getNickName(),model.getAvatarUrl());
    }

    /**
     * 缓存用户信息
     * @param ext 用户信息
     * @return
     */
    public static boolean save(String ext){
        if(ext == null) return false;

        UserCacheInfo user = UserCacheInfo.parse(ext);
        return save(user);
    }

    /**
     * 缓存用户信息
     * @param ext 消息的扩展属性
     * @return
     */
    public static void save(Map<String,Object> ext){

        if(ext == null) return;

        try {
            String userId = ext.get(kChatUserId).toString();
            String avatarUrl = ext.get(kChatUserPic).toString();;
            String nickName = ext.get(kChatUserNick).toString();;

            save(userId,nickName,avatarUrl);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取当前环信用户信息
     * @return
     */
    public static UserCacheInfo getMyInfo(){
        return get(EMClient.getInstance().getCurrentUser());
    }

    /**
     * 获取用户昵称
     * @return
     */
    public static String getMyNickName(){
        UserCacheInfo user = getMyInfo();
        if(user == null) return EMClient.getInstance().getCurrentUser();

        return user.getNickName();
    }

    /**
     * 设置消息的扩展属性
     * @param msg 发送的消息
     */
    public static void setMsgExt(EMMessage msg){
        if(msg == null) return;

        UserCacheInfo user = getMyInfo();
        msg.setAttribute(kChatUserId, user.getUserId());
        msg.setAttribute(kChatUserNick, user.getNickName());
        msg.setAttribute(kChatUserPic, user.getAvatarUrl());
    }

    /**
     * 获取登录用户的昵称头像
     * @return
     */
    public static String getMyInfoStr(){

        Map<String,Object> map = new HashMap<>();

        UserCacheInfo user = getMyInfo();
        map.put(kChatUserId, user.getUserId());
        map.put(kChatUserNick, user.getNickName());
        map.put(kChatUserPic, user.getAvatarUrl());

        return new Gson().toJson(map);
    }
}
