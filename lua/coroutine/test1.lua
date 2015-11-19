function producer()
    return coroutine.create(
    function (salt)
        local t = { 1, 2, 3 } 
        for i = 1, #t do
            salt = coroutine.yield(t[i] + salt)
        end 
    end
    ) 
end

function consumer(prod) 
    local salt = 10
    while true do
        local running, product =
        coroutine.resume(prod, salt)
        salt = salt * salt 
        if running then
            print(product or "END!") 
        else
            break 
        end
    end 
end
consumer(producer())
