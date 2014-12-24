-module(ecomet_sup).

-behaviour(supervisor).

-include("logger.hrl").

%% API
-export([start_link/0]).

%% Supervisor callbacks
-export([init/1]).

-define(SERVER, ?MODULE).

%% Helper macro for declaring children of supervisor
%% -define(CHILD(I, Type), {I, {I, start_link, []}, permanent, 5000, Type, [I]}).

%% ===================================================================
%% API functions
%% ===================================================================

start_link() ->
    supervisor:start_link({local, ?SERVER}, ?MODULE, []).

%% ===================================================================
%% Supervisor callbacks
%% ===================================================================

init([]) ->
    ?LOGDEBUG("ecomet_sup init", []),
    Server = {ecomet_server, {ecomet_server, start_link, []},
        permanent, 2000, worker, [ecomet_server]},
    Children = [Server],
    RestartStategy = {one_for_one, 0, 1},
    {ok, {RestartStategy, Children}}.

