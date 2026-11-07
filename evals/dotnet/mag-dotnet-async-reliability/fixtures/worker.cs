using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Channels;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;

namespace Fixture.Workers;

public sealed class OrderProcessor : BackgroundService
{
    private readonly Channel<Order> _inbox = Channel.CreateUnbounded<Order>();

    public ValueTask SubmitAsync(Order order, CancellationToken ct = default) =>
        _inbox.Writer.WriteAsync(order, ct);

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await _inbox.Reader.WaitToReadAsync(stoppingToken);
            while (_inbox.Reader.TryRead(out var order))
            {
                // fire-and-forget: the Task is dropped and its exceptions are
                // never observed; Process never receives the stopping token.
                _ = Task.Run(() => Process(order));
            }
        }
    }

    public async Task ProcessBatchAsync(IReadOnlyList<Order> orders)
    {
        // unbounded fan-out: one task per order with no concurrency limit, and
        // the caller's token is never threaded into Process.
        var tasks = new List<Task>(orders.Count);
        foreach (var order in orders)
        {
            tasks.Add(Task.Run(() => Process(order)));
        }
        await Task.WhenAll(tasks);
    }

    private static void Process(Order order)
    {
        // CPU-bound work that never observes a cancellation token.
        Thread.Sleep(1500);
        Console.WriteLine(order.Id);
    }
}

public sealed record Order(int Id);
