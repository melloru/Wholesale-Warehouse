Разбиение монолита на микросервисы

Сразу никому не доверяем и проверяем абсолютно все
```python
def internal_endpoint(allowed_services: list[str]):
    """Декоратор для internal endpoints"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request') or args[0]
            
            # 1. Проверка API ключа (всегда)
            api_key = request.headers.get("X-API-Key")
            service_name = request.headers.get("X-Service-Name")
            
            if service_name not in allowed_services:
                raise HTTPException(403, f"Service {service_name} not allowed")
            
            if not api_key or not service_name:
                raise HTTPException(403, "Missing credentials")
            
            if api_key != config.SERVICE_API_KEYS.get(service_name):
                raise HTTPException(403, "Invalid API key")
            
            # mTLS проверка (настоящая логика при добавлении новых серваков)
            cert = request.headers.get("X-Client-Cert")
            if not await verify_mtls(cert):
                pass
            
            # Логирование
            await InternalRequestLogger.log_request(
                service_name=service_name,
                endpoint=request.url.path,
                client_ip=request.client.host,
                success=True
            )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```