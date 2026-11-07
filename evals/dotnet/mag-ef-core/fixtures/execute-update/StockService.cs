using System.Linq;
using Microsoft.EntityFrameworkCore;

namespace Fixture.Inventory;

public sealed class StockService
{
    private readonly ShopDbContext _db;

    public StockService(ShopDbContext db)
    {
        _db = db;
    }

    public void DecrementStock(int productId, int quantity)
    {
        // Defect 1: ExecuteUpdate bypasses the change tracker. If the same
        // Product is already tracked, the stale tracked instance will later
        // overwrite this bulk change on SaveChanges.
        _db.Products
            .Where(p => p.Id == productId)
            .ExecuteUpdate(s => s.SetProperty(p => p.Stock, p => p.Stock - quantity));
    }

    public void AdjustTwoProducts(int aId, int bId, int delta)
    {
        // Defect 2: two ExecuteUpdate calls each run in their own implicit
        // transaction, so a failure between them leaves a partial update.
        _db.Products.Where(p => p.Id == aId)
            .ExecuteUpdate(s => s.SetProperty(p => p.Stock, p => p.Stock - delta));
        _db.Products.Where(p => p.Id == bId)
            .ExecuteUpdate(s => s.SetProperty(p => p.Stock, p => p.Stock + delta));
    }
}

public sealed class Product
{
    public int Id { get; set; }
    public int Stock { get; set; }
}

public sealed class ShopDbContext : DbContext
{
    public DbSet<Product> Products => Set<Product>();
}
