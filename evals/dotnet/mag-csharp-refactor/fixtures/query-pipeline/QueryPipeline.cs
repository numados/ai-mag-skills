using System.Collections.Generic;
using System.Linq;

namespace Fixture.Pipelines;

public sealed class QueryPipeline
{
    // Eager pipeline: work runs once, here, and the result is a stable list.
    public IReadOnlyList<string> SortedProducts(IEnumerable<Order> orders)
    {
        var products = orders
            .Where(o => o.Quantity > 0)
            .Select(o => o.Product)
            .Distinct()
            .OrderBy(p => p)
            .ToList();
        return products;
    }

    // Lazy candidate the caller is considering: return IEnumerable<string>
    // without ToList. This defers all work to enumeration time and re-runs
    // it on each enumeration — a semantic, not mechanical, change.
    public IEnumerable<string> SortedProductsLazy(IEnumerable<Order> orders) =>
        orders
            .Where(o => o.Quantity > 0)
            .Select(o => o.Product)
            .Distinct()
            .OrderBy(p => p);
}

public sealed record Order(int Id, string Product, int Quantity);
