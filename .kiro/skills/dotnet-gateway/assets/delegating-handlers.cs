public class CorrelationIdDelegatingHandler : DelegatingHandler
{
    private const string CorrelationIdHeader = "X-Correlation-Id";
    private const string CorrelationIdKey = "CorrelationId";

    private readonly IHttpContextAccessor _httpContextAccessor;

    public CorrelationIdDelegatingHandler(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        var httpContext = _httpContextAccessor.HttpContext;

        if (httpContext != null &&
            httpContext.Items.TryGetValue(CorrelationIdKey, out var correlationId) &&
            correlationId is string correlationIdString &&
            !string.IsNullOrEmpty(correlationIdString))
        {
            if (request.Headers.Contains(CorrelationIdHeader))
                request.Headers.Remove(CorrelationIdHeader);

            request.Headers.Add(CorrelationIdHeader, correlationIdString);

            Log.Information("Propagating {Header}: {CorrelationId} to {Url}",
                CorrelationIdHeader, correlationIdString, request.RequestUri);
        }

        return await base.SendAsync(request, cancellationToken);
    }
}

public class MissingBodyDelegatingHandler : DelegatingHandler
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        var httpContext = _httpContextAccessor.HttpContext;
        
        if (httpContext?.Request.ContentType != null && request.Content == null)
        {
            if (httpContext.Request.Body.CanSeek)
                httpContext.Request.Body.Seek(0, SeekOrigin.Begin);

            if (httpContext.Request.HasFormContentType)
            {
                var multipartContent = new MultipartFormDataContent();
                multipartContent.Headers.ContentDisposition = 
                    new ContentDispositionHeaderValue("form-data");

                var forms = await httpContext.Request.ReadFormAsync(cancellationToken);
                
                foreach (var file in forms.Files)
                {
                    using var ms = new MemoryStream();
                    await file.CopyToAsync(ms, cancellationToken);
                    var fileContent = new ByteArrayContent(ms.ToArray())
                    {
                        Headers = { ContentType = new MediaTypeHeaderValue(file.ContentType) }
                    };
                    multipartContent.Add(fileContent, file.Name, file.FileName);
                }

                foreach (var key in forms.Keys)
                    multipartContent.Add(new StringContent(forms[key].ToString() ?? ""), key);

                request.Content = multipartContent;
            }
            else
            {
                using var body = new MemoryStream();
                await httpContext.Request.Body.CopyToAsync(body, cancellationToken);
                request.Content = new ByteArrayContent(body.ToArray())
                {
                    Headers = { ContentType = new MediaTypeHeaderValue(httpContext.Request.ContentType) }
                };
            }
        }

        return await base.SendAsync(request, cancellationToken);
    }
}
