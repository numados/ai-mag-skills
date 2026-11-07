using Microsoft.Extensions.Caching.Memory;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddMemoryCache();

var app = builder.Build();

app.MapGet("/tenant/{tenantId}/report", (string tenantId, IMemoryCache cache) =>
{
    // Defect: tenant-sensitive data is cached under a tenant-agnostic key,
    // so tenant A can observe tenant B's cached report.
    if (!cache.TryGetValue("report", out Report? report))
    {
        report = new Report(tenantId, Guid.NewGuid());
        cache.Set("report", report, TimeSpan.FromMinutes(5));
    }

    return Results.Ok(report);
});

app.Run();

sealed record Report(string TenantId, Guid Id);
