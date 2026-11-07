using System.Net.Http.Json;
using Microsoft.Extensions.Http.Resilience;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient<OrderClient>(client =>
{
    client.BaseAddress = new Uri("https://orders.internal/");
})
// Defect: the standard resilience handler retries every HTTP method by
// default, including POST, so a failed insert can be replayed and the row
// created twice.
.AddStandardResilienceHandler();

var app = builder.Build();

app.MapPost("/orders", async (OrderClient client, Order order) =>
{
    await client.CreateAsync(order);
    return Results.Created($"/orders/{order.Id}", order);
});

app.Run();

public sealed class OrderClient(HttpClient http)
{
    public Task CreateAsync(Order order) =>
        http.PostAsJsonAsync($"/orders/{order.Id}", order);
}

public sealed record Order(int Id, string Sku);
