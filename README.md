# wpoly

Display unread message count for [WeeChat](https://weechat.org/)
in a [Polybar](https://polybar.github.io/) module.

Load the script into WeeChat (you may want to do so automatically on launch):

~~~
/script load /path/to/wpoly.py
~~~

Create a corresponding Polybar module:

~~~
[module/wpoly]
type = custom/ipc
hook-0 = [ -s /tmp/wpoly.msgs ] && cat /tmp/wpoly.msgs || echo 0
initial = 1
format = new msgs: <output>
~~~

Make sure you have `enable-ipc = true` set for the parent bar.
