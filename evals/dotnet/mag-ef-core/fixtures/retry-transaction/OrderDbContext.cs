using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace Fixture.Orders;

public sealed class OrderDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        // EnableRetryOnFailure configures an execution strategy that retries
        // failed commands and buffers resultsets.
        optionsBuilder.UseSqlServer(
            "Server=.;Database=Orders;Trusted_Connection=True;",
            sql => sql.EnableRetryOnFailure());
    }
}

public sealed class Order
{
    public int Id { get; set; }
    public string Number { get; set; } = string.Empty;
}

public static class OrderCheckout
{
    public static async Task PlaceAsync(OrderDbContext db, Order order)
    {
        // Defect: a manual transaction is incompatible with the retry
        // execution strategy enabled in OnConfiguring. BeginTransactionAsync
        // throws InvalidOperationException; the sequence must be wrapped in
        // db.Database.CreateExecutionStrategy().ExecuteAsync(...).
        await using var tx = await db.Database.BeginTransactionAsync();
        db.Orders.Add(order);
        await db.SaveChangesAsync();
        await tx.CommitAsync();
    }
}
