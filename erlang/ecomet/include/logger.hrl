
-define(LOGDEBUG(Format, Msgs), 
    ?LOG_F(debug, Format, Msgs)).

-define(LOGINFO(Format, Msgs), 
    ?LOG_F(info, Format, Msgs)).

-define(LOGWARN(Format, Msgs), 
    ?LOG_F(warn, Format, Msgs)).

-define(LOGERROR(Format, Msgs), 
    ?LOG_F(error, Format, Msgs)).

-define(LOG_F(Level, Format, Msgs), 
    io:format("~p ~p ~p ~p " ++ Format ++ " ~n", [calendar:now_to_local_time(erlang:now()), ?FILE, ?LINE, Level] ++ Msgs)).

