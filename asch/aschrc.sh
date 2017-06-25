HOST=myasch.com
PORT=8192
PUB=164495284179d7289264325a7c4e0a4a4969e7b81577108dc8975562ad2cdfdf
ADDR=A7rANTV8Ncod7MmqFaEduqdNhVARnyEuLX
ME=yanyiwu

function mainasch() {
    asch-cli --main --host $HOST --port $PORT $@
}

function aschdelegatebyname() {
    mainasch getdelegatebyusername $@
}

function aschme() {
    mainasch openaccountbypublickey $PUB
    mainasch getblockstatus
    aschdelegatebyname $ME
}

function myvotes() {
    mainasch getvoteddelegates $ADDR
}

function voteme() {
    mainasch getvoters $PUB
}

function aschpubbyname() {
    x=`aschdelegatebyname $1 | egrep '"publicKey": "(.*)"' | sed 's/"publicKey": "\(.*\)",/\1/g'`
    echo $x
}

function upvote() {
    echo "first:"
    read -s s
    echo "second:"
    read -s ss
    echo "$@"
    asch-cli --main --port $PORT upvote -e "$s" -s $ss -p $@
}
function downvote() {
    echo "first:"
    read -s s
    echo "second:"
    read -s ss
    echo "$@"
    asch-cli --main --port $PORT downvote -e "$s" -s $ss -p $@
}

function aschdelegates() {
    mainasch getdelegates
    mainasch getdelegates -o 101 -l 3
}

function voteeachother() {
    echo "myvote"
    mainasch getvoteddelegates $ADDR | grep $1
    echo "voteme"
    mainasch getvoters $PUB | grep $1
}

