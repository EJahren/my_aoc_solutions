#!/usr/bin/env escript
-import(lists, [sum/1, map/2]).

main(_) ->
    {ok, Device} = file:open("day1_input.txt", [read]),
    Lines = try get_all_lines(Device)
            after file:close(Device)
        end,
    io:format("~w~n", [sum(map(fun($)) -> -1; ($() -> 1 end,Lines))]),
    io:format("~w~n", [part2(0, 1, Lines)]).

part2(-1, Pos, _) -> Pos;
part2(Floor, Pos, [$) | Rest]) -> part2(Floor-1, Pos+1, Rest);
part2(Floor, Pos, [$( | Rest]) -> part2(Floor+1, Pos+1, Rest).

    
get_all_lines(Device) ->
    case io:get_line(Device, "") of
        eof  -> [];
        Line -> Line ++ get_all_lines(Device)
    end.
