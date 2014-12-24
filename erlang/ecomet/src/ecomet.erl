-module(ecomet).

-export([start/0, stop/0]).

-include("logger.hrl").

start() ->
    io:format("~p~p~n", [?FILE, ?LINE]),
    ?LOGINFO("starting ~p...", ["2"]),
    application:start(ecomet).

stop() ->
    ?LOGINFO("stopping ...", []),
    application:stop(ecomet).
