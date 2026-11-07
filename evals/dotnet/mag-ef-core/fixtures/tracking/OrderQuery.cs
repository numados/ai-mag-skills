using System.Collections.Generic;
using System.Linq;
using Microsoft.EntityFrameworkCore;

namespace Fixture.Orders;

public sealed class OrderQuery
{
    private readonly AppDbContext _db;

    public OrderQuery(AppDbContext db)
    {
        _db = db;
    }

    // Tracking query: EF performs identity resolution, so the same row loaded
    // twice returns the same instance and navigation fix-up applies.
    public Order? GetTracked(int id) =>
        _db.Orders.FirstOrDefault(o => o.Id == id);

    // No-tracking query: returns a fresh instance each time and does not
    // register the result with the change tracker.
    public Order? GetNoTracking(int id) =>
        _db.Orders.AsNoTracking().FirstOrDefault(o => o.Id == id);

    // Custom projection that still tracks the Order entity it contains,
    // because the anonymous type holds an entity type.
    public (Order? Order, decimal Total) GetProjected(int id)
    {
        var row = _db.Orders
            .Where(o => o.Id == id)
            .Select(o => new { Order = o, Total = o.Lines.Sum(l => l.Amount) })
            .FirstOrDefault();

        return row is null ? (null, 0m) : (row.Order, row.Total);
    }
}

public sealed class Order
{
    public int Id { get; set; }
    public List<OrderLine> Lines { get; set; } = new();
}

public sealed class OrderLine
{
    public int Id { get; set; }
    public int OrderId { get; set; }
    public decimal Amount { get; set; }
}

public sealed class AppDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderLine> OrderLines => Set<OrderLine>();
}
