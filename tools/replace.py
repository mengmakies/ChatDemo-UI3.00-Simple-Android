#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "xyjxyf"

"替换枚举类型"

import sys
import os
import re

walk_path = '../'
# 需要替换的字典：key->旧值， value->新值
#======================= special',
replace_dic = {
'\<msg.status\>\s*=[^=]\(.*\);': 'msg.setStatus(\1);',
'\<msg.status\>\s*[^=]': 'msg.status() ',
'\<msg.status\>\s*==': 'msg.status() ==',

'\<msg.direct\>\s*=[^=]\(.*\);': 'msg.setdirect(\1);',
'\<msg.direct\>\s*==': 'msg.direct() ==',

'\<msg.type\>\s*==': 'msg.getType() ==',

'\<msg.msgTime\>\s*=[^=]\(.*\);': 'msg.setMsgTime(\1);',
'\<msg.msgTime\>\s*==': 'msg.getMsgTime() ==',

'\<msg.chatType\>\s*=[^=]\(.*\);': 'msg.getChatType(\1);',
'\<msg.chatType\>\s*==': 'msg.getChatType() ==',

'\<msg.progress\>\s*==': 'msg.progress() ==',

'\<msg.unread\>\s*=[^=]\(.*\);': 'msg.setUnread(\1);',
'\<msg.unread\>\s*==': 'msg.isUnread() ==',

'\<msg.isAcked\>\s*==': 'msg.isAcked() ==',

'\<msg.msgId\>\s*=[^=]\(.*\);': 'msg.setMsgId(\1);',
'\<msg.msgId\>\s*==': 'msg.getMsgId() ==',

'\<msg.isListened\>\s*=[^=]\(.*\);': 'msg.setisListened(\1);',
'\<msg.isListened\>\s*==': 'msg.isListened() ==',

'\<msg.isDelivered\>\s*=[^=]\(.*\);': 'msg.setDelivered(\1);',
'\<msg.isDelivered\>\s*==': 'msg.isDelivered() ==',

'\<msg.from\>\s*=[^=]\(.*\);': 'msg.setFrom(\1);',
'\<msg.from\>\s*==': 'msg.getFrom() ==',

'\<msg.to\>\s*=[^=]\(.*\);': 'msg.setTo(\1);',
'\<msg.to\>\s*==': 'msg.getTo() ==',



'\<message.status\>\s*=[^=]\(.*\);': 'message.setStatus(\1);',
'\<message.status\>\s*==': 'message.status() ==',

'\<message.direct\>\s*=[^=]\(.*\);': 'message.setdirect(\1);',
'\<message.direct\>\s*==': 'message.direct() ==',

'\<message.type\>\s*==': 'message.getType() ==',

'\<message.msgTime\>\s*=[^=]\(.*\);': 'message.setMsgTime(\1);',
'\<message.msgTime\>\s*==': 'message.getMsgTime() ==',

'\<message.chatType\>\s*=[^=]\(.*\);': 'message.setChatType(\1);',
'\<message.chatType\>\s*==': 'message.getChatType() ==',

'\<message.progress\>\s*==': 'message.progress() ==',

'\<message.unread\>\s*=[^=]\(.*\);': 'message.setUnread(\1);',
'\<message.unread\>\s*==': 'message.isUnread() ==',

'\<message.isAcked\>\s*==': 'message.isAcked() ==',

'\<message.msgId\>\s*=[^=]\(.*\);': 'message.setMsgId(\1);',
'\<message.msgId\>\s*==': 'message.getMsgId() ==',

'\<message.isListened\>\s*=[^=]\(.*\);': 'message.setisListened(\1);',
'\<message.isListened\>\s*==': 'message.isListened() ==',

'\<message.isDelivered\>\s*=[^=]\(.*\);': 'message.setDelivered(\1);',
'\<message.isDelivered\>\s*==': 'message.isDelivered() ==',

'\<message.from\>\s*=[^=]\(.*\);': 'message.setFrom(\1);',
'\<message.from\>\s*==': 'message.getFrom() ==',

'\<message.to\>\s*=[^=]\(.*\);': 'message.setTo(\1);',
'\<message.to\>\s*==': 'message.getTo() ==',



#======================= normal',
'\<EMChatOptions\>': 'EMOptions',

'\<CmdMessageBody\>': 'EMCmdMessageBody',
'\<FileMessageBody\>': 'EMFileMessageBody',
'\<ImageMessageBody\>': 'EMImageMessageBody',
'\<LocationMessageBody\>': 'EMLocationMessageBody',
'\<TextMessageBody\>': 'EMTextMessageBody',
'\<VideoMessageBody\>': 'EMVideoMessageBody',
'\<VoiceMessageBody\>': 'EMVoiceMessageBody',

'\<conversation.loadMoreGroupMsgFromDB\>': 'conversation.loadMoreMsgFromDB',

'EMChat.getInstance().isLoggedIn()': 'EMClient.getInstance().isLoggedInBefore()',
'EMChat.getInstance().setDebugMode': 'EMClient.getInstance().setDebugMode',
'EMChat.getInstance().uploadLog': 'EMClient.getInstance().uploadLog',
'EMChatManager.getInstance().ackMessageRead': 'EMClient.getInstance().chatManager().ackMessageRead',
'EMChatManager.getInstance().addCallStateChangeListener': 'EMClient.getInstance().callManager().addCallStateChangeListener',
'EMChatManager.getInstance().addChatRoomChangeListener': 'EMClient.getInstance().chatroomManager().addChatRoomChangeListener',
'EMChatManager.getInstance().addConnectionListener': 'EMClient.getInstance().addConnectionListener',
'EMChatManager.getInstance().answerCall();': 'EMClient.getInstance().callManager().answerCall();',
'EMChatManager.getInstance().asyncFetchMessage': 'EMClient.getInstance().chatManager().downloadThumbnail',
'EMChatManager.getInstance().clearConversation': 'EMClient.getInstance().chatManager().deleteConversation',
'EMChatManager.getInstance().createAccountOnServer': 'EMClient.getInstance().createAccount',
'EMChatManager.getInstance().downloadFile': 'EMClient.getInstance().chatManager().downloadFile',
'EMChatManager.getInstance': 'EMClient.getInstance',
'EMChatManager.getInstance().endCall();': 'EMClient.getInstance().callManager().endCall();',
'EMChatManager.getInstance().fetchChatRoomFromServer': 'EMClient.getInstance().chatroomManager().fetchChatRoomFromServer',
'EMChatManager.getInstance().fetchPublicChatRoomsFromServer': 'EMClient.getInstance().chatroomManager().fetchPublicChatRoomsFromServer',
'EMChatManager.getInstance().getAllChatRooms();': 'EMClient.getInstance().chatroomManager().getAllChatRooms();',
'EMChatManager.getInstance().getAllConversations()': 'EMClient.getInstance().chatManager().getAllConversations()',
'EMChatManager.getInstance().getChatOptions()': 'EMClient.getInstance().getOptions()',
'EMChatManager.getInstance().getChatRoom': 'EMClient.getInstance().chatroomManager().getChatRoom',
'EMChatManager.getInstance().getConversation': 'EMClient.getInstance().chatManager().getConversation',
'EMChatManager.getInstance().getCurrentUser();': 'EMClient.getInstance().getCurrentUser();',
'EMChatManager.getInstance().getCurrentUser()': 'EMClient.getInstance().getCurrentUser()',
'EMChatManager.getInstance().getIncomingCallBroadcastAction()': 'EMClient.getInstance().callManager().getIncomingCallBroadcastAction()',
'EMChatManager.getInstance().getMessage': 'EMClient.getInstance().chatManager().getMessage',
'EMChatManager.getInstance().getRobotsFromServer();': 'EMClient.getInstance().getRobotsFromServer();',
'EMChatManager().getInstance().getUnreadMsgsCount();': 'EMClient.getInstance().chatManager().getUnreadMsgsCount();',
'EMChatManager.getInstance().isConnected()': 'EMClient.getInstance().isConnected()',
'EMChatManager.getInstance().isDirectCall()': 'EMClient.getInstance().callManager().isDirectCall()',
'EMChatManager.getInstance().isSlientMessage': 'EMClient.getInstance().chatManager().isSlientMessage',
'EMChatManager.getInstance().joinChatRoom': 'EMClient.getInstance().chatroomManager().joinChatRoom',
'EMChatManager.getInstance().leaveChatRoom': 'EMClient.getInstance().chatroomManager().leaveChatRoom',
'EMChatManager.getInstance().loadAllConversations();': 'EMClient.getInstance().chatManager().loadAllConversations();',
'EMChatManager.getInstance().login': 'EMClient.getInstance().login',
'EMChatManager.getInstance().makeVideoCall': 'EMClient.getInstance().callManager().makeVideoCall',
'EMChatManager.getInstance().makeVoiceCall': 'EMClient.getInstance().callManager().makeVoiceCall',
'EMChatManager.getInstance().rejectCall();': 'EMClient.getInstance().callManager().rejectCall();',
'EMChatManager.getInstance().removeCallStateChangeListener': 'EMClient.getInstance().callManager().removeCallStateChangeListener',
'EMChatManager.getInstance().removeConnectionListener': 'EMClient.getInstance().removeConnectionListener',
'EMChatManager.getInstance().saveMessage': 'EMClient.getInstance().chatManager().saveMessage',
'EMChatManager.getInstance().sendMessage': 'EMClient.getInstance().chatManager().sendMessage',
'EMChatManager.getInstance().setMessageListened': 'EMClient.getInstance().chatManager().setMessageListened',
'EMChatManager.getInstance().updateCurrentUserNick': 'EMClient.getInstance().updateCurrentUserNick',
'EMContactManager.getInstance().addContact': 'EMClient.getInstance().contactManager().addContact',
'EMContactManager.getInstance().addUserToBlackList': 'EMClient.getInstance().contactManager().addUserToBlackList',
'EMContactManager.getInstance().deleteContact': 'EMClient.getInstance().contactManager().deleteContact',
'EMContactManager.getInstance().deleteUserFromBlackList': 'EMClient.getInstance().contactManager().removeUserFromBlackList',
'EMContactManager.getInstance().getBlackListUsernames();': 'EMClient.getInstance().contactManager().getBlackListUsernames();',
'EMContactManager.getInstance().getBlackListUsernamesFromServer();': 'EMClient.getInstance().contactManager().getBlackListFromServer();',
'EMContactManager.getInstance().getContactUserNames();': 'EMClient.getInstance().contactManager().getAllContacts();',
'EMContactManager.getInstance().setContactListener': 'EMClient.getInstance().contactManager().setContactListener',
'EMGroupManager.getInstance().addGroupChangeListener': 'EMClient.getInstance().groupManager().addGroupChangeListener',
'EMGroupManager.getInstance().addUsersToGroup': 'EMClient.getInstance().groupManager().addUsersToGroup',
'EMGroupManager.getInstance().applyJoinToGroup': 'EMClient.getInstance().groupManager().applyJoinToGroup',
'EMGroupManager.getInstance().asyncGetGroupsFromServer': 'EMClient.getInstance().groupManager().asyncGetGroupsFromServer',
'EMGroupManager.getInstance().blockGroupMessage': 'EMClient.getInstance().groupManager().blockGroupMessage',
'EMGroupManager.getInstance().blockUser': 'EMClient.getInstance().groupManager().blockUser',
'EMGroupManager.getInstance().changeGroupName': 'EMClient.getInstance().groupManager().changeGroupName',
'EMGroupManager.getInstance().createOrUpdateLocalGroup': 'EMClient.getInstance().groupManager().createOrUpdateLocalGroup',
'EMGroupManager.getInstance().createPrivateGroup': 'EMClient.getInstance().groupManager().createPrivateGroup',
'EMGroupManager.getInstance().createPublicGroup': 'EMClient.getInstance().groupManager().createPublicGroup',
'EMGroupManager.getInstance()': 'EMClient.getInstance().groupManager()',
'EMGroupManager.getInstance().exitAndDeleteGroup': 'EMClient.getInstance().groupManager().exitAndDeleteGroup',
'EMGroupManager.getInstance().exitFromGroup': 'EMClient.getInstance().groupManager().exitFromGroup',
'EMGroupManager.getInstance().getAllGroups();': 'EMClient.getInstance().groupManager().getAllGroups();',
'EMGroupManager.getInstance().getBlockedUsers': 'EMClient.getInstance().groupManager().getBlockedUsers',
'EMGroupManager.getInstance().getGroup': 'EMClient.getInstance().groupManager().getGroup',
'EMGroupManager.getInstance().getGroupFromServer': 'EMClient.getInstance().groupManager().getGroupFromServer',
'EMGroupManager.getInstance().getGroupsFromServer();': 'EMClient.getInstance().groupManager().getGroupsFromServer();',
'EMGroupManager.getInstance().getPublicGroupsFromServer': 'EMClient.getInstance().groupManager().getPublicGroupsFromServer',
'EMGroupManager.getInstance().inviteUser': 'EMClient.getInstance().groupManager().inviteUser',
'EMGroupManager.getInstance().joinGroup': 'EMClient.getInstance().groupManager().joinGroup',
'EMGroupManager.getInstance().loadAllGroups': 'EMClient.getInstance().groupManager().loadAllGroups',
'EMGroupManager.getInstance().removeUserFromGroup': 'EMClient.getInstance().groupManager().removeUserFromGroup',
'EMGroupManager.getInstance().unblockGroupMessage': 'EMClient.getInstance().groupManager().unblockGroupMessage',
'EMGroupManager.getInstance().unblockUser': 'EMClient.getInstance().groupManager().unblockUser'
}

def check_main(root_path):
    if (len(sys.argv) < 2):
        print "Please input source folder path"
        return 1

    for root, dirs, files in os.walk(sys.argv[1]):
        for file_path in files:
            if file_path.endswith('.java'):
                full_path = os.path.join(root, file_path)

                print full_path

                fr = open(full_path, 'r')
                content = fr.read()
                fr.close()

                for key in replace_dic:
                    match = re.search(key, content)
                    if match:
                        #替换
                        content = re.sub(key, replace_dic[key], content);

                #重新写入文件
                open(full_path,'w').write(content)

if __name__ == '__main__':
    check_main(walk_path)

