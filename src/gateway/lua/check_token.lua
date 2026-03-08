local token = ngx.var.http_authorization

if ngx.var.uri:match("^/docs") then
    return
end

if not token then
    ngx.status = 401
    ngx.say('{"detail": "Missing authorization token"}')
    ngx.exit(401)
end

if not token:find("^Bearer ") then
    ngx.status = 401
    ngx.say('{"detail": "Invalid token format. Use Bearer scheme"}')
    ngx.exit(401)
end