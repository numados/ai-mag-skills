var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();

// Expose the implicit Program class so a WebApplicationFactory<Program> in
// the test project can reference the entry point.
public partial class Program { }
