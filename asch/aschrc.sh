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
    x=`aschdelegatebyname $1 | egrep '"publicKey": "(.*)"' | sed 's/"publicKey": "\(.*\)",/\1/g' | sed 's/ //g'`
    echo $x
}

function upvote() {
    pub=`aschpubbyname $@`
    echo $pub
    echo "first:"
    read -s s
    echo "second:"
    read -s ss
    echo "$@"
    asch-cli --main --host $HOST --port $PORT upvote -e "$s" -s $ss -p $pub
}
function downvote() {
    pub=`aschpubbyname $@`
    echo $pub
    echo "first:"
    read -s s
    echo "second:"
    read -s ss
    asch-cli --main --host $HOST --port $PORT downvote -e "$s" -s $ss -p $pub
}

function aschdelegates() {
    mainasch getdelegates
}

function voteeachother() {
    echo "myvote"
    mainasch getvoteddelegates $ADDR | grep $1
    echo "voteme"
    mainasch getvoters $PUB | grep $1
}

