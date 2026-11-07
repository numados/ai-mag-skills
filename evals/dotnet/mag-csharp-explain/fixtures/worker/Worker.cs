using System;
using System.Threading;
using System.Threading.Tasks;

namespace Fixture.Workers;

public sealed class OrderWorker
{
    private readonly Func<Order, CancellationToken, Task> _process;

    public OrderWorker(Func<Order, CancellationToken, Task> process)
    {
        _process = process;
    }

    // Blocks synchronously on an async call while forwarding the CancellationToken.
    public void RunSync(Order order, CancellationToken ct)
    {
        _process(order, ct).GetAwaiter().GetResult();
    }

    public async Task RunAsync(Order order, CancellationToken ct)
    {
        await _process(order, ct);
    }
}

public sealed record Order(int Id);
