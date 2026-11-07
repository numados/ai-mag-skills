using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Fixture.Pipelines;

public sealed class OrderPipeline
{
    // The returned query is deferred: it captures `orders` and `threshold`
    // and is evaluated only when enumerated. Each enumeration re-reads the
    // captured variables and re-runs the Where/Select work.
    public IEnumerable<string> ExpensiveOrders(IEnumerable<Order> orders, decimal threshold)
    {
        var query = orders
            .Where(o => o.Total > threshold)
            .Select(o => o.Number);

        return query;
    }

    public async Task PrintAsync(IAsyncEnumerable<Order> orders)
    {
        await using var enumerator = orders.GetAsyncEnumerator();

        while (await enumerator.MoveNextAsync().ConfigureAwait(false))
        {
            Console.WriteLine(enumerator.Current.Number);
        }

        // IAsyncEnumerator is IAsyncDisposable; await using guarantees
        // disposal on normal exit and on exception.
    }
}

public sealed record Order(string Number, decimal Total);
