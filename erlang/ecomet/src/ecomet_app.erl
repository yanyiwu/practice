-module(ecomet_app).

-behaviour(application).

-include("logger.hrl").

%% Application callbacks
-export([start/2, stop/1]).

%% ===================================================================
%% Application callbacks
%% ===================================================================

start(_StartType, _StartArgs) ->
    ?LOGDEBUG("ecomet_app start node ~p", [node()]),
    db_init(),
    Sup = ecomet_sup:start_link(),
    Sup.

stop(_State) ->
    ?LOGDEBUG("ecomet_app stop node ~p", [node()]),
    ok.


db_init() ->
    MyNode = node(),
    DbNodes = mnesia:system_info(db_nodes),
    ?LOGDEBUG("mynode ~p , dbnodes ~p", [MyNode, DbNodes]),
    case lists:member(MyNode, DbNodes) of
        true ->
            ok;
        false ->
            ?LOGERROR("node ~p is not in dbnodes ~p", [MyNode, DbNodes]),
            erlang:error(node_name_mismatch)
    end,
    case mnesia:system_info(extra_db_nodes) of 
        [] ->
            mnesia:create_schema([node()]);
        _ ->
            ok
    end,
    ?LOGDEBUG("mnesia:wait_for_tables ing ...", []),
    case mnesia:wait_for_tables(mnesia:system_info(local_tables), infinity) of 
        ok ->
            ?LOGDEBUG("mnesia:wait_for_tables finished ok.", []),
            ok;
        Others ->
            ?LOGERROR("wait_for_tables failed.", []),
            Others
    end.
