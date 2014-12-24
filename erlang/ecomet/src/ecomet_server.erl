-module(ecomet_server).

-behavior(gen_server).

-include("logger.hrl").

%% API

-export([
        start_link/1,
        start_link/0,
        get_count/0
    ]).

%% gen_server callbacks
-export([
        init/1,
        handle_call/3,
        handle_cast/2,
        handle_info/2,
        terminate/2,
        code_change/3]).

-define(SERVER, ?MODULE).
-define(DEFUALT_PORT, 1055).

-record(state, {port, lsock, request_count = 0}).

%% gen_server callbacks

init([Port]) ->
    %%?LOGDEBUG([?SERVER, init_listen_port, Port]),
    {ok, LSock} = gen_tcp:listen(Port, [{active, true}]),
    {ok, #state{port = Port, lsock = LSock}, 0}.

handle_call(Request, From, State) ->
    %%?LOGDEBUG(Request),
    %%?LOGDEBUG(From),
    {reply, {ok, State#state.request_count}, State}.

handle_cast(stop, State) ->
    %%?LOGDEBUG(State),
    {stop, normal, State}.

handle_info({tcp, Socket, RawData}, State) ->
    do_rpc(Socket, RawData),
    RequestCount = State#state.request_count,
    %%?LOGDEBUG(RequestCount),
    {noreply, State#state{request_count = RequestCount + 1}};
handle_info(timeout, #state{lsock = LSock} = State) ->
    %%?LOGDEBUG(["gen_tcp:accept", LSock]),
    %%?LOGDEBUG(inet:peername(LSock)),
    {ok, Sock} = gen_tcp:accept(LSock),
    %%?LOGDEBUG(["gen_tcp:accept", Sock]),
    {ok, RemoteAddr, RemotePort} = inet:peername(Sock),
    %%?LOGDEBUG(RemoteAddr),
    %%?LOGDEBUG(RemotePort),
    {noreply, State}.

terminate(Reason, #state{lsock = LSock} = State) ->
    %%?INFO("close lsock"),
    gen_tcp:close(LSock).

code_change(_OldVsn, State, _Extra) ->
    %%?LOGDEBUG("code_change"),
    {ok, State}.

%% API functions

get_count() ->
    %%?LOGDEBUG(get_count),
    %%?LOGDEBUG(?SERVER),
    gen_server:call(?SERVER, get_count).

start_link(Port) ->
    %%?LOGDEBUG([gen_server_start_link, Port]),
    gen_server:start_link({local, ?SERVER}, ?MODULE, [Port], []).
start_link() ->
    %%?LOGDEBUG(gen_server_start_link),
    start_link(?DEFUALT_PORT).

%% Internal functions

do_rpc(Socket, RawData) ->
    try
        %%?LOGDEBUG(RawData),
        gen_tcp:send(Socket, "ok hehe")
    catch
        _Class:Err ->
            ?LOGERROR("do_rpc", [Err]),
            gen_tcp:send(Socket, "error hehe")
    end.
