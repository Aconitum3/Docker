# .profile

以下のように編集されていれば良い。

```
# ~/.profile: executed by Bourne-compatible login shells.

if [ "$BASH" ]; then
  if [ -f ~/.bashrc ]; then
    . ~/.bashrc
  fi
fi

mesg n || true

PATH="$PATH:/root/anaconda3/bin"
```
また、`PATH = "$PATH***"`のように半角スペースを入れないこと。
