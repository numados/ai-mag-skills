using Microsoft.AspNetCore.RateLimiting;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors();
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("orders", limiter =>
    {
        limiter.PermitLimit = 10;
        limiter.Window = TimeSpan.FromSeconds(1);
    });
});

var app = builder.Build();

// Defect 1: UseResponseCaching runs before UseCors, so cached responses are
// stored and served without the CORS headers UseCors would have added.
app.UseResponseCaching();
app.UseCors();

// Defect 2: UseRateLimiter runs before UseRouting, so the endpoint-specific
// RequireRateLimiting("orders") metadata below is not yet selected when the
// limiter middleware executes.
app.UseRateLimiter();
app.UseRouting();

app.MapGet("/orders", () => Results.Ok(new[] { 101, 102, 103 }))
   .RequireRateLimiting("orders");

app.Run();
