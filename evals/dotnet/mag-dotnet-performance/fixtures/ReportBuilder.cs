using System.Collections.Generic;
using System.Linq;

namespace Fixture.HotPath;

public sealed class ReportBuilder
{
    // p95-latency-critical: called once per request on the settlement path.
    public string BuildSettlementReport(IEnumerable<Settlement> settlements)
    {
        var lines = string.Empty;
        foreach (var s in settlements.OrderBy(s => s.Amount))
        {
            lines += Format(s); // string concatenation in a loop allocates per iteration.
        }

        var top = settlements.OrderByDescending(s => s.Amount).Take(10);
        var total = top.Sum(s => s.Amount); // first enumeration of the LINQ query.
        var max = top.Max(s => s.Amount);   // second enumeration of the same query.

        return lines + " total=" + total + " max=" + max;
    }

    private static string Format(Settlement s) => s.Id + ":" + s.Amount;
}

public readonly record struct Settlement(long Id, decimal Amount);
