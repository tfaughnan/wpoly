try:
    import weechat
except ModuleNotFoundError:
    print('This script must be run by WeeChat')
    exit(1)

import os

SCRIPT_NAME = 'wpoly'
SCRIPT_AUTHOR = 'tom faughnan'
SCRIPT_VERSION = '0.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'indicate new weechat messages in polybar'

TMPFILE = '/tmp/wpoly.msgs'

unread_buffers = {}
unread_count = 0


def update_unread_count():
    global unread_buffers, unread_count
    old_count = unread_count
    unread_count = sum(unread_buffers.values())
    if unread_count != old_count:
        with open(TMPFILE, 'w') as f:
            f.write(f'{unread_count}\n')
            os.system('polybar-msg hook wpoly 1 &> /dev/null')


def cb_handle_message(
        data,
        buff,
        date,
        tags,
        displayed,
        highlight,
        prefix,
        message):
    global unread_buffers
    buff_name = weechat.buffer_get_string(buff, 'name')
    num_displayed = weechat.buffer_get_integer(buff, 'num_displayed')
    if not num_displayed and 'notify_' in tags and 'self_msg' not in tags:
        unread_buffers[buff_name] = unread_buffers.get(buff_name, 0) + 1
        update_unread_count()

    return weechat.WEECHAT_RC_OK


def cb_buffer_switch(data, signal, buff):
    global unread_buffers
    buff_name = weechat.buffer_get_string(buff, 'name')
    if buff_name in unread_buffers:
        unread_buffers.pop(buff_name)
        update_unread_count()

    return weechat.WEECHAT_RC_OK


if __name__ == '__main__':
    weechat.register(SCRIPT_NAME,
                     SCRIPT_AUTHOR,
                     SCRIPT_VERSION,
                     SCRIPT_LICENSE,
                     SCRIPT_DESC,
                     '',
                     '')
    weechat.hook_print('', '', '', 1, 'cb_handle_message', '')
    weechat.hook_signal('buffer_switch', 'cb_buffer_switch', '')
