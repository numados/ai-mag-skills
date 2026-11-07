using System;
using System.Collections.Generic;
using System.Linq;

namespace Fixture.Reports;

public sealed class ReportBuilder
{
    public string Build(IEnumerable<Sale> sales)
    {
        var lines = new List<string>();

        // Deferred query: re-evaluated on every enumeration below.
        var significant = sales.Where(s => s.Amount > 100m);

        // First enumeration.
        var total = significant.Sum(s => s.Amount);
        lines.Add($"total={total}");

        // Second enumeration of the same deferred query — if the source is
        // expensive (e.g., hits the database) or the predicate has side
        // effects, the work and side effects run twice.
        var count = significant.Count();
        lines.Add($"count={count}");

        return string.Join(Environment.NewLine, lines);
    }
}

public sealed record Sale(int Id, decimal Amount);
